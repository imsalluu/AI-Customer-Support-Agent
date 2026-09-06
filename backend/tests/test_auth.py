import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_organization_and_user(client: AsyncClient):
    payload = {
        "email": "newowner@enterprise.com",
        "password": "secretpassword123",
        "full_name": "Jane Doe",
        "organization_name": "Enterprise SaaS Solutions",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["email"] == "newowner@enterprise.com"
    assert data["role"] == "OWNER"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_org):
    payload = {
        "email": "admin@testcorp.com",
        "password": "password123",
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "OWNER"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, test_org):
    payload = {
        "email": "admin@testcorp.com",
        "password": "wrong_password",
    }
    response = await client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@testcorp.com"
