from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class FeedbackCreate(BaseModel):
    conversation_id: str
    customer_id: Optional[str] = None
    rating: int  # 1 (positive) or -1 (negative) or 1-5
    comment: Optional[str] = None
    tags: Optional[List[str]] = []


class FeedbackResponse(BaseModel):
    id: str
    organization_id: str
    conversation_id: str
    customer_id: Optional[str] = None
    rating: int
    comment: Optional[str] = None
    tags_json: Optional[str] = "[]"
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditLogResponse(BaseModel):
    id: str
    organization_id: str
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details_json: Optional[str] = "{}"
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
