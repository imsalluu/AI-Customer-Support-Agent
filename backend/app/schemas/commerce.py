from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ProductCreate(BaseModel):
    sku: str
    title: str
    description: Optional[str] = None
    category: str = "General"
    price: float
    currency: str = "USD"
    inventory_count: int = 0
    is_active: bool = True
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    inventory_count: Optional[int] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None


class ProductResponse(BaseModel):
    id: str
    organization_id: str
    sku: str
    title: str
    description: Optional[str] = None
    category: str
    price: float
    currency: str
    inventory_count: int
    is_active: bool
    image_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderItemCreate(BaseModel):
    product_id: Optional[str] = None
    sku: str
    title: str
    quantity: int = 1
    unit_price: float


class OrderItemResponse(BaseModel):
    id: str
    order_id: str
    product_id: Optional[str] = None
    sku: str
    title: str
    quantity: int
    unit_price: float
    total_price: float

    model_config = {"from_attributes": True}


class OrderCreate(BaseModel):
    customer_id: str
    order_number: str
    status: str = "PROCESSING"
    total_amount: float
    currency: str = "USD"
    payment_status: str = "PAID"
    carrier: Optional[str] = "FedEx"
    tracking_number: Optional[str] = None
    shipping_address: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    items: List[OrderItemCreate] = []


class OrderResponse(BaseModel):
    id: str
    organization_id: str
    customer_id: str
    order_number: str
    status: str
    total_amount: float
    currency: str
    payment_status: str
    carrier: Optional[str] = None
    tracking_number: Optional[str] = None
    shipping_address: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    tracking_history_json: Optional[str] = "[]"
    created_at: datetime
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True}
