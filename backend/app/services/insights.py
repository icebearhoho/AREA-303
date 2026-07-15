"""Heuristic scorers for #01 Review Sentiment and #05 Fake Review.

Key-free and deterministic so the seller app always gets a live response. The
LLM versions live in the offline modeling layer (review_sentiment/, fake_review/)
and can replace these later behind the same schema.
"""

from __future__ import annotations

import re

from app.schemas.insights import (
    FakeReviewRequest,
    FakeReviewResponse,
    SentimentRequest,
    SentimentResponse,
)

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
