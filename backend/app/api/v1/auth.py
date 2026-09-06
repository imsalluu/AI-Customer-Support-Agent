from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user, require_roles
from app.core.constants import Role
from app.core.database import get_db
from app.core.security import get_password_hash
from app.models.tenant import Organization, User
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.tenant import ApiKeyRegenerateResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    """Register a new SaaS Organization and its Owner user."""
    return await AuthService.register(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Authenticate a user and return JWT tokens."""
    return await AuthService.login(db, data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(data: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Refresh an expired access token using a valid refresh token."""
    return await AuthService.refresh_token(db, data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user profile."""
    return current_user


@router.post("/api-key/regenerate", response_model=ApiKeyRegenerateResponse)
async def regenerate_api_key(
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Regenerate the organization's public API Key for widget embeds."""
    new_key = await AuthService.regenerate_api_key(db, current_user.organization_id)
    return ApiKeyRegenerateResponse(api_key=new_key, organization_id=current_user.organization_id)


@router.get("/members", response_model=List[UserResponse])
async def list_members(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List team members in the current organization."""
    query = select(User).where(User.organization_id == current_user.organization_id)
    res = await db.execute(query)
    return res.scalars().all()


@router.post("/members", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_member(
    data: RegisterRequest,
    current_user: User = Depends(require_roles(Role.OWNER, Role.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Add a new support agent or admin to the organization."""
    new_member = User(
        email=data.email,
        hashed_password=get_password_hash(data.password),
        full_name=data.full_name,
        role=Role.SUPPORT_AGENT.value,
        organization_id=current_user.organization_id,
        is_active=True,
    )
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)
    return new_member
