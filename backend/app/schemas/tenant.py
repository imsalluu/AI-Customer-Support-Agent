from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    name: str


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    plan: Optional[str] = None
    is_active: Optional[bool] = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    api_key: str
    plan: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ApiKeyRegenerateResponse(BaseModel):
    api_key: str
    organization_id: str
