from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.tenant import User
from app.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    StatusUpdateRequest,
    TakeoverRequest,
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["Support Inbox & Conversations"])


def map_conversation_detail(conv) -> ConversationDetailResponse:
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

    return ConversationDetailResponse(
        id=conv.id,
        organization_id=conv.organization_id,
        customer_id=conv.customer_id,
        channel=conv.channel,
        status=conv.status,
        current_intent=conv.current_intent,
        sentiment=conv.sentiment,
        confidence_score=conv.confidence_score,
        assigned_agent_id=conv.assigned_agent_id,
        summary=conv.summary,
        created_at=conv.created_at,
        updated_at=conv.updated_at,
        resolved_at=conv.resolved_at,
        customer_name=conv.customer.name if conv.customer else "Guest Visitor",
        customer_email=conv.customer.email if conv.customer else None,
        customer_phone=conv.customer.phone if conv.customer else None,
        customer_total_orders=conv.customer.total_orders if conv.customer else 0,
        customer_lifetime_value=conv.customer.lifetime_value if conv.customer else 0.0,
        assigned_agent_name=conv.assigned_agent.full_name if conv.assigned_agent else None,
        messages=messages_out,
    )


@router.get("", response_model=List[ConversationDetailResponse])
async def list_conversations(
    status: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    assigned_agent_id: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Search by customer name, email, or summary"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List support conversations with status and channel filtering."""
    convs = await ConversationService.list_conversations(
        db,
        current_user.organization_id,
        status=status,
        channel=channel,
        assigned_agent_id=assigned_agent_id,
        customer_id=customer_id,
        search_query=q,
        limit=limit,
        offset=offset,
    )
    return [map_conversation_detail(c) for c in convs]


@router.post("", response_model=ConversationDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create or resume an active conversation."""
    conv, _, _ = await ConversationService.create_or_get_conversation(db, current_user.organization_id, data)
    return map_conversation_detail(conv)


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get single conversation details with all messages and customer 360 profile."""
    conv = await ConversationService.get_conversation_by_id(db, current_user.organization_id, conversation_id)
    return map_conversation_detail(conv)


@router.post("/{conversation_id}/messages", response_model=MessageResponse)
async def send_agent_message(
    conversation_id: str,
    data: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Send an agent reply into the conversation (stops AI auto-reply)."""
    msg = await ConversationService.send_agent_message(
        db, current_user.organization_id, conversation_id, current_user, data.content
    )
    return MessageResponse(
        id=msg.id,
        conversation_id=msg.conversation_id,
        sender_type=msg.sender_type,
        sender_id=msg.sender_id,
        content=msg.content,
        intent=msg.intent,
        sentiment=msg.sentiment,
        confidence=msg.confidence,
        sources_json=msg.sources_json or "[]",
        tool_calls_json=msg.tool_calls_json or "[]",
        metadata_json=msg.metadata_json or "{}",
        created_at=msg.created_at,
    )


@router.post("/{conversation_id}/takeover", response_model=ConversationDetailResponse)
async def takeover_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Support agent takes over the conversation (pauses AI)."""
    conv = await ConversationService.take_over(db, current_user.organization_id, conversation_id, current_user)
    return map_conversation_detail(conv)


@router.post("/{conversation_id}/release", response_model=ConversationDetailResponse)
async def release_conversation_to_ai(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return conversation back to AI automation."""
    conv = await ConversationService.release_to_ai(db, current_user.organization_id, conversation_id)
    return map_conversation_detail(conv)


@router.post("/{conversation_id}/resolve", response_model=ConversationDetailResponse)
async def resolve_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark conversation as resolved."""
    conv = await ConversationService.resolve(db, current_user.organization_id, conversation_id)
    return map_conversation_detail(conv)
