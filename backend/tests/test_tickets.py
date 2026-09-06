import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from app.models.tenant import Organization


@pytest.mark.asyncio
async def test_ticket_lifecycle_api(client: AsyncClient, db_session: AsyncSession, test_org: Organization, auth_headers: dict):
    cust = Customer(organization_id=test_org.id, name="Emily Blunt", email="emily@example.com")
    db_session.add(cust)
    await db_session.commit()
    await db_session.refresh(cust)

    # 1. Create Ticket
    create_payload = {
        "customer_id": cust.id,
        "subject": "Damaged parcel upon delivery",
        "description": "The box arrived crushed and the screen is cracked.",
        "priority": "HIGH",
        "category": "COMPLAINT",
    }
    res = await client.post("/api/v1/tickets", json=create_payload, headers=auth_headers)
    assert res.status_code == 201
    ticket_data = res.json()
    ticket_id = ticket_data["id"]
    assert ticket_data["status"] == "OPEN"
    assert ticket_data["priority"] == "HIGH"
    assert ticket_data["ticket_number"].startswith("TCK-")

    # 2. Update Ticket to RESOLVED
    update_payload = {
        "status": "RESOLVED",
        "resolution_notes": "Shipped a brand new replacement via FedEx overnight.",
    }
    res_up = await client.put(f"/api/v1/tickets/{ticket_id}", json=update_payload, headers=auth_headers)
    assert res_up.status_code == 200
    assert res_up.json()["status"] == "RESOLVED"
    assert res_up.json()["resolved_at"] is not None

    # 3. Check stats
    res_stats = await client.get("/api/v1/tickets/stats/summary", headers=auth_headers)
    assert res_stats.status_code == 200
    assert res_stats.json()["resolved"] == 1
