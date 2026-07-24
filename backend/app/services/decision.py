"""Track 2, Đề 5 — E-commerce Decision Intelligence service.

Heuristic core (deterministic): for every listed metric, higher is better
(ROAS, sales lift %, margin %, sell-through %), so the "best" past decision is
simply the highest-value entry. The best month to push ads is the month of the
best-performing `ad` decision (falls back to None if no ad decisions carry a
month). The recommendation narrative runs on the LLM with a templated fallback.
"""

from __future__ import annotations

from app.schemas.decision import (
    BestDecision,
    DecisionRequest,
    DecisionResponse,
    PastDecision,
)
from app.services.llm_reasoning import reason_json

_MONTHS_VI = {
    1: "Tháng 1", 2: "Tháng 2", 3: "Tháng 3", 4: "Tháng 4", 5: "Tháng 5", 6: "Tháng 6",
    7: "Tháng 7", 8: "Tháng 8", 9: "Tháng 9", 10: "Tháng 10", 11: "Tháng 11", 12: "Tháng 12",
}


def _best(req: DecisionRequest) -> tuple[PastDecision, int | None]:
    best = max(req.decisions, key=lambda d: d.value)
    ad_decisions = [d for d in req.decisions if d.kind == "ad" and d.month is not None]
    best_ad_month = max(ad_decisions, key=lambda d: d.value).month if ad_decisions else None
    return best, best_ad_month


_SYSTEM = (
    "You are an operations-strategy agent for a Vietnamese e-commerce seller. "
    "Given the current situation, a category, and the single best-performing past "
    "decision (with its metric), recommend ONE concrete next action in a short "
    "Vietnamese paragraph (2-3 sentences), grounded in that past result. "
    'Reply as JSON: {"recommended_action": "...", "reasoning": "..."}'
)


def _fallback(req: DecisionRequest, best: PastDecision, ad_month: int | None) -> tuple[str, str]:
    timing = f" Thời điểm đẩy quảng cáo tốt nhất: {_MONTHS_VI[ad_month]}." if ad_month else ""
    action = (
        f"Lặp lại chiến lược '{best.description}' ({best.kind}) — nó đạt "
        f"{best.metric} = {best.value:g}, tốt nhất trong lịch sử.{timing}"
    )
    reasoning = (
        f"Với tình huống hiện tại ({req.situation[:80]}), quyết định quá khứ hiệu quả "
        f"nhất theo {best.metric} là '{best.description}'. Ưu tiên tái áp dụng cách làm này "
        f"cho ngành {req.category}."
    )
    return action, reasoning


async def recommend_decision(req: DecisionRequest) -> DecisionResponse:
    best, ad_month = _best(req)
    hist = "; ".join(f"{d.kind}:'{d.description}' {d.metric}={d.value:g}" for d in req.decisions[:12])
    data = await reason_json(
        _SYSTEM,
        f"Situation: {req.situation}\nCategory: {req.category}\n"
        f"Best past decision: {best.kind} '{best.description}' ({best.metric}={best.value:g}).\n"
        f"Full history: {hist}."
        + (f"\nBest ad month observed: {ad_month}." if ad_month else ""),
        label="decision",
    )
    action = (data or {}).get("recommended_action") if data else None
    reasoning = (data or {}).get("reasoning") if data else None
    fb_action, fb_reason = _fallback(req, best, ad_month)
    return DecisionResponse(
        best_decision=BestDecision(
            kind=best.kind, description=best.description, metric=best.metric, value=best.value
        ),
        best_ad_month=ad_month,
        recommended_action=(action or "").strip() or fb_action,
        reasoning=(reasoning or "").strip() or fb_reason,
    )
