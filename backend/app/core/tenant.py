from contextvars import ContextVar
from typing import Optional
from app.core.exceptions import TenantMismatchError

_current_tenant_id: ContextVar[Optional[str]] = ContextVar("current_tenant_id", default=None)


def set_current_tenant_id(tenant_id: Optional[str]) -> None:
    _current_tenant_id.set(tenant_id)


def get_current_tenant_id() -> Optional[str]:
    return _current_tenant_id.get()


def validate_tenant_access(target_tenant_id: str) -> None:
    current = get_current_tenant_id()
    if current and current != target_tenant_id:
        raise TenantMismatchError(
            f"Access denied: current tenant '{current}' cannot access resource in tenant '{target_tenant_id}'"
        )
