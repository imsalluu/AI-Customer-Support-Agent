import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError
from app.models.commerce import Order, OrderItem, Product
from app.schemas.commerce import OrderCreate, ProductCreate, ProductUpdate


class CommerceService:
    @staticmethod
    async def list_products(
        db: AsyncSession,
        org_id: str,
        query_str: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
    ) -> List[Product]:
        stmt = select(Product).where(Product.organization_id == org_id)
        if query_str:
            q = f"%{query_str.strip()}%"
            stmt = stmt.where(or_(Product.title.ilike(q), Product.sku.ilike(q), Product.description.ilike(q)))
        if category:
            stmt = stmt.where(Product.category.ilike(f"%{category}%"))
        stmt = stmt.order_by(Product.title.asc()).limit(limit)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_product_by_sku_or_id(db: AsyncSession, org_id: str, identifier: str) -> Optional[Product]:
        stmt = select(Product).where(
            Product.organization_id == org_id,
            or_(Product.id == identifier, Product.sku.ilike(identifier), Product.title.ilike(f"%{identifier}%")),
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def create_product(db: AsyncSession, org_id: str, data: ProductCreate) -> Product:
        product = Product(
            organization_id=org_id,
            sku=data.sku,
            title=data.title,
            description=data.description,
            category=data.category,
            price=data.price,
            currency=data.currency,
            inventory_count=data.inventory_count,
            is_active=data.is_active,
            image_url=data.image_url,
        )
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def list_orders(
        db: AsyncSession,
        org_id: str,
        customer_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[Order]:
        stmt = select(Order).options(selectinload(Order.items)).where(Order.organization_id == org_id)
        if customer_id:
            stmt = stmt.where(Order.customer_id == customer_id)
        stmt = stmt.order_by(Order.created_at.desc()).limit(limit)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_order_by_number_or_id(db: AsyncSession, org_id: str, identifier: str) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(
                Order.organization_id == org_id,
                or_(
                    Order.id == identifier,
                    Order.order_number.ilike(identifier.strip()),
                    Order.tracking_number.ilike(identifier.strip()),
                ),
            )
        )
        res = await db.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def create_order(db: AsyncSession, org_id: str, data: OrderCreate) -> Order:
        order = Order(
            organization_id=org_id,
            customer_id=data.customer_id,
            order_number=data.order_number,
            status=data.status,
            total_amount=data.total_amount,
            currency=data.currency,
            payment_status=data.payment_status,
            carrier=data.carrier,
            tracking_number=data.tracking_number,
            shipping_address=data.shipping_address,
            estimated_delivery=data.estimated_delivery,
            tracking_history_json=json.dumps([
                {
                    "status": "Order Placed",
                    "location": "Warehouse Hub",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "details": "Order confirmed and verified.",
                }
            ]),
        )
        db.add(order)
        await db.flush()

        for item_data in data.items:
            item = OrderItem(
                order_id=order.id,
                product_id=item_data.product_id,
                sku=item_data.sku,
                title=item_data.title,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                total_price=item_data.unit_price * item_data.quantity,
            )
            db.add(item)

        await db.commit()
        await db.refresh(order)
        return order
