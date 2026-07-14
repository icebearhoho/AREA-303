"""Auth: login (issue token) + me (verify token). Skeleton only."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.core.responses import ApiResponse, PageMeta

router = APIRouter()


@router.post("/login", response_model=ApiResponse[dict])
async def login() -> ApiResponse[dict]:
    # TODO: validate credentials, call create_access_token()
    return ApiResponse[dict](
        success=True,
        data={"access_token": "REPLACE_ME", "token_type": "bearer"},
        meta=PageMeta(),
        error=None,
    )


@router.get("/me", response_model=ApiResponse[dict])
async def me(user=Depends(get_current_user)) -> ApiResponse[dict]:
    return ApiResponse[dict](
        success=True,
        data={"user": user},
        meta=PageMeta(),
        error=None,
    )
