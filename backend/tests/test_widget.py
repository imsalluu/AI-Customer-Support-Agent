import pytest
from httpx import AsyncClient
from app.models.tenant import Organization


@pytest.mark.asyncio
async def test_public_chat_widget_flow(client: AsyncClient, test_org: Organization):
    # 1. Initialize Widget with public API Key
    init_res = await client.post(
        "/api/v1/widget/init",
        headers={"X-API-Key": test_org.api_key},
        json={"customer_name": "Web Shopper", "customer_email": "shopper@test.com"},
    )
    assert init_res.status_code == 200
    init_data = init_res.json()
    conv_id = init_data["conversation_id"]
    assert init_data["organization_name"] == test_org.name
    assert init_data["status"] == "AI_ACTIVE"

    # 2. Send Customer Message from Widget
    send_res = await client.post(
        "/api/v1/widget/send",
        headers={"X-API-Key": test_org.api_key},
        json={"conversation_id": conv_id, "message": "Hi, what is your return policy?"},
    )
    assert send_res.status_code == 200
    send_data = send_res.json()
    assert send_data["conversation_id"] == conv_id
    assert send_data["ai_response"] is not None
    assert send_data["status"] in ["AI_ACTIVE", "WAITING_HUMAN"]

    # 3. Submit CSAT rating
    fb_res = await client.post(
        "/api/v1/widget/feedback",
        headers={"X-API-Key": test_org.api_key},
        json={"conversation_id": conv_id, "rating": 5, "comment": "Great assistance!"},
    )
    assert fb_res.status_code == 201
    assert fb_res.json()["success"] is True
