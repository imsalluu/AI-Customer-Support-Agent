from typing import Any, Dict, Optional
from app.channels.base import ChannelProvider, NormalizedInboundMessage
from app.core.constants import ChannelType


class MessengerProvider(ChannelProvider):
    async def verify_webhook(self, headers: Dict[str, str], body: bytes, params: Dict[str, Any]) -> bool:
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        return mode == "subscribe" and token == "supportiq_messenger_verify"

    async def parse_inbound_message(self, payload: Dict[str, Any]) -> Optional[NormalizedInboundMessage]:
        try:
            entry = payload.get("entry", [])[0]
            messaging = entry.get("messaging", [])[0]
            sender_id = messaging.get("sender", {}).get("id")
            message = messaging.get("message", {})
            text = message.get("text", "")
            if not text:
                return None

            return NormalizedInboundMessage(
                sender_id=sender_id,
                sender_name="Messenger User",
                content=text,
                channel_type=ChannelType.MESSENGER.value,
                metadata={"mid": message.get("mid")},
            )
        except Exception:
            return None

    async def send_outbound_message(self, recipient_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        return True


class EmailProvider(ChannelProvider):
    async def verify_webhook(self, headers: Dict[str, str], body: bytes, params: Dict[str, Any]) -> bool:
        return True

    async def parse_inbound_message(self, payload: Dict[str, Any]) -> Optional[NormalizedInboundMessage]:
        try:
            sender_email = payload.get("from_email") or payload.get("from")
            subject = payload.get("subject", "")
            body_text = payload.get("body_text") or payload.get("text", "")
            full_content = f"Subject: {subject}\n\n{body_text}".strip()

            return NormalizedInboundMessage(
                sender_id=sender_email,
                sender_name=payload.get("from_name", "Email Customer"),
                sender_email=sender_email,
                content=full_content,
                channel_type=ChannelType.EMAIL.value,
                metadata={"subject": subject},
            )
        except Exception:
            return None

    async def send_outbound_message(self, recipient_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        return True
