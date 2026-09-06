from typing import List, Optional
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.ticket import Ticket
from app.models.commerce import Order
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    @staticmethod
    async def list_customers(
        db: AsyncSession,
        org_id: str,
        query_str: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Customer]:
        stmt = select(Customer).where(Customer.organization_id == org_id)
        if query_str:
            q = f"%{query_str.strip()}%"
            stmt = stmt.where(
                or_(
                    Customer.name.ilike(q),
                    Customer.email.ilike(q),
                    Customer.phone.ilike(q),
                    Customer.tags.ilike(q),
                )
            )
        stmt = stmt.order_by(Customer.created_at.desc()).limit(limit).offset(offset)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_customer_by_id(db: AsyncSession, org_id: str, customer_id: str) -> Customer:
        stmt = select(Customer).where(Customer.id == customer_id, Customer.organization_id == org_id)
        res = await db.execute(stmt)
        customer = res.scalar_one_or_none()
        if not customer:
            raise NotFoundError("Customer", customer_id)
        return customer

    @staticmethod
    async def get_or_create(
        db: AsyncSession,
        org_id: str,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        external_id: Optional[str] = None,
    ) -> Customer:
        conditions = [Customer.organization_id == org_id]
        match_clauses = []
        if email:
            match_clauses.append(Customer.email == email)
        if phone:
            match_clauses.append(Customer.phone == phone)
        if external_id:
            match_clauses.append(Customer.external_id == external_id)

        if match_clauses:
            stmt = select(Customer).where(*conditions, or_(*match_clauses))
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                if name and existing.name == "Guest Visitor":
                    existing.name = name
                    await db.commit()
                return existing

        # Create new customer
        customer = Customer(
            organization_id=org_id,
            name=name or "Guest Visitor",
            email=email,
            phone=phone,
            external_id=external_id,
            total_orders=0,
            lifetime_value=0.0,
            tags="New",
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def update_customer(
        db: AsyncSession,
        org_id: str,
        customer_id: str,
        data: CustomerUpdate,
    ) -> Customer:
        customer = await CustomerService.get_customer_by_id(db, org_id, customer_id)
        if data.name is not None:
            customer.name = data.name
        if data.email is not None:
            customer.email = data.email
        if data.phone is not None:
            customer.phone = data.phone
        if data.avatar_url is not None:
            customer.avatar_url = data.avatar_url
        if data.tags is not None:
            customer.tags = data.tags
        if data.metadata_json is not None:
            customer.metadata_json = data.metadata_json

        await db.commit()
        await db.refresh(customer)
        return customer

    @staticmethod
    async def get_customer_360(db: AsyncSession, org_id: str, customer_id: str) -> dict:
        customer = await CustomerService.get_customer_by_id(db, org_id, customer_id)
        
        # Load orders
        orders_stmt = select(Order).where(Order.customer_id == customer_id, Order.organization_id == org_id).order_by(Order.created_at.desc()).limit(10)
        orders_res = await db.execute(orders_stmt)
        orders = orders_res.scalars().all()

        # Load tickets
        tickets_stmt = select(Ticket).where(Ticket.customer_id == customer_id, Ticket.organization_id == org_id).order_by(Ticket.created_at.desc()).limit(10)
        tickets_res = await db.execute(tickets_stmt)
        tickets = tickets_res.scalars().all()

        # Load conversations
        convs_stmt = select(Conversation).where(Conversation.customer_id == customer_id, Conversation.organization_id == org_id).order_by(Conversation.created_at.desc()).limit(5)
        convs_res = await db.execute(convs_stmt)
        convs = convs_res.scalars().all()

        return {
            "customer": customer,
            "orders": orders,
            "tickets": tickets,
            "recent_conversations": convs,
        }
