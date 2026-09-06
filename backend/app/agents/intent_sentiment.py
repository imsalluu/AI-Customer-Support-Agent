import re
from typing import Dict, List, Optional, Tuple
from app.core.constants import IntentType, SentimentType


class IntentSentimentClassifier:
    INTENT_PATTERNS = {
        IntentType.ORDER_STATUS.value: [
            r"where is my order",
            r"track my order",
            r"order status",
            r"package status",
            r"ord-\d+",
            r"#\d+",
            r"order #",
            r"when will my order arrive",
            r"delivery status",
        ],
        IntentType.SHIPPING.value: [
            r"shipping",
            r"delivery time",
            r"fedex",
            r"dhl",
            r"ups",
            r"tracking number",
            r"how long does shipping take",
            r"shipping cost",
            r"international shipping",
        ],
        IntentType.RETURN.value: [
            r"return",
            r"send back",
            r"exchange item",
            r"return policy",
            r"return window",
            r"rma",
        ],
        IntentType.REFUND.value: [
            r"refund",
            r"money back",
            r"charge back",
            r"cancel order",
            r"get my money",
        ],
        IntentType.PRODUCT_INFO.value: [
            r"product",
            r"price",
            r"in stock",
            r"inventory",
            r"specs",
            r"features",
            r"do you have",
            r"how much is",
            r"sku",
        ],
        IntentType.PAYMENT.value: [
            r"payment",
            r"credit card",
            r"invoice",
            r"bill",
            r"declined",
            r"paypal",
            r"apple pay",
        ],
        IntentType.ACCOUNT.value: [
            r"account",
            r"login",
            r"password",
            r"reset password",
            r"email address",
            r"profile",
        ],
        IntentType.COMPLAINT.value: [
            r"broken",
            r"damaged",
            r"wrong item",
            r"terrible",
            r"horrible",
            r"unacceptable",
            r"worst service",
            r"scam",
            r"disappointed",
        ],
        IntentType.TECHNICAL.value: [
            r"error",
            r"bug",
            r"not working",
            r"broken link",
            r"crash",
            r"failed",
            r"app not loading",
        ],
        IntentType.HUMAN_REQUEST.value: [
            r"human",
            r"agent",
            r"real person",
            r"support specialist",
            r"speak to someone",
            r"representative",
            r"manager",
        ],
    }

    ANGRY_KEYWORDS = [
        "furious", "unacceptable", "scam", "fraud", "lawyer", "lawsuit",
        "worst service", "horrible", "terrible", "ridiculous", "disaster",
        "stole my money", "garbage", "trash", "sue you", "pissed off"
    ]

    NEGATIVE_KEYWORDS = [
        "angry", "upset", "frustrated", "bad", "slow", "delay", "waiting forever",
        "broken", "damaged", "wrong", "annoyed", "poor", "issue", "problem",
        "not happy", "disappointed", "complaint"
    ]

    POSITIVE_KEYWORDS = [
        "thank", "thanks", "great", "awesome", "perfect", "helpful", "love",
        "excellent", "amazing", "good", "appreciate", "wonderful", "solved"
    ]

    @classmethod
    def classify_intent(cls, text: str) -> str:
        text_lower = text.lower()
        for intent, patterns in cls.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent
        return IntentType.GENERAL.value

    @classmethod
    def analyze_sentiment(cls, text: str) -> str:
        text_lower = text.lower()

        # Check for angry indicators
        for kw in cls.ANGRY_KEYWORDS:
            if kw in text_lower:
                return SentimentType.ANGRY.value

        # Check for all caps frustration (e.g. "I WANT MY REFUND NOW!!!")
        caps_words = [w for w in text.split() if len(w) > 2 and w.isupper()]
        if len(caps_words) >= 3 and ("!" in text or "?" in text):
            return SentimentType.ANGRY.value

        # Check for negative indicators
        for kw in cls.NEGATIVE_KEYWORDS:
            if kw in text_lower:
                return SentimentType.NEGATIVE.value

        # Check for positive indicators
        for kw in cls.POSITIVE_KEYWORDS:
            if kw in text_lower:
                return SentimentType.POSITIVE.value

        return SentimentType.NEUTRAL.value

    @classmethod
    def extract_entities(cls, text: str) -> Dict[str, Optional[str]]:
        entities: Dict[str, Optional[str]] = {
            "order_number": None,
            "email": None,
            "sku": None,
        }

        # Match Order numbers like ORD-10023, ORD10023, #10023
        order_match = re.search(r"\b(ORD-?\d+|\#\d{4,6})\b", text, re.IGNORECASE)
        if order_match:
            entities["order_number"] = order_match.group(1).upper()
            if entities["order_number"].startswith("#"):
                entities["order_number"] = "ORD-" + entities["order_number"].lstrip("#")

        # Match Email
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
        if email_match:
            entities["email"] = email_match.group(0)

        # Match SKU like SKU-990 or PROD-102
        sku_match = re.search(r"\b(SKU-[A-Z0-9]+|PROD-[A-Z0-9]+)\b", text, re.IGNORECASE)
        if sku_match:
            entities["sku"] = sku_match.group(1).upper()

        return entities
