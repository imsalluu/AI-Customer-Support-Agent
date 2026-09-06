from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.tenant import User
from app.schemas.customer import (
    CustomerCreate,
    CustomerDetailResponse,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers CRM"])


@router.get("", response_model=List[CustomerResponse])
async def list_customers(
    q: Optional[str] = Query(None, description="Search by name, email, phone, or tags"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List and search customers in the organization."""
    return await CustomerService.list_customers(db, current_user.organization_id, q, limit, offset)


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    data: CustomerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new customer profile."""
    return await CustomerService.get_or_create(
        db,
        current_user.organization_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        external_id=data.external_id,
    )


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get single customer profile by ID."""
    return await CustomerService.get_customer_by_id(db, current_user.organization_id, customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    data: CustomerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update customer profile."""
    return await CustomerService.update_customer(db, current_user.organization_id, customer_id, data)


@router.get("/{customer_id}/360")
async def get_customer_360(
    customer_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get 360-degree customer intelligence including orders, tickets, and conversation history."""
    return await CustomerService.get_customer_360(db, current_user.organization_id, customer_id)
