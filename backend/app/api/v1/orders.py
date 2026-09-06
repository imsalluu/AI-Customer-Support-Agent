from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.tenant import User
from app.schemas.commerce import OrderCreate, OrderResponse
from app.services.commerce_service import CommerceService

router = APIRouter(prefix="/orders", tags=["Orders & Shipping"])


@router.get("", response_model=List[OrderResponse])
async def list_orders(
    customer_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List orders with items."""
    return await CommerceService.list_orders(db, current_user.organization_id, customer_id, limit)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new order record."""
    return await CommerceService.create_order(db, current_user.organization_id, data)


@router.get("/{identifier}", response_model=OrderResponse)
async def get_order(
    identifier: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get order details and tracking status by Order ID, Order Number, or Tracking Number."""
    order = await CommerceService.get_order_by_number_or_id(db, current_user.organization_id, identifier)
    if not order:
        raise NotFoundError("Order", identifier)
    return order
