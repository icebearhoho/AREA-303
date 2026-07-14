"""#17 Seller Coach — 5-step audit + 4-week roadmap."""

from __future__ import annotations

import json

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.genai import (
    AuditStep,
    RoadmapWeek,
    SellerCoachRequest,
    SellerCoachResponse,
)
from app.services.genai import SELLER_COACH_SYSTEM, llm_cache
from app.services.genai.base import LlmMessage
from app.services.genai.demo_data import SELLER_AUDIT, SELLER_ROADMAP
from app.services.genai.factory import get_llm_client

log = get_logger("app.services.seller_coach")


def _overall(audit: list[AuditStep]) -> int:
    return round(sum(s.score for s in audit) / max(1, len(audit)))


async def _llm_audit(req: SellerCoachRequest) -> SellerCoachResponse:
    """Ask the LLM to score a seller's audit + propose a roadmap as JSON."""
    llm = get_llm_client()
    prompt = (
        "Đánh giá seller dựa trên 5 trục (listing, pricing, visuals, reviews, inventory). "
        "Trả về JSON thuần:\n"
        "{\n"
        '  "audit": [{"id": "...", "label": "...", "score": 0-100, "tip": "..."}],\n'
        '  "roadmap": [{"week": 1, "title": "...", "bullets": ["..."]}]\n'
        "}\n"
        f"Seller id: {req.seller_id or 'demo'}"
    )
    resp = await llm.chat(
        [
            LlmMessage(role="system", content=SELLER_COACH_SYSTEM),
            LlmMessage(role="user", content=prompt),
        ],
        temperature=0.5,
        max_tokens=900,
    )

    # Parse JSON — strip markdown fences if the model wraps it.
    raw = resp.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```", 2)[1].lstrip("json").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        log.warning("seller_coach.json_parse_failed")
        return _demo_response(req)

    audit = [AuditStep(**a) for a in data.get("audit", [])][:5]
    roadmap = [RoadmapWeek(**w) for w in data.get("roadmap", [])][:4]

    if len(audit) < 5 or len(roadmap) < 4:
        return _demo_response(req)

    return SellerCoachResponse(
        overall=_overall(audit),
        audit=audit,
        roadmap=roadmap,
        demo_mode=False,
    )


def _demo_response(req: SellerCoachRequest) -> SellerCoachResponse:
    audit = [AuditStep(**a) for a in SELLER_AUDIT]
    roadmap = [RoadmapWeek(**w) for w in SELLER_ROADMAP]
    return SellerCoachResponse(
        overall=_overall(audit),
        audit=audit,
        roadmap=roadmap,
        demo_mode=True,
    )


@llm_cache(prefix="seller_coach")
async def coach(req: SellerCoachRequest) -> SellerCoachResponse:
    if settings.DEMO_MODE or (not settings.GEMINI_API_KEY and not settings.OPENAI_API_KEY):
        log.info("seller_coach.demo_mode")
        return _demo_response(req)
    try:
        return await _llm_audit(req)
    except Exception as exc:
        log.warning("seller_coach.fallback_to_demo", error=str(exc))
        return _demo_response(req)