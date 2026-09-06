from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_roles
from app.core.constants import Role
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.tenant import User
from app.schemas.commerce import ProductCreate, ProductResponse, ProductUpdate
from app.services.commerce_service import CommerceService

router = APIRouter(prefix="/products", tags=["Product Catalog"])


@router.get("", response_model=List[ProductResponse])
async def list_products(
    q: Optional[str] = Query(None, description="Search products by title, SKU, or description"),
    category: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List products in the organization's catalog."""
    return await CommerceService.list_products(db, current_user.organization_id, q, category, limit)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Add a product to the catalog."""
    return await CommerceService.create_product(db, current_user.organization_id, data)


@router.get("/{identifier}", response_model=ProductResponse)
async def get_product(
    identifier: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get product details by SKU or ID."""
    product = await CommerceService.get_product_by_sku_or_id(db, current_user.organization_id, identifier)
    if not product:
        raise NotFoundError("Product", identifier)
    return product
