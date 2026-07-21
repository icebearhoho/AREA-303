"""#13 Customer Segmentation — XGBoost persona scorer.

Loads the trained artifacts from ``customer_segmentation/models/`` once (lazy
singleton) and predicts a persona for a user's behavioural features. This is
the first backend service to wire in a real trained ML model (.pkl) rather than
a heuristic, so the model is loaded lazily on first request and cached for the
process lifetime — no reload per request.
"""

from __future__ import annotations

import json
import pickle
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.core.exceptions import UpstreamUnavailableError
from app.core.logging import get_logger
from app.schemas.segmentation import SegmentationRequest, SegmentationResponse

log = get_logger("app.services.segmentation")

# customer_segmentation/models/ sits at the repo root, i.e. three levels up
# from this file: app/services/segmentation.py -> app -> backend -> repo root.
_MODELS_DIR = (
    Path(__file__).resolve().parents[3] / "customer_segmentation" / "models"
)
_MODEL_PATH = _MODELS_DIR / "xgb_persona_classifier.pkl"
_ENCODER_PATH = _MODELS_DIR / "label_encoder.pkl"
_FEATURES_PATH = _MODELS_DIR / "feature_columns.json"


class _Artifacts:
    """Bundle of the loaded model, label encoder and feature order."""

    def __init__(self, model: Any, encoder: Any, feature_cols: list[str]) -> None:
        self.model = model
        self.encoder = encoder
        self.feature_cols = feature_cols


@lru_cache(maxsize=1)
def _load_artifacts() -> _Artifacts:
    """Load and cache model artifacts. Raises if any file is missing."""
    missing = [p.name for p in (_MODEL_PATH, _ENCODER_PATH, _FEATURES_PATH) if not p.exists()]
    if missing:
        log.error("segmentation.artifacts_missing", missing=missing, dir=str(_MODELS_DIR))
        raise UpstreamUnavailableError(
            "Segmentation model artifacts not found. "
            "Chạy customer_segmentation/src/03_xgboost_scorer.py để sinh model trước.",
            details={"missing": missing, "models_dir": str(_MODELS_DIR)},
        )

    with open(_MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(_ENCODER_PATH, "rb") as f:
        encoder = pickle.load(f)
    with open(_FEATURES_PATH, encoding="utf-8") as f:
        feature_cols = json.load(f)

    log.info("segmentation.artifacts_loaded", n_features=len(feature_cols),
             classes=list(encoder.classes_))
    return _Artifacts(model=model, encoder=encoder, feature_cols=feature_cols)


def predict_persona(req: SegmentationRequest) -> SegmentationResponse:
    """Predict the persona and per-class probabilities for one user.

    Mirrors ``score_new_user()`` from 03_xgboost_scorer.py, but takes a typed
    request and returns a typed response. Imports pandas locally so the module
    stays import-light when the endpoint isn't hit.
    """
    import pandas as pd

    art = _load_artifacts()

    # Order features exactly as the model was trained on.
    feature_dict = req.model_dump()
    x = pd.DataFrame([feature_dict])[art.feature_cols]

    pred_class = art.model.predict(x)[0]
    pred_proba = art.model.predict_proba(x)[0]

    persona = art.encoder.inverse_transform([pred_class])[0]
    probabilities = {
        cls: round(float(p), 4)
        for cls, p in zip(art.encoder.classes_, pred_proba, strict=True)
    }

    return SegmentationResponse(
        persona=str(persona),
        probabilities=probabilities,
    )


def warmup() -> None:
    """Optionally preload artifacts at startup (called from app lifespan).

    Safe to call even if artifacts are missing — it swallows the error so the
    rest of the API still boots; the first real request will surface the error.
    """
    try:
        _load_artifacts()
    except UpstreamUnavailableError:
        log.warning("segmentation.warmup_skipped_missing_artifacts")
