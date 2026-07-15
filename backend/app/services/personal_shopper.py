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


_COSMETICS_HINTS = (
    "skincare", "da dầu", "da khô", "mụn", "dưỡng", "serum", "kem", "son", "môi",
    "trang điểm", "makeup", "mặt nạ", "toner", "chống nắng", "spf", "mỹ phẩm",
    "beauty", "cushion", "phấn", "cấp ẩm", "rửa mặt", "sạch da", "bha", "aha",
)
_FASHION_HINTS = (
    "áo", "váy", "đầm", "quần", "jean", "giày", "sneaker", "dép", "sandal", "túi",
    "balo", "ví", "phụ kiện", "thời trang", "đồng hồ", "kính", "mũ", "nón",
    "hoodie", "khoác", "outfit", "mặc",
)


def _tokens(s: str) -> set[str]:
    import re
    return set(re.findall(r"[^\W\d_]+", s.lower(), flags=re.UNICODE))


def _relevance(item: dict, qtokens: set[str], q: str, cos: bool, fas: bool) -> int:
    meta = item.get("metadata", {})
    cat = meta.get("category", "")
    text = f"{item['title']} {item.get('text', '')} {cat}".lower()
    score = len(qtokens & _tokens(text))          # keyword overlap
    score += sum(1 for h in _COSMETICS_HINTS if h in q and h in text)
    score += sum(1 for h in _FASHION_HINTS if h in q and h in text)
    if cos and cat == "Mỹ phẩm":
        score += 6                                  # match the query's intent
    if fas and cat in ("Thời trang", "Phụ kiện"):
        score += 6
    return score


@llm_cache(prefix="shopper_products")
async def _retrieve_products(query: str, top_k: int) -> ShopperProductsResponse:
    """Rank the catalog by relevance to the query and return the top_k.

    A skincare query surfaces cosmetics; a fashion query surfaces clothing —
    off-intent items are pushed out rather than padding the list with noise.
    """
    q = query.lower()
    qtokens = _tokens(query)
    cos = any(h in q for h in _COSMETICS_HINTS)
    fas = any(h in q for h in _FASHION_HINTS)

    scored = sorted(
        DEMO_CATALOG,
        key=lambda it: _relevance(it, qtokens, q, cos, fas),
        reverse=True,
    )

    # With a clear single intent, keep only that domain when there's enough of it.
    if cos and not fas:
        on = [it for it in scored if it["metadata"].get("category") == "Mỹ phẩm"]
        if len(on) >= min(top_k, 4):
            scored = on
    elif fas and not cos:
        on = [it for it in scored if it["metadata"].get("category") in ("Thời trang", "Phụ kiện")]
        if len(on) >= min(top_k, 4):
            scored = on

    picks = scored[:top_k]
    products = [
        _card(it, max(0.55, min(0.98, 0.6 + _relevance(it, qtokens, q, cos, fas) * 0.05)))
        for it in picks
    ]
    return ShopperProductsResponse(
        products=products,
        sources=[{"id": it["id"], "title": it["title"], "score": 1.0} for it in picks],
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