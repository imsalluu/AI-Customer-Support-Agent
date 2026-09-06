from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.core.constants import AgentTone


class AgentConfigUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    tone: Optional[str] = None
    language: Optional[str] = None
    personality_prompt: Optional[str] = None
    greeting_message: Optional[str] = None
    business_hours_json: Optional[str] = None
    escalation_rules_json: Optional[str] = None
    confidence_threshold: Optional[float] = None
    enabled_tools_json: Optional[str] = None
    is_active: Optional[bool] = None


class AgentConfigResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    avatar_url: Optional[str] = None
    tone: str
    language: str
    personality_prompt: str
    greeting_message: str
    business_hours_json: Optional[str] = None
    escalation_rules_json: Optional[str] = None
    confidence_threshold: float
    enabled_tools_json: Optional[str] = None
    is_active: bool
    updated_at: datetime

    model_config = {"from_attributes": True}
