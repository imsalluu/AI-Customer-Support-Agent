import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.engine import SupportAgentEngine
from app.agents.intent_sentiment import IntentSentimentClassifier
from app.core.constants import IntentType, SentimentType
from app.models.customer import Customer
from app.models.tenant import Organization
from app.schemas.commerce import OrderCreate, OrderItemCreate, ProductCreate
from app.services.commerce_service import CommerceService


def test_intent_and_sentiment_classification():
    # Order Status Intent
    intent1 = IntentSentimentClassifier.classify_intent("Where is my order ORD-10023?")
    assert intent1 == IntentType.ORDER_STATUS.value

    # Angry Sentiment
    sent_angry = IntentSentimentClassifier.analyze_sentiment("This is ridiculous, worst service ever, I am furious!")
    assert sent_angry == SentimentType.ANGRY.value

    # Positive Sentiment
    sent_pos = IntentSentimentClassifier.analyze_sentiment("Thank you so much, this is great!")
    assert sent_pos == SentimentType.POSITIVE.value

    # Entity Extraction
    entities = IntentSentimentClassifier.extract_entities("Track my package ORD-5544 please")
    assert entities["order_number"] == "ORD-5544"


@pytest.mark.asyncio
async def test_agent_engine_operational_grounding(db_session: AsyncSession, test_org: Organization):
    # Create product and order
    prod = await CommerceService.create_product(
        db_session,
        test_org.id,
        ProductCreate(sku="SKU-PRO-1", title="Studio Monitor", category="Audio", price=199.0, inventory_count=10),
    )
    cust = Customer(organization_id=test_org.id, name="Sarah Connor", email="sarah@resistance.com")
    db_session.add(cust)
    await db_session.commit()
    await db_session.refresh(cust)

    await CommerceService.create_order(
        db_session,
        test_org.id,
        OrderCreate(
            customer_id=cust.id,
            order_number="ORD-99112",
            status="SHIPPED",
            total_amount=199.0,
            carrier="FedEx",
            tracking_number="FDX-777",
            items=[OrderItemCreate(product_id=prod.id, sku=prod.sku, title=prod.title, quantity=1, unit_price=199.0)],
        ),
    )

    # Process order status inquiry through Agent
    result = await SupportAgentEngine.process_message(
        db=db_session,
        org_id=test_org.id,
        customer=cust,
        conversation_id="conv_test_1",
        message_text="Where is my order ORD-99112?",
        conversation_history=[],
    )

    assert result.intent == IntentType.ORDER_STATUS.value
    assert len(result.tool_executions) == 1
    assert result.tool_executions[0].tool_name == "get_order_status"
    assert "ORD-99112" in result.response_text
    assert "SHIPPED" in result.response_text
    assert result.confidence >= 0.75
