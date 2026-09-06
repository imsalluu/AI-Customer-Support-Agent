from typing import Callable, List, Optional
from fastapi import Depends, Header, HTTPException, Query, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.constants import Role
from app.core.database import get_db
from app.core.exceptions import AuthenticationError, NotFoundError, PermissionDeniedError
from app.core.security import decode_token
from app.core.tenant import set_current_tenant_id
from app.models.tenant import Organization, User

security = HTTPBearer(auto_error=False)


async def get_current_user(
    auth: Optional[HTTPAuthorizationCredentials] = Security(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Validate bearer token, load user, and bind current tenant context."""
    if not auth or not auth.credentials:
        raise AuthenticationError("Authorization header with Bearer token is required")

    try:
        payload = decode_token(auth.credentials)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if not user_id or token_type != "access":
            raise AuthenticationError("Invalid access token")
    except JWTError:
        raise AuthenticationError("Could not validate credentials / expired token")

    query = select(User).where(User.id == user_id, User.is_active.is_(True))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise AuthenticationError("User not found or inactive")

    # Set tenant context variable for isolation
    set_current_tenant_id(user.organization_id)
    return user


def require_roles(*allowed_roles: Role) -> Callable:
    """RBAC dependency to enforce permitted roles."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        allowed_role_values = [r.value for r in allowed_roles]
        if current_user.role not in allowed_role_values and current_user.role != Role.OWNER.value:
            raise PermissionDeniedError(
                f"Role '{current_user.role}' is not authorized. Required: {', '.join(allowed_role_values)}"
            )
        return current_user

    return role_checker


async def get_api_key_organization(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
    api_key: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Organization:
    """Validate public widget API key and bind tenant context."""
    key = x_api_key or api_key
    if not key:
        raise AuthenticationError("API Key required via 'X-API-Key' header or 'api_key' query parameter")

    query = select(Organization).where(Organization.api_key == key, Organization.is_active.is_(True))
    result = await db.execute(query)
    org = result.scalar_one_or_none()

    if not org:
        raise AuthenticationError("Invalid or inactive API Key")

    set_current_tenant_id(org.id)
    return org
