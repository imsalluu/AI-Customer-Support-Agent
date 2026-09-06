from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import PlanType
from app.core.database import Base, TimestampMixin, TenantMixin


class Subscription(Base, TimestampMixin, TenantMixin):
    __tablename__ = "subscriptions"

    plan: Mapped[str] = mapped_column(String(50), default=PlanType.STARTER.value, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    max_monthly_messages: Mapped[int] = mapped_column(Integer, default=5000, nullable=False)
    current_month_messages: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_knowledge_docs: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    max_agents: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)


class UsageRecord(Base, TimestampMixin, TenantMixin):
    __tablename__ = "usage_records"

    metric: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # "ai_message", "tool_call", "rag_query"
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    period_date: Mapped[str] = mapped_column(String(10), index=True, nullable=False)  # YYYY-MM
