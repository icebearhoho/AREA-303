"""
PHASE 7 - Demo Fallback: dong goi TOAN BO du lieu brand + cache sentiment vao demo_data.json.
Dashboard doc file nay -> chay duoc du KHONG co parquet / khong co model / mat mang.
"""
import sys
import json
from datetime import datetime
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

O = config.OUTPUT_DIR
alerts = pd.read_parquet(O / "brand_alerts.parquet")
bm     = pd.read_parquet(O / "brand_monthly.parquet")
bf     = pd.read_parquet(O / "brand_forecast.parquet")
bt     = pd.read_parquet(O / "brand_trends.parquet")
pm     = pd.read_parquet(O / "product_monthly.parquet")


def recs(df, datecols=()):
    df = df.copy()
    for c in datecols:
        df[c] = df[c].dt.strftime("%Y-%m-%d")
    return df.to_dict(orient="records")


meta = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "reviews": int(bm["volume"].sum()),
    "brands": int(bm["brand_name"].nunique()),
    "months": int(bm["month"].nunique()),
    "rising": int(bt["rising"].sum()),
    "span": f'{bm["month"].min():%b %Y} - {bm["month"].max():%b %Y}',
    "sentiment_f1": 0.69,
}

# Cache sentiment cho vai cau demo (chay model 1 lan roi luu)
demo_sentences = [
    "This serum completely transformed my skin!",
    "Broke me out and irritated my face, would not buy again",
    "It arrived on time and the packaging was fine",
    "Absolutely love this moisturizer, worth every penny",
]
examples = []
try:
    from sentiment import predict_sentiment
    for s in demo_sentences:
        examples.append({"text": s, **predict_sentiment(s)})
    print("Cached sentiment for", len(examples), "sentences (real model).")
except Exception as e:
    print("Skip sentiment cache:", e)

bundle = {
    "meta": meta,
    "alerts": recs(alerts),
    "brand_trends": recs(bt),
    "brand_monthly": recs(bm, ["month"]),
    "brand_forecast": recs(bf, ["month"]),
    "product_monthly": recs(pm, ["month"]),
    "sentiment_examples": examples,
}
path = O / "demo_data.json"
path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
print("Created:", path.name, f"({path.stat().st_size // 1024} KB)")
