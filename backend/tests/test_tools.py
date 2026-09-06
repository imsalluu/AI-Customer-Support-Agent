import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.models.tenant import Organization
from app.schemas.commerce import OrderCreate, OrderItemCreate, ProductCreate
from app.services.commerce_service import CommerceService
from app.tools.implementations import (
    tool_check_inventory,
    tool_check_shipping,
    tool_create_support_ticket,
    tool_get_order_status,
    tool_get_product,
    tool_request_human_agent,
    tool_search_customer,
    tool_search_products,
)


@pytest.mark.asyncio
async def test_order_and_inventory_tools(db_session: AsyncSession, test_org: Organization):
    # Create product
    prod = await CommerceService.create_product(
        db_session,
        test_org.id,
        ProductCreate(sku="SKU-TEST-99", title="Wireless Mouse", category="Electronics", price=49.99, inventory_count=25),
    )

    # Create customer
    cust = Customer(organization_id=test_org.id, name="John Doe", email="john@example.com")
    db_session.add(cust)
    await db_session.commit()
    await db_session.refresh(cust)

    # Create order
    order = await CommerceService.create_order(
        db_session,
        test_org.id,
        OrderCreate(
            customer_id=cust.id,
            order_number="ORD-88221",
            status="IN_TRANSIT",
            total_amount=49.99,
            carrier="FedEx",
            tracking_number="FDX-112233",
            shipping_address="100 Main St",
            items=[OrderItemCreate(product_id=prod.id, sku=prod.sku, title=prod.title, quantity=1, unit_price=49.99)],
        ),
    )

    # Test tool_get_order_status
    res_order = await tool_get_order_status(db_session, test_org.id, "ORD-88221")
    assert res_order["found"] is True
    assert res_order["status"] == "IN_TRANSIT"
    assert res_order["carrier"] == "FedEx"
    assert len(res_order["items"]) == 1

    # Test tool_check_inventory
    res_inv = await tool_check_inventory(db_session, test_org.id, "SKU-TEST-99")
    assert res_inv["inventory_count"] == 25
    assert res_inv["is_available"] is True

    # Test tool_search_customer
    res_cust = await tool_search_customer(db_session, test_org.id, "john@example.com")
    assert res_cust["count"] == 1
    assert res_cust["customers"][0]["name"] == "John Doe"

    # Test tool_create_support_ticket
    res_tck = await tool_create_support_ticket(
        db_session,
        test_org.id,
        customer_id=cust.id,
        subject="Missing item in shipment",
        description="I only received half of the order.",
        priority="HIGH",
        category="SHIPPING",
    )
    assert res_tck["success"] is True
    assert res_tck["ticket_number"].startswith("TCK-")

    # Test tool_request_human_agent
    res_handoff = await tool_request_human_agent(db_session, test_org.id, reason="Customer request")
    assert res_handoff["escalated"] is True
