"""Cross-cutting concerns: config, security, response envelope, exceptions."""

from app.core.config import settings
from app.core.exceptions import (
    AppError,
    ErrorCode,
    register_exception_handlers,
)
from app.core.responses import (
    ApiResponse,
    PageMeta,
    make_response,
)

__all__ = [
    "settings",
    "AppError",
    "ErrorCode",
    "register_exception_handlers",
    "ApiResponse",
    "PageMeta",
    "make_response",
]
