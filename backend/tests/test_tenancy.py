import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, get_password_hash
from app.models.customer import Customer
from app.models.tenant import Organization, User


@pytest.mark.asyncio
async def test_tenant_data_isolation(client: AsyncClient, db_session: AsyncSession, test_org: Organization, auth_headers: dict):
    # Create Organization B
    org_b = Organization(name="Company B", slug="company-b", api_key="spiq_key_b", plan="STARTER")
    db_session.add(org_b)
    await db_session.flush()

    user_b = User(
        organization_id=org_b.id,
        email="userb@companyb.com",
        hashed_password=get_password_hash("password123"),
        full_name="User B",
        role="OWNER",
        is_active=True,
    )
    db_session.add(user_b)

    # Customer in Org A
    cust_a = Customer(organization_id=test_org.id, name="Alice Org A", email="alice@orga.com")
    # Customer in Org B
    cust_b = Customer(organization_id=org_b.id, name="Bob Org B", email="bob@orgb.com")
    db_session.add_all([cust_a, cust_b])
    await db_session.commit()

    # Query with Org A Auth
    res_a = await client.get("/api/v1/customers", headers=auth_headers)
    assert res_a.status_code == 200
    names_a = [c["name"] for c in res_a.json()]
    assert "Alice Org A" in names_a
    assert "Bob Org B" not in names_a  # Strict isolation verified!

    # Attempt to fetch Org B customer using Org A auth
    res_cross = await client.get(f"/api/v1/customers/{cust_b.id}", headers=auth_headers)
    assert res_cross.status_code == 404
