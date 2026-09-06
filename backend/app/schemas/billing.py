from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    id: str
    organization_id: str
    plan: str
    is_active: bool
    max_monthly_messages: int
    current_month_messages: int
    max_knowledge_docs: int
    current_docs_count: int
    max_agents: int
    current_agents_count: int
    current_period_end: Optional[datetime] = None

    model_config = {"from_attributes": True}


class PlanChangeRequest(BaseModel):
    plan: str
