from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.core.constants import TicketCategory, TicketPriority, TicketStatus


class TicketCreate(BaseModel):
    customer_id: str
    conversation_id: Optional[str] = None
    subject: str
    description: str
    priority: str = TicketPriority.MEDIUM.value
    category: str = TicketCategory.GENERAL.value
    assigned_agent_id: Optional[str] = None


class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    resolution_notes: Optional[str] = None


class TicketResponse(BaseModel):
    id: str
    ticket_number: str
    organization_id: str
    customer_id: str
    conversation_id: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    subject: str
    description: str
    status: str
    priority: str
    category: str
    resolution_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    assigned_agent_name: Optional[str] = None

    model_config = {"from_attributes": True}
