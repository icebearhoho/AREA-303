"""#14 AI Negotiation Bot cho B2B."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.negotiation import NegotiationRequest
from app.services import negotiation as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def negotiate(req: NegotiationRequest) -> ApiResponse[dict]:
    data = service.negotiate(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
