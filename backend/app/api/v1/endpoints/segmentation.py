"""#13 Customer Segmentation — predict a user's persona from behavioural features."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.responses import ApiResponse, PageMeta
from app.schemas.segmentation import SegmentationRequest
from app.services import segmentation as service

router = APIRouter()


@router.post("/", response_model=ApiResponse[dict])
async def predict(req: SegmentationRequest) -> ApiResponse[dict]:
    """Dự đoán persona (1 trong 4 nhóm) cho 1 user từ 14 feature hành vi."""
    data = service.predict_persona(req)
    return ApiResponse[dict](
        success=True,
        data=data.model_dump(),
        meta=PageMeta(),
        error=None,
    )
