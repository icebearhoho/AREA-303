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
    InventoryAlertRequest,
    InventoryAlertResponse,
    PricingRequest,
    PricingResponse,
    RegretRequest,
    RegretResponse,
    ReturnRequest,
    ReturnResponse,
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


def _risk_band(risk: float) -> str:
    return "high" if risk >= 0.6 else ("medium" if risk >= 0.3 else "low")


# ---------------------------------------------------------------------------
# #10 Return/Refund Prediction — heuristic: high price + sizing risk + heavy
# discount (impulse buy) + new customer + few reviews read all raise return risk.
# ---------------------------------------------------------------------------
# Category base return rates — grounded in 2026 industry benchmarks: apparel
# runs 20-40% (highest of any category, driven by sizing/fit uncertainty and
# "bracketing"), beauty/cosmetics runs 4-12% (hygiene concerns keep it low).
# Sources: capitaloneshopping.com/research/average-retail-return-rate,
# richpanel.com/learn/ecommerce-return-rates (2026 benchmarks).
_BASE_RETURN_RATE = {"Thời trang": 0.28, "Mỹ phẩm": 0.08, "Phụ kiện": 0.12}


def score_return(req: ReturnRequest) -> ReturnResponse:
    base = _BASE_RETURN_RATE[req.category]
    z = math.log(base / (1 - base))  # start from the category's real base rate
    z += 0.5 if req.size_related else 0.0   # fit/sizing is THE documented driver of apparel returns
    z += 0.015 * req.discount_pct
    z += 0.4 if req.is_new_customer else 0.0
    # Reading reviews reduces risk, but with diminishing returns — cap the
    # benefit so it can't cancel out a genuine sizing/fit return risk. (QA:
    # previously uncapped, letting reviews_read=30+ collapse a high-risk order to "low".)
    z -= 0.12 * min(req.reviews_read, 4)
    z += (req.price_vnd / 1_000_000) * 0.15
    risk = 1 / (1 + math.exp(-z))
    band = _risk_band(risk)

    drivers = []
    if req.size_related:
        drivers.append("Sizing-sensitive item (clothing/shoes) — fit risk")
    if req.discount_pct >= 30:
        drivers.append(f"Heavy discount ({req.discount_pct:.0f}%) — possible impulse buy")
    if req.is_new_customer:
        drivers.append("First-time customer — no purchase history to gauge fit")
    if req.reviews_read == 0:
        drivers.append("Bought without reading any reviews")
    if req.price_vnd >= 1_000_000:
        drivers.append("High-value item — more room for buyer's remorse")
    if not drivers:
        drivers.append("Low-risk profile")

    action = (
        "Proactively send sizing guidance + easy-return reminder before shipping."
        if band == "high" else
        "Include a size chart / usage tip in the packing slip."
        if band == "medium" else
        "No special handling needed."
    )
    return ReturnResponse(return_risk=round(risk, 2), risk_band=band, drivers=drivers, action=action)


# ---------------------------------------------------------------------------
# #15 Post-purchase Regret Predictor — heuristic: fast/late-night/discount-driven
# purchases with no comparison shopping signal higher regret risk.
# ---------------------------------------------------------------------------
# Grounded in impulse-buying research: cognitive/self-control decline sets in
# after ~10pm (decision fatigue + prefrontal cortex impairment), and ~48% of
# impulse purchases are later regretted (vs. a much lower base rate for
# deliberate purchases). Sources: capitaloneshopping.com/research/
# impulse-buying-statistics, simplicitydx.com (48% regret finding), 100.3thepeak
# late-night-shopping coverage (worst decisions after 10pm).
_LATE_NIGHT_HOURS = {22, 23, 0, 1, 2, 3}
_IMPULSE_REGRET_RATE = 0.48
_DELIBERATE_REGRET_RATE = 0.12


def score_regret(req: RegretRequest) -> RegretResponse:
    impulsive = req.decision_time_seconds < 60 or req.revisit_count == 0
    base = _IMPULSE_REGRET_RATE if impulsive else _DELIBERATE_REGRET_RATE
    z = math.log(base / (1 - base))
    z += 0.5 if req.decision_time_seconds < 60 else 0.0
    z += 0.3 if req.revisit_count == 0 else 0.0
    z += 0.6 if req.purchase_hour in _LATE_NIGHT_HOURS else 0.0
    z += 0.3 if req.used_discount else 0.0
    z += 0.3 if req.price_vnd >= 1_000_000 else 0.0
    risk = 1 / (1 + math.exp(-z))
    band = _risk_band(risk)

    drivers = []
    if req.decision_time_seconds < 60:
        drivers.append("Decided in under a minute — impulsive")
    if req.revisit_count == 0:
        drivers.append("Bought without comparing alternatives")
    if req.purchase_hour in _LATE_NIGHT_HOURS:
        drivers.append("Purchased late at night — lower self-control window")
    if req.used_discount:
        drivers.append("Purchase driven mainly by a discount")
    if req.price_vnd >= 1_000_000:
        drivers.append("High-value purchase — more room for regret")
    if not drivers:
        drivers.append("Deliberate, well-considered purchase")

    if band == "high":
        msg = "Cảm ơn bạn đã mua hàng! Bạn có 7 ngày đổi trả miễn phí nếu sản phẩm chưa phù hợp — không cần lo lắng nhé 💛"
    elif band == "medium":
        msg = "Đơn hàng của bạn đang được xử lý. Nếu cần đổi size hoặc màu khác, chỉ cần liên hệ trong vòng 7 ngày."
    else:
        msg = "Cảm ơn bạn đã tin tưởng lựa chọn kỹ lưỡng — chúc bạn hài lòng với sản phẩm!"

    return RegretResponse(regret_risk=round(risk, 2), risk_band=band, drivers=drivers, reassurance_message=msg)


# ---------------------------------------------------------------------------
# #08 Sentiment-driven Inventory Alert — combine social buzz (mentions x
# sentiment) with current stock runway to flag understock risk before a
# viral moment causes a stockout. Approach is grounded in real research: 59%
# of consumers say viral trends now cause faster sellouts, blending social
# sentiment with historical sales improves forecast accuracy by ~42%, and
# early trend detection cut stockouts ~40% in one study. Sources:
# homeofdirectcommerce.com (1-in-3-shoppers social-speed-retail),
# sranalytics.io/blog/predictive-inventory-analytics.
# ---------------------------------------------------------------------------
def score_inventory_alert(req: InventoryAlertRequest) -> InventoryAlertResponse:
    trend_score = (req.social_mentions_7d / 100) * max(0.0, (req.social_sentiment + 1) / 2)
    is_trending = trend_score >= 2.0

    days_left = req.current_stock / max(req.avg_daily_sales, 0.1)
    projected_daily = req.avg_daily_sales * (1 + min(2.0, trend_score / 3))

    if is_trending and days_left <= 7:
        level = "urgent"
    elif is_trending and days_left <= 14:
        level = "watch"
    else:
        level = "none"

    target_days = 14
    needed = max(0, round(projected_daily * target_days - req.current_stock))

    if level == "urgent":
        reason = (f"'{req.product_name}' is trending (score {trend_score:.1f}) "
                  f"with only {days_left:.1f} days of stock left — restock now.")
    elif level == "watch":
        reason = (f"'{req.product_name}' is picking up buzz (score {trend_score:.1f}) "
                  f"and stock runway is getting short ({days_left:.1f} days) — plan a restock.")
    else:
        reason = "No unusual social buzz — current stock runway looks fine."

    return InventoryAlertResponse(
        is_trending=is_trending, trend_score=round(trend_score, 2),
        days_of_stock_left=round(days_left, 1), alert_level=level,
        recommended_restock_qty=needed, reason=reason,
    )
