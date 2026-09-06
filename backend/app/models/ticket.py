import random
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import TicketCategory, TicketPriority, TicketStatus
from app.core.database import Base, TimestampMixin, TenantMixin


def generate_ticket_number() -> str:
    return f"TCK-{random.randint(10000, 99999)}"


class Ticket(Base, TimestampMixin, TenantMixin):
    __tablename__ = "tickets"

    ticket_number: Mapped[str] = mapped_column(String(50), default=generate_ticket_number, unique=True, index=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    conversation_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True)
    assigned_agent_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=TicketStatus.OPEN.value, index=True, nullable=False)
    priority: Mapped[str] = mapped_column(String(50), default=TicketPriority.MEDIUM.value, index=True, nullable=False)
    category: Mapped[str] = mapped_column(String(50), default=TicketCategory.GENERAL.value, index=True, nullable=False)

    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="tickets")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="tickets")
    conversation: Mapped[Optional["Conversation"]] = relationship("Conversation", back_populates="tickets")
    assigned_agent: Mapped[Optional["User"]] = relationship("User", foreign_keys=[assigned_agent_id])
