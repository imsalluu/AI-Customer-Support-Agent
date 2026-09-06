from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.core.constants import TicketPriority, TicketStatus
from app.core.exceptions import NotFoundError
from app.models.customer import Customer
from app.models.tenant import User
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate


class TicketService:
    @staticmethod
    async def list_tickets(
        db: AsyncSession,
        org_id: str,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
        customer_id: Optional[str] = None,
        assigned_agent_id: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Ticket]:
        stmt = (
            select(Ticket)
            .options(selectinload(Ticket.customer), selectinload(Ticket.assigned_agent))
            .where(Ticket.organization_id == org_id)
        )
        if status:
            stmt = stmt.where(Ticket.status == status)
        if priority:
            stmt = stmt.where(Ticket.priority == priority)
        if category:
            stmt = stmt.where(Ticket.category == category)
        if customer_id:
            stmt = stmt.where(Ticket.customer_id == customer_id)
        if assigned_agent_id:
            stmt = stmt.where(Ticket.assigned_agent_id == assigned_agent_id)
        if search_query:
            q = f"%{search_query.strip()}%"
            stmt = stmt.where(
                or_(
                    Ticket.ticket_number.ilike(q),
                    Ticket.subject.ilike(q),
                    Ticket.description.ilike(q),
                )
            )

        stmt = stmt.order_by(Ticket.created_at.desc()).limit(limit).offset(offset)
        res = await db.execute(stmt)
        return res.scalars().all()

    @staticmethod
    async def get_ticket_by_id(db: AsyncSession, org_id: str, ticket_id: str) -> Ticket:
        stmt = (
            select(Ticket)
            .options(selectinload(Ticket.customer), selectinload(Ticket.assigned_agent))
            .where(
                Ticket.organization_id == org_id,
                or_(Ticket.id == ticket_id, Ticket.ticket_number == ticket_id),
            )
        )
        res = await db.execute(stmt)
        ticket = res.scalar_one_or_none()
        if not ticket:
            raise NotFoundError("Ticket", ticket_id)
        return ticket

    @staticmethod
    async def create_ticket(db: AsyncSession, org_id: str, data: TicketCreate) -> Ticket:
        ticket = Ticket(
            organization_id=org_id,
            customer_id=data.customer_id,
            conversation_id=data.conversation_id,
            assigned_agent_id=data.assigned_agent_id,
            subject=data.subject,
            description=data.description,
            priority=data.priority,
            category=data.category,
            status=TicketStatus.OPEN.value,
        )
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        return await TicketService.get_ticket_by_id(db, org_id, ticket.id)

    @staticmethod
    async def update_ticket(
        db: AsyncSession,
        org_id: str,
        ticket_id: str,
        data: TicketUpdate,
    ) -> Ticket:
        ticket = await TicketService.get_ticket_by_id(db, org_id, ticket_id)
        if data.subject is not None:
            ticket.subject = data.subject
        if data.description is not None:
            ticket.description = data.description
        if data.status is not None:
            ticket.status = data.status
            if data.status in [TicketStatus.RESOLVED.value, TicketStatus.CLOSED.value]:
                ticket.resolved_at = datetime.now(timezone.utc)
            else:
                ticket.resolved_at = None
        if data.priority is not None:
            ticket.priority = data.priority
        if data.category is not None:
            ticket.category = data.category
        if data.assigned_agent_id is not None:
            ticket.assigned_agent_id = data.assigned_agent_id
        if data.resolution_notes is not None:
            ticket.resolution_notes = data.resolution_notes

        await db.commit()
        await db.refresh(ticket)
        return await TicketService.get_ticket_by_id(db, org_id, ticket.id)

    @staticmethod
    async def get_stats(db: AsyncSession, org_id: str) -> dict:
        stmt = (
            select(
                Ticket.status,
                func.count(Ticket.id),
            )
            .where(Ticket.organization_id == org_id)
            .group_by(Ticket.status)
        )
        res = await db.execute(stmt)
        counts = dict(res.all())
        total = sum(counts.values())
        return {
            "total": total,
            "open": counts.get(TicketStatus.OPEN.value, 0),
            "in_progress": counts.get(TicketStatus.IN_PROGRESS.value, 0),
            "waiting_customer": counts.get(TicketStatus.WAITING_CUSTOMER.value, 0),
            "resolved": counts.get(TicketStatus.RESOLVED.value, 0),
            "closed": counts.get(TicketStatus.CLOSED.value, 0),
        }
