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


def _card(item: dict, score: float) -> ProductCard:
    meta = item.get("metadata", {})
    return ProductCard(
        id=item["id"],
        name=item["title"],
        brand=meta.get("brand", "OEM"),
        category=meta.get("category", "Thời trang"),
        platform=meta.get("platform", "Shopee"),
        price_vnd=meta.get("price_vnd", 0),
        rating=round(4.0 + (hash(item["id"]) % 10) / 10, 1),
        reviews=120 + (hash(item["id"]) % 4000),
        similarity=score,
        image_hue=200 + (hash(item["id"]) % 160),
    )


@llm_cache(prefix="shopper_products")
async def _retrieve_products(query: str, top_k: int) -> ShopperProductsResponse:
    """Top-k product cards + retrieved doc metadata. Always returns up to top_k
    by padding from the catalog so the UI shows a full set of suggestions."""
    rag = get_rag()
    docs = await rag.retrieve(query, top_k=top_k)

    products: list[ProductCard] = []
    seen: set[str] = set()
    for d in docs:
        item = _PRODUCT_INDEX.get(d.id)
        if item is None or item["id"] in seen:
            continue
        products.append(_card(item, d.score))
        seen.add(item["id"])

    # Pad to top_k from the rest of the catalog (demo picks first, then any).
    if len(products) < top_k:
        order = SHOPPER_DEMO_PRODUCT_IDS + [p["id"] for p in DEMO_CATALOG]
        for pid in order:
            if len(products) >= top_k:
                break
            if pid in seen or pid not in _PRODUCT_INDEX:
                continue
            products.append(_card(_PRODUCT_INDEX[pid], 0.55))
            seen.add(pid)

    return ShopperProductsResponse(
        products=products[:top_k],
        sources=[{"id": d.id, "title": d.title, "score": d.score} for d in docs],
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