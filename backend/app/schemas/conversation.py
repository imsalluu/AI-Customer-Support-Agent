from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.core.constants import ChannelType, ConversationStatus, SenderType


class CitationSchema(BaseModel):
    document_title: str
    source_name: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    snippet: str
    relevance_score: Optional[float] = None


class ToolExecutionSchema(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]
    output: Any
    timestamp: Optional[str] = None


class MessageCreate(BaseModel):
    content: str
    sender_type: str = SenderType.CUSTOMER.value
    sender_id: Optional[str] = None


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    sender_type: str
    sender_id: Optional[str] = None
    content: str
    intent: Optional[str] = None
    sentiment: Optional[str] = None
    confidence: Optional[float] = None
    sources_json: Optional[str] = "[]"
    tool_calls_json: Optional[str] = "[]"
    metadata_json: Optional[str] = "{}"
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationCreate(BaseModel):
    customer_id: Optional[str] = None
    customer_name: Optional[str] = "Guest Visitor"
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    channel: str = ChannelType.WEBCHAT.value
    initial_message: Optional[str] = None


class ConversationResponse(BaseModel):
    id: str
    organization_id: str
    customer_id: str
    channel: str
    status: str
    current_intent: Optional[str] = None
    sentiment: Optional[str] = None
    confidence_score: float
    assigned_agent_id: Optional[str] = None
    summary: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class ConversationDetailResponse(ConversationResponse):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_total_orders: Optional[int] = 0
    customer_lifetime_value: Optional[float] = 0.0
    assigned_agent_name: Optional[str] = None
    messages: List[MessageResponse] = []


class TakeoverRequest(BaseModel):
    agent_id: Optional[str] = None
    status: str = ConversationStatus.HUMAN_ACTIVE.value


class StatusUpdateRequest(BaseModel):
    status: str
    resolution_notes: Optional[str] = None
