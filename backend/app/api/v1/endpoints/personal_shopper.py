"""#03 Personal Shopper — SSE streaming endpoint + product retrieval."""

from __future__ import annotations

from fastapi import APIRouter
from starlette.responses import Response

from app.core.responses import ApiResponse, PageMeta
from app.core.sse import SseResponse, stream_chunks
from app.schemas.genai import ShopperRequest
from app.services import personal_shopper as service

router = APIRouter()


@router.post("/", response_model=None)
async def chat(req: ShopperRequest) -> Response:
    """Stream the assistant reply as Server-Sent Events.

    Each event frame is JSON ``{"delta": "...", "finish_reason": null}``.
    The final frame is ``{"done": true, "meta": {...}}``.
    """
    chunks = service.stream_reply(req.query, top_k=req.top_k)
    body = stream_chunks(
        chunks,
        on_done={"query": req.query, "top_k": req.top_k},
    )
    return SseResponse(body)


@router.get("/products", response_model=ApiResponse[dict])
async def products(query: str, top_k: int = 4) -> ApiResponse[dict]:
    """Return the recommended product cards for a query (no LLM stream)."""
    data = await service.products_for(query=query, top_k=top_k)
    return ApiResponse[dict](
        success=True,
        data=data.model_dump(),
        meta=PageMeta(),
        error=None,
    )