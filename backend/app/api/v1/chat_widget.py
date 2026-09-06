from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_api_key_organization
from app.core.database import get_db
from app.models.agent_config import AgentConfig
from app.models.feedback import Feedback
from app.models.tenant import Organization
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    MessageResponse,
)
from app.schemas.feedback import FeedbackCreate
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/widget", tags=["Public Web Chat Widget"])


class WidgetInitRequest(BaseModel):
    customer_name: Optional[str] = "Website Visitor"
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    conversation_id: Optional[str] = None


class WidgetInitResponse(BaseModel):
    conversation_id: str
    customer_id: str
    organization_name: str
    agent_name: str
    agent_avatar: Optional[str] = None
    greeting_message: str
    status: str
    messages: List[MessageResponse] = []


class WidgetSendMessageRequest(BaseModel):
    conversation_id: str
    message: str


class WidgetSendMessageResponse(BaseModel):
    conversation_id: str
    status: str
    customer_message: MessageResponse
    ai_response: Optional[MessageResponse] = None
    handoff_requested: bool = False


@router.post("/init", response_model=WidgetInitResponse)
async def init_widget(
    data: WidgetInitRequest,
    org: Organization = Depends(get_api_key_organization),
    db: AsyncSession = Depends(get_db),
):
    """Initialize or restore chat session for website visitor."""
    # Load agent config
    cfg_stmt = select(AgentConfig).where(AgentConfig.organization_id == org.id)
    cfg_res = await db.execute(cfg_stmt)
    cfg = cfg_res.scalar_one_or_none()

    agent_name = cfg.name if cfg else "SupportIQ Assistant"
    agent_avatar = cfg.avatar_url if cfg else None
    greeting = cfg.greeting_message if cfg else f"Hello! Welcome to {org.name}. How can I help you today?"

    conv_create = ConversationCreate(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        customer_phone=data.customer_phone,
        channel="WEBCHAT",
    )
    conv, customer, _ = await ConversationService.create_or_get_conversation(db, org.id, conv_create)

    messages_out = [
        MessageResponse(
            id=m.id,
            conversation_id=m.conversation_id,
            sender_type=m.sender_type,
            sender_id=m.sender_id,
            content=m.content,
            intent=m.intent,
            sentiment=m.sentiment,
            confidence=m.confidence,
            sources_json=m.sources_json or "[]",
            tool_calls_json=m.tool_calls_json or "[]",
            metadata_json=m.metadata_json or "{}",
            created_at=m.created_at,
        )
        for m in conv.messages
    ]

    return WidgetInitResponse(
        conversation_id=conv.id,
        customer_id=customer.id,
        organization_name=org.name,
        agent_name=agent_name,
        agent_avatar=agent_avatar,
        greeting_message=greeting,
        status=conv.status,
        messages=messages_out,
    )


@router.post("/send", response_model=WidgetSendMessageResponse)
async def send_widget_message(
    data: WidgetSendMessageRequest,
    org: Organization = Depends(get_api_key_organization),
    db: AsyncSession = Depends(get_db),
):
    """Send customer message from embeddable chat widget and receive instant grounded response."""
    conv, cust_msg, ai_msg = await ConversationService.process_customer_message(
        db, org.id, data.conversation_id, data.message
    )

    cust_msg_resp = MessageResponse(
        id=cust_msg.id,
        conversation_id=cust_msg.conversation_id,
        sender_type=cust_msg.sender_type,
        sender_id=cust_msg.sender_id,
        content=cust_msg.content,
        intent=cust_msg.intent,
        sentiment=cust_msg.sentiment,
        confidence=cust_msg.confidence,
        sources_json=cust_msg.sources_json or "[]",
        tool_calls_json=cust_msg.tool_calls_json or "[]",
        metadata_json=cust_msg.metadata_json or "{}",
        created_at=cust_msg.created_at,
    )

    ai_msg_resp = None
    if ai_msg:
        ai_msg_resp = MessageResponse(
            id=ai_msg.id,
            conversation_id=ai_msg.conversation_id,
            sender_type=ai_msg.sender_type,
            sender_id=ai_msg.sender_id,
            content=ai_msg.content,
            intent=ai_msg.intent,
            sentiment=ai_msg.sentiment,
            confidence=ai_msg.confidence,
            sources_json=ai_msg.sources_json or "[]",
            tool_calls_json=ai_msg.tool_calls_json or "[]",
            metadata_json=ai_msg.metadata_json or "{}",
            created_at=ai_msg.created_at,
        )

    return WidgetSendMessageResponse(
        conversation_id=conv.id,
        status=conv.status,
        customer_message=cust_msg_resp,
        ai_response=ai_msg_resp,
        handoff_requested=(conv.status == "WAITING_HUMAN"),
    )


@router.post("/feedback", status_code=status.HTTP_201_CREATED)
async def submit_widget_feedback(
    data: FeedbackCreate,
    org: Organization = Depends(get_api_key_organization),
    db: AsyncSession = Depends(get_db),
):
    """Submit CSAT satisfaction rating for the conversation."""
    fb = Feedback(
        organization_id=org.id,
        conversation_id=data.conversation_id,
        customer_id=data.customer_id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(fb)
    await db.commit()
    return {"success": True, "message": "Feedback submitted successfully. Thank you!"}
