import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.agents.engine import SupportAgentEngine
from app.core.constants import ConversationStatus, SenderType
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.conversation import Conversation, Message
from app.models.customer import Customer
from app.models.tenant import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
)
from app.services.customer_service import CustomerService


class ConversationService:
    @staticmethod
    async def list_conversations(
        db: AsyncSession,
        org_id: str,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        assigned_agent_id: Optional[str] = None,
        customer_id: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Conversation]:
        stmt = (
            select(Conversation)
            .options(
                selectinload(Conversation.customer),
                selectinload(Conversation.assigned_agent),
                selectinload(Conversation.messages),
            )
            .where(Conversation.organization_id == org_id)
        )
        if status:
            stmt = stmt.where(Conversation.status == status)
        if channel:
            stmt = stmt.where(Conversation.channel == channel)
        if assigned_agent_id:
            stmt = stmt.where(Conversation.assigned_agent_id == assigned_agent_id)
        if customer_id:
            stmt = stmt.where(Conversation.customer_id == customer_id)
        if search_query:
            q = f"%{search_query.strip()}%"
            stmt = stmt.join(Customer).where(
                or_(
                    Customer.name.ilike(q),
                    Customer.email.ilike(q),
                    Conversation.summary.ilike(q),
                )
            )

        stmt = stmt.order_by(Conversation.updated_at.desc()).limit(limit).offset(offset)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_conversation_by_id(db: AsyncSession, org_id: str, conv_id: str) -> Conversation:
        stmt = (
            select(Conversation)
            .options(
                selectinload(Conversation.customer),
                selectinload(Conversation.assigned_agent),
                selectinload(Conversation.messages),
                selectinload(Conversation.tickets),
            )
            .where(Conversation.id == conv_id, Conversation.organization_id == org_id)
        )
        res = await db.execute(stmt)
        conv = res.scalar_one_or_none()
        if not conv:
            raise NotFoundError("Conversation", conv_id)
        return conv

    @staticmethod
    async def create_or_get_conversation(
        db: AsyncSession,
        org_id: str,
        data: ConversationCreate,
    ) -> Tuple[Conversation, Customer, Optional[Message]]:
        # Find or create customer
        if data.customer_id:
            customer = await CustomerService.get_customer_by_id(db, org_id, data.customer_id)
        else:
            customer = await CustomerService.get_or_create(
                db,
                org_id,
                name=data.customer_name or "Guest Visitor",
                email=data.customer_email,
                phone=data.customer_phone,
            )

        # Look for existing active conversation for this customer
        active_stmt = (
            select(Conversation)
            .where(
                Conversation.organization_id == org_id,
                Conversation.customer_id == customer.id,
                Conversation.status.in_([
                    ConversationStatus.AI_ACTIVE.value,
                    ConversationStatus.WAITING_HUMAN.value,
                    ConversationStatus.HUMAN_ACTIVE.value,
                ]),
            )
            .order_by(Conversation.created_at.desc())
        )
        res = await db.execute(active_stmt)
        conv = res.scalar_one_or_none()

        if not conv:
            conv = Conversation(
                organization_id=org_id,
                customer_id=customer.id,
                channel=data.channel,
                status=ConversationStatus.AI_ACTIVE.value,
            )
            db.add(conv)
            await db.commit()
            await db.refresh(conv)

        ai_response_msg = None
        if data.initial_message:
            conv, _, ai_response_msg = await ConversationService.process_customer_message(
                db, org_id, conv.id, data.initial_message
            )

        conv = await ConversationService.get_conversation_by_id(db, org_id, conv.id)
        return conv, customer, ai_response_msg

    @staticmethod
    async def process_customer_message(
        db: AsyncSession,
        org_id: str,
        conv_id: str,
        message_text: str,
    ) -> Tuple[Conversation, Message, Optional[Message]]:
        conv = await ConversationService.get_conversation_by_id(db, org_id, conv_id)
        customer = conv.customer

        # Save customer message
        cust_msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.CUSTOMER.value,
            sender_id=customer.id,
            content=message_text,
        )
        db.add(cust_msg)
        await db.flush()

        ai_msg = None

        # If human is actively managing, AI stays dormant
        if conv.status == ConversationStatus.HUMAN_ACTIVE.value:
            conv.updated_at = datetime.now(timezone.utc)
            await db.commit()
            return conv, cust_msg, None

        # Build conversation history for LLM
        history: List[Dict[str, str]] = []
        for m in conv.messages[-6:]:
            role = "user" if m.sender_type == SenderType.CUSTOMER.value else "assistant"
            history.append({"role": role, "content": m.content})

        # Process through SupportAgentEngine
        agent_result = await SupportAgentEngine.process_message(
            db=db,
            org_id=org_id,
            customer=customer,
            conversation_id=conv.id,
            message_text=message_text,
            conversation_history=history,
        )

        # Update customer message with detected intent and sentiment
        cust_msg.intent = agent_result.intent
        cust_msg.sentiment = agent_result.sentiment

        # Update conversation status and summary
        conv.current_intent = agent_result.intent
        conv.sentiment = agent_result.sentiment
        conv.confidence_score = agent_result.confidence
        if agent_result.summary_update:
            conv.summary = f"{conv.summary} | {agent_result.summary_update}".strip(" |")

        if agent_result.handoff_requested:
            conv.status = ConversationStatus.WAITING_HUMAN.value

        # Save AI Response Message
        citations_json = json.dumps([c.model_dump() for c in agent_result.citations])
        tool_calls_json = json.dumps([t.model_dump() for t in agent_result.tool_executions])

        ai_msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.AI.value,
            content=agent_result.response_text,
            intent=agent_result.intent,
            sentiment=agent_result.sentiment,
            confidence=agent_result.confidence,
            sources_json=citations_json,
            tool_calls_json=tool_calls_json,
        )
        db.add(ai_msg)

        conv.updated_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(cust_msg)
        await db.refresh(ai_msg)

        return conv, cust_msg, ai_msg

    @staticmethod
    async def send_agent_message(
        db: AsyncSession,
        org_id: str,
        conv_id: str,
        agent_user: User,
        content: str,
    ) -> Message:
        conv = await ConversationService.get_conversation_by_id(db, org_id, conv_id)
        conv.status = ConversationStatus.HUMAN_ACTIVE.value
        conv.assigned_agent_id = agent_user.id
        conv.updated_at = datetime.now(timezone.utc)

        msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.AGENT.value,
            sender_id=agent_user.id,
            content=content,
        )
        db.add(msg)
        await db.commit()
        await db.refresh(msg)
        return msg

    @staticmethod
    async def take_over(db: AsyncSession, org_id: str, conv_id: str, agent_user: User) -> Conversation:
        conv = await ConversationService.get_conversation_by_id(db, org_id, conv_id)
        conv.status = ConversationStatus.HUMAN_ACTIVE.value
        conv.assigned_agent_id = agent_user.id
        conv.updated_at = datetime.now(timezone.utc)

        sys_msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.SYSTEM.value,
            content=f"Support Specialist {agent_user.full_name} has joined the conversation.",
        )
        db.add(sys_msg)
        await db.commit()
        return await ConversationService.get_conversation_by_id(db, org_id, conv.id)

    @staticmethod
    async def release_to_ai(db: AsyncSession, org_id: str, conv_id: str) -> Conversation:
        conv = await ConversationService.get_conversation_by_id(db, org_id, conv_id)
        conv.status = ConversationStatus.AI_ACTIVE.value
        conv.updated_at = datetime.now(timezone.utc)

        sys_msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.SYSTEM.value,
            content="Conversation returned to AI Support Agent.",
        )
        db.add(sys_msg)
        await db.commit()
        return await ConversationService.get_conversation_by_id(db, org_id, conv.id)

    @staticmethod
    async def resolve(db: AsyncSession, org_id: str, conv_id: str) -> Conversation:
        conv = await ConversationService.get_conversation_by_id(db, org_id, conv_id)
        conv.status = ConversationStatus.RESOLVED.value
        conv.resolved_at = datetime.now(timezone.utc)
        conv.updated_at = datetime.now(timezone.utc)

        sys_msg = Message(
            organization_id=org_id,
            conversation_id=conv.id,
            sender_type=SenderType.SYSTEM.value,
            content="Conversation marked as resolved.",
        )
        db.add(sys_msg)
        await db.commit()
        return await ConversationService.get_conversation_by_id(db, org_id, conv.id)
