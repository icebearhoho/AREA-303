"""#14 AI Negotiation Bot — deterministic counter-offer logic.

Concession schedule: the counter price anchors near list_price on round 1 and
concedes toward min_price by round 5, always meeting the buyer halfway between
their offer and the current ask. Never counters below min_price; accepts at/
above 95% of list price; rejects lowball offers or after too many rounds.

Counter prices round to the nearest 100 (not 1,000) rather than a suspiciously
round number — negotiation research finds precise first offers (e.g. $287 vs
$300) make the anchoring party appear more competent/informed and outperform
round numbers. Source: pon.harvard.edu/daily/dealmaking-daily/
negotiation-research-can-use-effective-first-offer-strive-precision-nb.
"""

from __future__ import annotations

from app.schemas.negotiation import NegotiationRequest, NegotiationResponse


def negotiate(req: NegotiationRequest) -> NegotiationResponse:
    list_price = req.list_price_vnd
    min_price = max(0, min(req.min_price_vnd, list_price))
    offer = req.buyer_offer_vnd

    if offer >= list_price * 0.95:
        return NegotiationResponse(
            decision="accept", counter_price_vnd=offer, round=req.round,
            message=f"Đồng ý! {offer:,}₫ cho {req.product_name} — deal xong, cảm ơn bạn đã hợp tác.",
        )

    if req.round >= 6:
        return NegotiationResponse(
            decision="reject", counter_price_vnd=None, round=req.round,
            message=f"Xin lỗi, {min_price:,}₫ là mức thấp nhất bên mình có thể đưa ra cho {req.product_name} lúc này.",
        )
    if offer < min_price * 0.8:
        return NegotiationResponse(
            decision="reject", counter_price_vnd=None, round=req.round,
            message=f"Mức đề nghị {offer:,}₫ thấp hơn nhiều so với chi phí thực tế của {req.product_name}, bên mình không thể đồng ý.",
        )

    progress = min(1.0, (req.round - 1) / 4)  # 0 at round 1 -> 1 at round 5+
    current_ask = list_price - (list_price - min_price) * progress
    midpoint = (offer + current_ask) / 2
    counter = max(min_price, round(midpoint / 100) * 100)  # precise, not round-numbered

    return NegotiationResponse(
        decision="counter", counter_price_vnd=int(counter), round=req.round,
        message=f"Bên mình đề xuất {int(counter):,}₫ cho {req.product_name} — mức hợp lý dựa trên số lượng và chi phí vận hành.",
    )
