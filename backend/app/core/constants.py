from enum import Enum


class Role(str, Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    SUPPORT_AGENT = "SUPPORT_AGENT"
    VIEWER = "VIEWER"


class ConversationStatus(str, Enum):
    AI_ACTIVE = "AI_ACTIVE"
    WAITING_HUMAN = "WAITING_HUMAN"
    HUMAN_ACTIVE = "HUMAN_ACTIVE"
    RESOLVED = "RESOLVED"


class SenderType(str, Enum):
    CUSTOMER = "CUSTOMER"
    AI = "AI"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    WAITING_CUSTOMER = "WAITING_CUSTOMER"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"


class TicketCategory(str, Enum):
    ORDER_STATUS = "ORDER_STATUS"
    RETURN = "RETURN"
    REFUND = "REFUND"
    PRODUCT_INFO = "PRODUCT_INFO"
    SHIPPING = "SHIPPING"
    PAYMENT = "PAYMENT"
    ACCOUNT = "ACCOUNT"
    COMPLAINT = "COMPLAINT"
    TECHNICAL = "TECHNICAL"
    GENERAL = "GENERAL"


class IntentType(str, Enum):
    ORDER_STATUS = "ORDER_STATUS"
    RETURN = "RETURN"
    REFUND = "REFUND"
    PRODUCT_INFO = "PRODUCT_INFO"
    SHIPPING = "SHIPPING"
    PAYMENT = "PAYMENT"
    ACCOUNT = "ACCOUNT"
    COMPLAINT = "COMPLAINT"
    TECHNICAL = "TECHNICAL"
    GENERAL = "GENERAL"
    HUMAN_REQUEST = "HUMAN_REQUEST"


class SentimentType(str, Enum):
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    ANGRY = "ANGRY"


class ChannelType(str, Enum):
    WEBCHAT = "WEBCHAT"
    WHATSAPP = "WHATSAPP"
    MESSENGER = "MESSENGER"
    EMAIL = "EMAIL"


class PlanType(str, Enum):
    FREE = "FREE"
    STARTER = "STARTER"
    BUSINESS = "BUSINESS"
    ENTERPRISE = "ENTERPRISE"


class AgentTone(str, Enum):
    PROFESSIONAL = "PROFESSIONAL"
    EMPATHETIC = "EMPATHETIC"
    CASUAL = "CASUAL"
    DIRECT = "DIRECT"
