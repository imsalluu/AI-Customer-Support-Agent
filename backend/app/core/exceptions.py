from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthenticationError(AppException):
    def __init__(self, detail: str = "Invalid authentication credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class PermissionDeniedError(AppException):
    def __init__(self, detail: str = "Permission denied for this operation"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource", identifier: Any = None):
        detail = f"{resource} not found"
        if identifier:
            detail = f"{resource} '{identifier}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class TenantMismatchError(AppException):
    def __init__(self, detail: str = "Cross-tenant access prohibited"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class QuotaExceededError(AppException):
    def __init__(self, detail: str = "Organization subscription quota exceeded"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
        )


class ToolExecutionError(AppException):
    def __init__(self, tool_name: str, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error executing tool '{tool_name}': {detail}",
        )
