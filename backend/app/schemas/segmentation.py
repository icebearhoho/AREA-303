"""Schemas for #13 Customer Segmentation.

The XGBoost persona classifier (customer_segmentation/models/) is loaded by the
service layer and predicts one of the 4 personas from a user's behavioural
features. The client sends the 14 engineered features directly (same contract
as recsys: no DB lookup), so the endpoint stays stateless and demo-safe.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# --- #13 Customer Segmentation -------------------------------------------
class SegmentationRequest(BaseModel):
    """The 14 engineered behavioural features, matching
    ``customer_segmentation/models/feature_columns.json``.

    These are produced by the offline feature-engineering step
    (``01_feature_engineering.py``): counts are log1p-transformed, ratios are
    already in [0, 1], and the two ``has_*`` flags are 0/1.
    """

    log_recency: float = Field(..., ge=0, description="log1p(daysSinceLastLogin)")
    seniority_months: float = Field(..., ge=0, description="Số tháng gắn bó với platform")
    log_followers: float = Field(..., ge=0, description="log1p(socialNbFollowers)")
    log_follows: float = Field(..., ge=0, description="log1p(socialNbFollows)")
    log_products_liked: float = Field(..., ge=0, description="log1p(socialProductsLiked)")
    log_products_listed: float = Field(..., ge=0, description="log1p(productsListed)")
    log_products_sold: float = Field(..., ge=0, description="log1p(productsSold)")
    products_pass_rate: float = Field(..., ge=0, le=100, description="% sản phẩm bị từ chối khi bán")
    log_products_wished: float = Field(..., ge=0, description="log1p(productsWished)")
    log_products_bought: float = Field(..., ge=0, description="log1p(productsBought)")
    buy_ratio: float = Field(..., ge=0, le=1, description="Tỉ lệ mua / (mua+bán)")
    wish_to_buy: float = Field(..., ge=0, description="productsBought / (productsWished+1)")
    has_any_app: int = Field(..., ge=0, le=1, description="Có cài app điện thoại (0/1)")
    has_profile_picture: int = Field(..., ge=0, le=1, description="Có ảnh đại diện (0/1)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "log_recency": 5.92,
                "seniority_months": 102.0,
                "log_followers": 1.39,
                "log_follows": 2.20,
                "log_products_liked": 0.77,
                "log_products_listed": 0.02,
                "log_products_sold": 0.04,
                "products_pass_rate": 0.83,
                "log_products_wished": 0.44,
                "log_products_bought": 0.16,
                "buy_ratio": 0.16,
                "wish_to_buy": 0.14,
                "has_any_app": 1,
                "has_profile_picture": 1,
            }
        }
    }


class SegmentationResponse(BaseModel):
    persona: str = Field(..., description="Persona được dự đoán")
    probabilities: dict[str, float] = Field(
        ..., description="Xác suất từng persona (tổng ≈ 1.0)"
    )
    model_version: str = Field(
        default="xgb_persona_classifier", description="Định danh model dùng để dự đoán"
    )
