"""Heuristic scorers for #01 Review Sentiment, #05 Fake Review, #02 Dynamic
Pricing, and #04 Churn Prediction.

Key-free and deterministic so the seller app always gets a live response. The
LLM versions live in the offline modeling layer (review_sentiment/, fake_review/,
dynamic_pricing/, customer_churn/) and use the same formulas where applicable
(see customer_churn/src/02_score.py:rule_risk for the churn heuristic origin).
"""

from __future__ import annotations

import math
import re

from app.schemas.insights import (
    ChurnRequest,
    ChurnResponse,
    FakeReviewRequest,
    FakeReviewResponse,
    PricingRequest,
    PricingResponse,
    SentimentRequest,
    SentimentResponse,
)
from app.services.genai.demo_data import DEMO_CATALOG

# English + Vietnamese cue words (the seller platform sees both).
_POS = {
    "love", "great", "excellent", "perfect", "amazing", "comfortable", "soft",
    "recommend", "happy", "beautiful", "quality", "fast", "breathable", "worth",
    "tuyệt", "đẹp", "tốt", "thích", "hài lòng", "mượt", "chuẩn", "nhanh", "ưng",
}
_NEG = {
    "bad", "poor", "terrible", "disappointed", "cheap", "broke", "broken", "thin",
    "refund", "return", "smell", "fake", "worst", "damaged", "late", "wrong",
    "tệ", "dởm", "kém", "thất vọng", "rách", "hỏng", "chậm", "lừa", "trả hàng", "mỏng",
}
_GENERIC = {
    "highly recommend", "best ever", "best purchase", "love it", "amazing quality",
    "great quality", "works perfectly", "highly recommended", "so good", "perfect",
}


def _words(text: str) -> list[str]:
    return re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)


def analyze_sentiment(req: SentimentRequest) -> SentimentResponse:
    low = req.text.lower()
    words = set(_words(req.text))
    pos = sum(1 for w in _POS if (" " in w and w in low) or w in words)
    neg = sum(1 for w in _NEG if (" " in w and w in low) or w in words)

    score = pos - neg
    if req.rating is not None:  # rating is a strong prior when present
        score += {1: -2, 2: -1, 3: 0, 4: 1, 5: 2}[req.rating]

    if score > 1:
        s, reason = "positive", f"Positive cues ({pos}) outweigh negative ({neg})."
    elif score < -1:
        s, reason = "negative", f"Negative cues ({neg}) dominate the review."
    else:
        s, reason = "neutral", "Mixed or weak signal — lukewarm / factual review."

    confidence = min(0.95, 0.5 + 0.12 * abs(score))
    return SentimentResponse(sentiment=s, confidence=round(confidence, 2), reason=reason)


def detect_fake(req: FakeReviewRequest) -> FakeReviewResponse:
    low = req.text.lower()
    words = _words(req.text)
    signals: list[str] = []

    generic_hits = [g for g in _GENERIC if g in low]
    if generic_hits:
        signals.append(f"generic phrases: {', '.join(generic_hits[:2])}")
    if len(words) < 6:
        signals.append("very short, no product-specific detail")
    if low.count("!") >= 3:
        signals.append("excessive exclamation")
    # repetition of the same token (hollow enthusiasm)
    if words and max((words.count(w) for w in set(words)), default=0) >= 3:
        signals.append("repetitive wording")
    # 5★ + purely generic praise is a classic CG pattern
    specifics = any(k in low for k in (
        "fit", "size", "fabric", "color", "colour", "wash", "material", "scent",
        "smell", "delivery", "ship", "vải", "size", "màu", "giao", "chất liệu",
    ))
    if not specifics:
        signals.append("no concrete specifics (fit/fabric/scent/delivery)")

    score = len(signals) - (1 if specifics else 0)
    is_fake = score >= 2
    confidence = min(0.95, 0.5 + 0.13 * score) if is_fake else min(0.9, 0.5 + 0.1 * (2 - score))
    reason = (
        "Multiple fabrication signals with no concrete detail." if is_fake
        else "Reads like a genuine review (specific and/or balanced)."
    )
    return FakeReviewResponse(
        is_fake=is_fake, confidence=round(max(0.5, confidence), 2),
        signals=signals or ["no strong fake signals"], reason=reason,
    )


# ---------------------------------------------------------------------------
# #02 Dynamic Pricing — comps-median baseline (same idea as
# dynamic_pricing/src/02_recommend.py, using the demo catalog as comps).
# ---------------------------------------------------------------------------
def _category_price_stats(category: str) -> tuple[list[int], int, int, int]:
    prices = sorted(
        item["metadata"]["price_vnd"]
        for item in DEMO_CATALOG
        if item["metadata"].get("category") == category
    )
    if not prices:
        prices = sorted(item["metadata"]["price_vnd"] for item in DEMO_CATALOG)
    n = len(prices)
    median = prices[n // 2]
    p25 = prices[max(0, n // 4)]
    p75 = prices[min(n - 1, (3 * n) // 4)]
    return prices, median, p25, p75


def recommend_price(req: PricingRequest) -> PricingResponse:
    prices, median, p25, p75 = _category_price_stats(req.category)

    if req.current_price is None:
        recommended = median
        rationale = f"No current price given — using the {req.category} category median from {len(prices)} comparable products."
    else:
        cur = req.current_price
        if cur > median * 1.3:
            recommended = round((cur + median * 1.1) / 2)
            rationale = f"{cur:,}₫ is well above the {req.category} median ({median:,}₫) — nudging down to stay competitive."
        elif cur < median * 0.7:
            recommended = round((cur + median * 0.9) / 2)
            rationale = f"{cur:,}₫ is well below the {req.category} median ({median:,}₫) — you may be underpricing; nudging up."
        else:
            recommended = round((cur + median) / 2)
            rationale = f"{cur:,}₫ is already close to the {req.category} median ({median:,}₫) — minor optimization only."

    return PricingResponse(
        recommended_price=int(recommended), low=int(min(p25, recommended)),
        high=int(max(p75, recommended)), category_median=int(median),
        sample_size=len(prices), rationale=rationale,
    )


# ---------------------------------------------------------------------------
# #04 Churn Prediction — same rule_risk formula as
# customer_churn/src/02_score.py:rule_risk, ported to be key-free/deterministic.
# ---------------------------------------------------------------------------
def score_churn(req: ChurnRequest) -> ChurnResponse:
    z = (0.012 * req.recency_days - 0.15 * req.frequency_orders
         - 0.08 * req.sessions_last_month + 2.2 * req.cart_abandon_rate)
    z += 1.1 if req.trend == "declining" else (-0.9 if req.trend == "growing" else 0)
    z -= 1.6
    risk = 1 / (1 + math.exp(-z))

    band = "high" if risk >= 0.6 else ("medium" if risk >= 0.3 else "low")

    drivers = []
    if req.recency_days > 60:
        drivers.append(f"No purchase in {req.recency_days} days")
    if req.frequency_orders <= 1:
        drivers.append("Very few past orders")
    if req.sessions_last_month <= 1:
        drivers.append("Barely browsing lately")
    if req.cart_abandon_rate > 0.5:
        drivers.append(f"Abandons {req.cart_abandon_rate:.0%} of carts")
    if req.trend == "declining":
        drivers.append("Activity trending down")
    if not drivers:
        drivers.append("Healthy, active buying pattern")

    action = (
        "Send a win-back offer (discount or free shipping) before they churn."
        if band == "high" else
        "Nurture with a personalized recommendation email."
        if band == "medium" else
        "No action needed — keep delighting as usual."
    )
    return ChurnResponse(
        churn_risk=round(risk, 2), risk_band=band, drivers=drivers, retention_action=action,
    )
