"""Track 2, Đề 1 — Product Knowledge (causal sales explanation)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.knowledge import ProductKnowledgeRequest
from app.services import knowledge as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def explain(req: ProductKnowledgeRequest) -> ApiResponse[dict]:
    data = await service.explain_sales(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
