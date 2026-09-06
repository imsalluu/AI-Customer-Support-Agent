from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.tenant import User
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["Support Tickets"])


def map_ticket_response(ticket) -> TicketResponse:
    return TicketResponse(
        id=ticket.id,
        ticket_number=ticket.ticket_number,
        organization_id=ticket.organization_id,
        customer_id=ticket.customer_id,
        conversation_id=ticket.conversation_id,
        assigned_agent_id=ticket.assigned_agent_id,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        category=ticket.category,
        resolution_notes=ticket.resolution_notes,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        resolved_at=ticket.resolved_at,
        customer_name=ticket.customer.name if ticket.customer else "Unknown Customer",
        customer_email=ticket.customer.email if ticket.customer else None,
        assigned_agent_name=ticket.assigned_agent.full_name if ticket.assigned_agent else None,
    )


@router.get("", response_model=List[TicketResponse])
async def list_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    customer_id: Optional[str] = Query(None),
    assigned_agent_id: Optional[str] = Query(None),
    q: Optional[str] = Query(None, description="Search by number, subject, description"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List and filter support tickets."""
    tickets = await TicketService.list_tickets(
        db,
        current_user.organization_id,
        status=status,
        priority=priority,
        category=category,
        customer_id=customer_id,
        assigned_agent_id=assigned_agent_id,
        search_query=q,
        limit=limit,
        offset=offset,
    )
    return [map_ticket_response(t) for t in tickets]


@router.post("", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    data: TicketCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new support ticket."""
    ticket = await TicketService.create_ticket(db, current_user.organization_id, data)
    return map_ticket_response(ticket)


@router.get("/stats/summary")
async def get_ticket_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get ticket counts breakdown by status."""
    return await TicketService.get_stats(db, current_user.organization_id)


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get single ticket details."""
    ticket = await TicketService.get_ticket_by_id(db, current_user.organization_id, ticket_id)
    return map_ticket_response(ticket)


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    data: TicketUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update ticket status, assignment, priority, or notes."""
    ticket = await TicketService.update_ticket(db, current_user.organization_id, ticket_id, data)
    return map_ticket_response(ticket)
