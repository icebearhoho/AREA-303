"""Standard API response envelope: {success, data, meta, error}.

Every JSON response from the API conforms to one of these shapes:

Success:
    {"success": true,  "data": ..., "meta": {...}, "error": null}

Failure:
    {"success": false, "data": null, "meta": {...}, "error": {"code": ..., "message": ..., "details": {...}}}
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ErrorPayload(BaseModel):
    code: str = Field(..., description="Stable machine-readable error code, e.g. RESOURCE_NOT_FOUND")
    message: str = Field(..., description="Human-readable summary")
    details: dict[str, Any] = Field(default_factory=dict)


class PageMeta(BaseModel):
    request_id: str | None = None
    page: int | None = None
    page_size: int | None = None
    total: int | None = None


class ApiResponse(BaseModel, Generic[T]):
    """The universal API envelope."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    data: T | None = None
    meta: PageMeta | None = None
    error: ErrorPayload | None = None


def make_response(
    *,
    data: Any = None,
    meta: PageMeta | None = None,
    error: ErrorPayload | None = None,
) -> dict[str, Any]:
    """Build a raw envelope dict. The endpoint can return this directly,
    or — preferred — return the typed ``ApiResponse[T]``.
    """
    return {
        "success": error is None,
        "data": data,
        "meta": meta.model_dump() if meta else None,
        "error": error.model_dump() if error else None,
    }
