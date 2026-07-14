"""Datasets endpoints: list datasets under dataset/by_idea and dataset/processed."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Query

from app.core.responses import ApiResponse, PageMeta

router = APIRouter()


def _find_dataset_root() -> Path | None:
    # backend/app/api/v1/endpoints/datasets.py -> repo root has /dataset
    candidate = Path(__file__).resolve().parents[4] / "dataset"
    return candidate if candidate.exists() else None


@router.get("/", response_model=ApiResponse[list[dict]])
async def list_datasets(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> ApiResponse[list[dict]]:
    root = _find_dataset_root()
    if root is None:
        return ApiResponse[list[dict]](
            success=True, data=[],
            meta=PageMeta(page=page, page_size=page_size, total=0), error=None,
        )

    by_idea = root / "by_idea"
    items: list[dict] = []
    if by_idea.exists():
        for child in sorted(by_idea.iterdir()):
            if child.is_dir():
                items.append({"idea_slug": child.name, "path": str(child.relative_to(root))})

    total = len(items)
    start, end = (page - 1) * page_size, page * page_size
    return ApiResponse[list[dict]](
        success=True,
        data=items[start:end],
        meta=PageMeta(page=page, page_size=page_size, total=total),
        error=None,
    )
