from typing import Optional
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.constants import ChannelType
from app.core.database import Base, TimestampMixin, TenantMixin


class Channel(Base, TimestampMixin, TenantMixin):
    __tablename__ = "channels"

    channel_type: Mapped[str] = mapped_column(String(50), default=ChannelType.WEBCHAT.value, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config_json: Mapped[Optional[str]] = mapped_column(Text, default="{}", nullable=True)
    webhook_secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
