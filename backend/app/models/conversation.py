from datetime import datetime
from typing import List, Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import ChannelType, ConversationStatus, IntentType, SenderType, SentimentType
from app.core.database import Base, TimestampMixin, TenantMixin


class Conversation(Base, TimestampMixin, TenantMixin):
    __tablename__ = "conversations"

    customer_id: Mapped[str] = mapped_column(String(36), ForeignKey("customers.id", ondelete="CASCADE"), index=True, nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default=ChannelType.WEBCHAT.value, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default=ConversationStatus.AI_ACTIVE.value, index=True, nullable=False)
    current_intent: Mapped[Optional[str]] = mapped_column(String(50), default=IntentType.GENERAL.value, index=True, nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50), default=SentimentType.NEUTRAL.value, index=True, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    assigned_agent_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    summary: Mapped[Optional[str]] = mapped_column(Text, default="", nullable=True)
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, default="{}", nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="conversations")
    organization: Mapped["Organization"] = relationship("Organization", back_populates="conversations")
    assigned_agent: Mapped[Optional["User"]] = relationship("User", foreign_keys=[assigned_agent_id])
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="conversation")


class Message(Base, TimestampMixin, TenantMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(String(36), ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=False)
    sender_type: Mapped[str] = mapped_column(String(50), default=SenderType.CUSTOMER.value, nullable=False)
    sender_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)  # User id or customer id
    content: Mapped[str] = mapped_column(Text, nullable=False)
    intent: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    sentiment: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sources_json: Mapped[Optional[str]] = mapped_column(Text, default="[]", nullable=True)  # Array of citations
    tool_calls_json: Mapped[Optional[str]] = mapped_column(Text, default="[]", nullable=True)  # Array of tool executions
    metadata_json: Mapped[Optional[str]] = mapped_column(Text, default="{}", nullable=True)

    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
