"""#08 Sentiment-driven Inventory Alert — social buzz vs stock runway (seller insight)."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.insights import InventoryAlertRequest
from app.services import insights

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def check(req: InventoryAlertRequest) -> ApiResponse[dict]:
    data = insights.score_inventory_alert(req)
    return ApiResponse[dict](success=True, data=data.model_dump(), meta=PageMeta(), error=None)
