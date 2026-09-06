from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel
from app.core.constants import ChannelType


class ChannelCreate(BaseModel):
    channel_type: str = ChannelType.WEBCHAT.value
    name: str
    is_enabled: bool = True
    config_json: Optional[str] = "{}"
    webhook_secret: Optional[str] = None


class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    is_enabled: Optional[bool] = None
    config_json: Optional[str] = None
    webhook_secret: Optional[str] = None


class ChannelResponse(BaseModel):
    id: str
    organization_id: str
    channel_type: str
    name: str
    is_enabled: bool
    config_json: Optional[str] = "{}"
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class WebhookPayloadSchema(BaseModel):
    sender_id: str
    sender_name: Optional[str] = "Customer"
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None
    message_text: str
    external_message_id: Optional[str] = None
    channel_type: str = ChannelType.WHATSAPP.value
    metadata: Optional[Dict[str, Any]] = None
