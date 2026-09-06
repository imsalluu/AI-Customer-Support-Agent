from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel


class NormalizedInboundMessage(BaseModel):
    sender_id: str
    sender_name: Optional[str] = "Customer"
    sender_email: Optional[str] = None
    sender_phone: Optional[str] = None
    content: str
    channel_type: str
    metadata: Dict[str, Any] = {}


class ChannelProvider(ABC):
    @abstractmethod
    async def verify_webhook(self, headers: Dict[str, str], body: bytes, params: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def parse_inbound_message(self, payload: Dict[str, Any]) -> Optional[NormalizedInboundMessage]:
        pass

    @abstractmethod
    async def send_outbound_message(self, recipient_id: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        pass
