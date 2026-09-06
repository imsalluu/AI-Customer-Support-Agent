import re
from typing import List, Optional
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import PlanType, Role
from app.core.exceptions import AuthenticationError, PermissionDeniedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_api_key,
    get_password_hash,
    verify_password,
)
from app.models.agent_config import AgentConfig
from app.models.billing import Subscription
from app.models.tenant import Organization, User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, data: RegisterRequest) -> TokenResponse:
        # Check if user email already exists
        existing_user_query = select(User).where(User.email == data.email)
        res = await db.execute(existing_user_query)
        if res.scalar_one_or_none():
            raise AuthenticationError("User with this email already exists")

        # Create Organization
        base_slug = slugify(data.organization_name)
        slug = base_slug
        counter = 1
        while True:
            org_check = await db.execute(select(Organization).where(Organization.slug == slug))
            if not org_check.scalar_one_or_none():
                break
            slug = f"{base_slug}-{counter}"
            counter += 1

        org = Organization(
            name=data.organization_name,
            slug=slug,
            api_key=generate_api_key(),
            plan=PlanType.STARTER.value,
            is_active=True,
        )
        db.add(org)
        await db.flush()

        # Create Owner User
        owner = User(
            email=data.email,
            hashed_password=get_password_hash(data.password),
            full_name=data.full_name,
            role=Role.OWNER.value,
            organization_id=org.id,
            is_active=True,
        )
        db.add(owner)

        # Initialize Default Agent Config
        agent_config = AgentConfig(
            organization_id=org.id,
            name="SupportIQ Assistant",
            tone="PROFESSIONAL",
            personality_prompt="You are a calm, highly capable, and professional customer support specialist.",
            greeting_message=f"Hello! Welcome to {org.name}. How can I assist you with orders, returns, or support today?",
            confidence_threshold=0.75,
            is_active=True,
        )
        db.add(agent_config)

        # Initialize Subscription
        sub = Subscription(
            organization_id=org.id,
            plan=PlanType.STARTER.value,
            is_active=True,
            max_monthly_messages=5000,
            max_knowledge_docs=20,
            max_agents=5,
        )
        db.add(sub)

        await db.commit()
        await db.refresh(owner)

        access_token = create_access_token(
            subject=owner.id,
            claims={"org_id": org.id, "role": owner.role, "email": owner.email},
        )
        refresh_token = create_refresh_token(subject=owner.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=owner.id,
            organization_id=org.id,
            role=owner.role,
            full_name=owner.full_name,
            email=owner.email,
        )

    @staticmethod
    async def login(db: AsyncSession, data: LoginRequest) -> TokenResponse:
        query = select(User).where(User.email == data.email)
        res = await db.execute(query)
        user = res.scalar_one_or_none()

        if not user or not verify_password(data.password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("User account is deactivated")

        access_token = create_access_token(
            subject=user.id,
            claims={"org_id": user.organization_id, "role": user.role, "email": user.email},
        )
        refresh_token = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
            full_name=user.full_name,
            email=user.email,
        )

    @staticmethod
    async def refresh_token(db: AsyncSession, refresh_token_str: str) -> TokenResponse:
        try:
            payload = decode_token(refresh_token_str)
            user_id = payload.get("sub")
            token_type = payload.get("type")
            if not user_id or token_type != "refresh":
                raise AuthenticationError("Invalid refresh token")
        except JWTError:
            raise AuthenticationError("Expired or invalid refresh token")

        query = select(User).where(User.id == user_id, User.is_active.is_(True))
        res = await db.execute(query)
        user = res.scalar_one_or_none()

        if not user:
            raise AuthenticationError("User not found")

        access_token = create_access_token(
            subject=user.id,
            claims={"org_id": user.organization_id, "role": user.role, "email": user.email},
        )
        new_refresh_token = create_refresh_token(subject=user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
            full_name=user.full_name,
            email=user.email,
        )

    @staticmethod
    async def regenerate_api_key(db: AsyncSession, org_id: str) -> str:
        query = select(Organization).where(Organization.id == org_id)
        res = await db.execute(query)
        org = res.scalar_one_or_none()
        if not org:
            raise AuthenticationError("Organization not found")

        new_key = generate_api_key()
        org.api_key = new_key
        await db.commit()
        return new_key
