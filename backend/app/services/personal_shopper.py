"""Personal Shopper service — RAG + LLM with SSE-friendly streaming."""

from __future__ import annotations

from app.core.exceptions import ValidationError
from app.core.logging import get_logger
from app.schemas.genai import ProductCard, ShopperProductsResponse
from app.services.genai import (
    PERSONAL_SHOPPER_SYSTEM,
    llm_cache,
)
from app.services.genai.base import LlmMessage
from app.services.genai.demo_data import (
    DEMO_CATALOG,
    SHOPPER_DEMO_PRODUCT_IDS,
    SHOPPER_DEMO_REPLY,
)
from app.services.genai.factory import get_llm_client, get_rag

log = get_logger("app.services.shopper")

_PRODUCT_INDEX = {p["id"]: p for p in DEMO_CATALOG}


def _build_context_block(docs: list) -> str:
    """Render retrieved docs as a compact context block."""
    lines = ["CONTEXT (từ catalog nội bộ):"]
    for i, d in enumerate(docs, start=1):
        meta = d.metadata or {}
        lines.append(
            f"{i}. [{d.id}] {d.title} — {meta.get('category', '?')} · "
            f"{meta.get('platform', '?')} · {meta.get('price_vnd', 0):,}₫\n   {d.text}"
        )
    return "\n".join(lines)


@llm_cache(prefix="shopper_products")
async def _retrieve_products(query: str, top_k: int) -> ShopperProductsResponse:
    """Top-k product cards + the retrieved doc metadata."""
    rag = get_rag()
    docs = await rag.retrieve(query, top_k=top_k)
    products: list[ProductCard] = []
    for d in docs:
        item = _PRODUCT_INDEX.get(d.id)
        if item is None:
            continue
        meta = item.get("metadata", {})
        products.append(
            ProductCard(
                id=item["id"],
                name=item["title"],
                brand=meta.get("brand", "OEM"),
                category=meta.get("category", "Thời trang"),
                platform=meta.get("platform", "Shopee"),
                price_vnd=meta.get("price_vnd", 0),
                rating=4.5,
                reviews=0,
                similarity=d.score,
                image_hue=200 + (hash(item["id"]) % 160),
            )
        )

    if not products:
        # Always return something — fall back to demo picks.
        for pid in SHOPPER_DEMO_PRODUCT_IDS[:top_k]:
            item = _PRODUCT_INDEX[pid]
            meta = item.get("metadata", {})
            products.append(
                ProductCard(
                    id=item["id"],
                    name=item["title"],
                    brand=meta.get("brand", "OEM"),
                    category=meta.get("category", "Thời trang"),
                    platform=meta.get("platform", "Shopee"),
                    price_vnd=meta.get("price_vnd", 0),
                    rating=4.5,
                    reviews=0,
                    similarity=0.5,
                    image_hue=200 + (hash(item["id"]) % 160),
                )
            )

    return ShopperProductsResponse(
        products=products,
        sources=[
            {"id": d.id, "title": d.title, "score": d.score} for d in docs
        ],
    )


async def stream_reply(query: str, top_k: int = 4):
    """Yield ChatChunk objects for the SSE endpoint."""
    if not query.strip():
        raise ValidationError("query must not be empty")

    # Warm the product cache so /products endpoint is hot by the
    # time the user reads the streamed reply.
    await _retrieve_products(query, top_k)
    rag = get_rag()
    docs = await rag.retrieve(query, top_k=top_k)

    llm = get_llm_client()
    messages = [
        LlmMessage(role="system", content=PERSONAL_SHOPPER_SYSTEM),
        LlmMessage(role="user", content=f"{_build_context_block(docs)}\n\nUser: {query}"),
    ]

    async for chunk in llm.stream(messages, temperature=0.6):
        yield chunk


async def products_for(query: str, top_k: int = 4) -> ShopperProductsResponse:
    return await _retrieve_products(query, top_k)


def demo_reply() -> tuple[str, list[str]]:
    """Pure fallback for the absolute worst case (LLM disabled, cache empty)."""
    return SHOPPER_DEMO_REPLY, SHOPPER_DEMO_PRODUCT_IDS