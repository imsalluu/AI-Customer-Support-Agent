from typing import Any, Dict, Optional
import httpx
from app.channels.base import ChannelProvider, NormalizedInboundMessage
from app.core.config import settings
from app.core.constants import ChannelType


class WhatsAppProvider(ChannelProvider):
    def __init__(self, api_token: Optional[str] = None, phone_number_id: Optional[str] = None, verify_token: Optional[str] = None):
        self.api_token = api_token or settings.WHATSAPP_API_TOKEN
        self.phone_number_id = phone_number_id or settings.WHATSAPP_PHONE_NUMBER_ID
        self.verify_token = verify_token or settings.WHATSAPP_VERIFY_TOKEN

    async def verify_webhook(self, headers: Dict[str, str], body: bytes, params: Dict[str, Any]) -> bool:
        mode = params.get("hub.mode")
        token = params.get("hub.verify_token")
        return mode == "subscribe" and token == self.verify_token

    async def parse_inbound_message(self, payload: Dict[str, Any]) -> Optional[NormalizedInboundMessage]:
        try:
            entry = payload.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            if not messages:
                return None

            msg = messages[0]
            contacts = value.get("contacts", [])
            sender_name = contacts[0].get("profile", {}).get("name", "WhatsApp User") if contacts else "WhatsApp User"
            from_phone = msg.get("from")

            text_content = ""
            if msg.get("type") == "text":
                text_content = msg.get("text", {}).get("body", "")
            elif msg.get("type") == "button":
                text_content = msg.get("button", {}).get("text", "")
            elif msg.get("type") == "interactive":
                text_content = (
                    msg.get("interactive", {}).get("button_reply", {}).get("title")
                    or msg.get("interactive", {}).get("list_reply", {}).get("title", "")
                )

            if not text_content:
                return None

            return NormalizedInboundMessage(
                sender_id=from_phone,
                sender_name=sender_name,
                sender_phone=from_phone,
                content=text_content,
                channel_type=ChannelType.WHATSAPP.value,
                metadata={"whatsapp_message_id": msg.get("id"), "raw": msg},
            )
        except Exception:
            return None

    async def send_outbound_message(self, recipient_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        if not self.api_token or not self.phone_number_id:
            # Fallback for dev / mock
            return True

        url = f"https://graph.facebook.com/v19.0/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": content},
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                return res.status_code == 200
        except Exception:
            return False
