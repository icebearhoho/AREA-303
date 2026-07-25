"""API sentiment dung chung: tu chon transformer (chinh) hoac baseline (du phong)."""
import config

ID_TO_NAME = {0: "negative", 1: "neutral", 2: "positive"}
_MODEL_DIR = config.OUTPUT_DIR / "xlmr_sentiment"
_engine = None  # lazy-load: chi nap model lan goi dau tien


def _load():
    global _engine
    if _engine is not None:
        return _engine
    if _MODEL_DIR.exists():                       # co model transformer -> dung
        import torch
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        tok = AutoTokenizer.from_pretrained(_MODEL_DIR)
        mdl = AutoModelForSequenceClassification.from_pretrained(_MODEL_DIR).eval()
        _engine = ("transformer", tok, mdl, torch)
    else:                                         # khong co -> fallback baseline
        import joblib
        vec = joblib.load(config.OUTPUT_DIR / "sentiment_vectorizer.pkl")
        mdl = joblib.load(config.OUTPUT_DIR / "sentiment_baseline_model.pkl")
        _engine = ("baseline", vec, mdl, None)
    return _engine


def predict_sentiment(text: str) -> dict:
    kind, a, b, torch = _load()
    if kind == "transformer":
        inputs = a(text, return_tensors="pt", truncation=True, max_length=128)
        with torch.no_grad():
            probs = torch.softmax(b(**inputs).logits[0], dim=-1).numpy()
        i = int(probs.argmax())
        return {"label": ID_TO_NAME[i], "label_id": i,
                "score": round(float(probs[i]), 4), "engine": "transformer"}
    else:
        X = a.transform([text])
        i = int(b.predict(X)[0])
        score = float(b.predict_proba(X)[0][i])
        return {"label": ID_TO_NAME[i], "label_id": i,
                "score": round(score, 4), "engine": "baseline"}


if __name__ == "__main__":   # test nhanh
    for t in ["I love this dress, so beautiful!",
              "Terrible quality, very disappointed",
              "The package arrived today"]:
        print(predict_sentiment(t), "<-", t)
