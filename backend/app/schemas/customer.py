from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    external_id: Optional[str] = None
    avatar_url: Optional[str] = None
    tags: Optional[str] = ""
    metadata_json: Optional[str] = "{}"


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    tags: Optional[str] = None
    metadata_json: Optional[str] = None


class CustomerResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    external_id: Optional[str] = None
    avatar_url: Optional[str] = None
    total_orders: int
    lifetime_value: float
    tags: Optional[str] = ""
    created_at: datetime

    model_config = {"from_attributes": True}


class CustomerDetailResponse(CustomerResponse):
    metadata_json: Optional[str] = "{}"
