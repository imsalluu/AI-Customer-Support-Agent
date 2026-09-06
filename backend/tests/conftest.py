import asyncio
import os
from typing import AsyncGenerator
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.database import Base, get_db
from app.core.security import create_access_token, get_password_hash
from app.main import app
from app.models.agent_config import AgentConfig
from app.models.billing import Subscription
from app.models.tenant import Organization, User

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestAsyncSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_org(db_session: AsyncSession) -> Organization:
    org = Organization(
        name="Test Corp",
        slug="test-corp",
        api_key="spiq_test_key_12345",
        plan="BUSINESS",
        is_active=True,
    )
    db_session.add(org)
    await db_session.flush()

    user = User(
        organization_id=org.id,
        email="admin@testcorp.com",
        hashed_password=get_password_hash("password123"),
        full_name="Admin Test",
        role="OWNER",
        is_active=True,
    )
    db_session.add(user)

    agent_cfg = AgentConfig(
        organization_id=org.id,
        name="Test Assistant",
        tone="PROFESSIONAL",
        personality_prompt="You are a helpful assistant.",
        confidence_threshold=0.75,
        is_active=True,
    )
    db_session.add(agent_cfg)

    sub = Subscription(
        organization_id=org.id,
        plan="BUSINESS",
        max_monthly_messages=5000,
        max_knowledge_docs=20,
        max_agents=5,
        is_active=True,
    )
    db_session.add(sub)

    await db_session.commit()
    await db_session.refresh(org)
    return org


@pytest_asyncio.fixture(scope="function")
async def auth_headers(db_session: AsyncSession, test_org: Organization) -> dict:
    user_stmt = select(User).where(User.organization_id == test_org.id)
    res = await db_session.execute(user_stmt)
    user = res.scalar_one()

    token = create_access_token(
        subject=user.id,
        claims={"org_id": test_org.id, "role": user.role, "email": user.email},
    )
    return {"Authorization": f"Bearer {token}"}
