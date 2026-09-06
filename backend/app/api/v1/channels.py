from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_roles
from app.core.constants import Role
from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.models.channel import Channel
from app.models.tenant import User
from app.schemas.channel import ChannelCreate, ChannelResponse, ChannelUpdate

router = APIRouter(prefix="/channels", tags=["Channel Integrations"])


@router.get("", response_model=List[ChannelResponse])
async def list_channels(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List connected support channels (WebChat, WhatsApp, Messenger, Email)."""
    stmt = select(Channel).where(Channel.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    channels = res.scalars().all()

    if not channels:
        # Initialize default WebChat and WhatsApp channel records
        webchat = Channel(
            organization_id=current_user.organization_id,
            channel_type="WEBCHAT",
            name="Website Live Chat Widget",
            is_enabled=True,
            config_json='{"theme": "indigo", "position": "bottom-right", "show_avatar": true}',
        )
        whatsapp = Channel(
            organization_id=current_user.organization_id,
            channel_type="WHATSAPP",
            name="WhatsApp Support Line",
            is_enabled=False,
            config_json='{"phone_number": "+1 (555) 019-2834", "verified": true}',
        )
        db.add(webchat)
        db.add(whatsapp)
        await db.commit()
        return [webchat, whatsapp]

    return channels


@router.post("", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    data: ChannelCreate,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Connect a new communication channel."""
    channel = Channel(
        organization_id=current_user.organization_id,
        channel_type=data.channel_type,
        name=data.name,
        is_enabled=data.is_enabled,
        config_json=data.config_json,
        webhook_secret=data.webhook_secret,
    )
    db.add(channel)
    await db.commit()
    await db.refresh(channel)
    return channel


@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: str,
    data: ChannelUpdate,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Update channel status and credentials."""
    stmt = select(Channel).where(Channel.id == channel_id, Channel.organization_id == current_user.organization_id)
    res = await db.execute(stmt)
    channel = res.scalar_one_or_none()
    if not channel:
        raise NotFoundError("Channel", channel_id)

    if data.name is not None:
        channel.name = data.name
    if data.is_enabled is not None:
        channel.is_enabled = data.is_enabled
    if data.config_json is not None:
        channel.config_json = data.config_json
    if data.webhook_secret is not None:
        channel.webhook_secret = data.webhook_secret

    await db.commit()
    await db.refresh(channel)
    return channel
