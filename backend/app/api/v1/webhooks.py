from typing import Any, Dict
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.channels.whatsapp import WhatsAppProvider
from app.core.database import get_db
from app.models.tenant import Organization
from app.schemas.conversation import ConversationCreate
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/webhooks", tags=["Channel Webhooks"])


@router.get("/whatsapp")
async def verify_whatsapp_webhook(
    request: Request,
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
):
    """Meta WhatsApp Webhook Verification handshake."""
    provider = WhatsAppProvider()
    verified = await provider.verify_webhook(
        headers=dict(request.headers),
        body=b"",
        params={"hub.mode": hub_mode, "hub.verify_token": hub_verify_token},
    )
    if verified and hub_challenge:
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@router.post("/whatsapp")
async def handle_whatsapp_webhook(
    payload: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
):
    """Handle incoming WhatsApp messages from Meta Cloud API."""
    provider = WhatsAppProvider()
    inbound = await provider.parse_inbound_message(payload)
    if not inbound:
        return {"status": "ignored"}

    # Match or find organization
    stmt = select(Organization).where(Organization.is_active.is_(True)).limit(1)
    res = await db.execute(stmt)
    org = res.scalar_one_or_none()
    if not org:
        return {"status": "no_active_org"}

    conv_create = ConversationCreate(
        customer_name=inbound.sender_name or "WhatsApp User",
        customer_phone=inbound.sender_phone,
        channel="WHATSAPP",
    )
    conv, customer, _ = await ConversationService.create_or_get_conversation(db, org.id, conv_create)

    # Process message through AI Agent
    conv, cust_msg, ai_msg = await ConversationService.process_customer_message(
        db, org.id, conv.id, inbound.content
    )

    if ai_msg:
        # Dispatch WhatsApp reply
        await provider.send_outbound_message(inbound.sender_id, ai_msg.content)

    return {"status": "processed", "conversation_id": conv.id}
