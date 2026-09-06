from typing import Optional
from sqlalchemy import Boolean, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import AgentTone
from app.core.database import Base, TimestampMixin, TenantMixin


class AgentConfig(Base, TimestampMixin, TenantMixin):
    __tablename__ = "agent_configs"

    organization_id: Mapped[str] = mapped_column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), default="SupportIQ Assistant", nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    tone: Mapped[str] = mapped_column(String(50), default=AgentTone.PROFESSIONAL.value, nullable=False)
    language: Mapped[str] = mapped_column(String(50), default="en", nullable=False)
    personality_prompt: Mapped[str] = mapped_column(
        Text,
        default="You are SupportIQ, a helpful, polite, and precise customer support specialist.",
        nullable=False,
    )
    greeting_message: Mapped[str] = mapped_column(
        Text,
        default="Hello! How can I assist you with your orders, products, or support today?",
        nullable=False,
    )
    business_hours_json: Mapped[Optional[str]] = mapped_column(
        Text,
        default='{"timezone": "UTC", "monday_friday": "09:00-18:00", "saturday_sunday": "closed"}',
        nullable=True,
    )
    escalation_rules_json: Mapped[Optional[str]] = mapped_column(
        Text,
        default='{"sentiment_angry_escalate": true, "max_failed_attempts": 2, "vip_customer_escalate": true}',
        nullable=True,
    )
    confidence_threshold: Mapped[float] = mapped_column(Float, default=0.75, nullable=False)
    enabled_tools_json: Mapped[Optional[str]] = mapped_column(
        Text,
        default='["search_customer","get_customer","search_order","get_order_status","search_products","get_product","check_inventory","create_support_ticket","update_support_ticket","check_shipping","request_human_agent"]',
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    organization: Mapped["Organization"] = relationship("Organization", back_populates="agent_config")
