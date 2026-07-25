"""
Demo Fallback: dong goi keyword trend + alert + interest series + cache sentiment
vao demo_data.json (tu chua). Dashboard doc file nay -> chay du KHONG co parquet /
model / mang.
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
alerts = pd.read_parquet(O / "keyword_alerts.parquet")
trends = pd.read_parquet(O / "keyword_trends.parquet")
g = pd.read_parquet(config.GOOGLE_TRENDS_PARQUET)


def recs(df):
    return df.to_dict(orient="records")


# Interest series theo tung keyword (cho bieu do)
series = {}
for kw, d in g.sort_values("date").groupby("keyword"):
    series[kw] = [{"date": dt.strftime("%Y-%m-%d"), "interest": int(v)}
                  for dt, v in zip(d["date"], d["interest"])]

meta = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "keywords": int(trends.shape[0]),
    "weeks": int(g["date"].nunique()),
    "span": f'{g["date"].min():%b %Y} - {g["date"].max():%b %Y}',
    "rising": int(trends["rising"].sum()),
    "sentiment_f1": 0.69,
}

# Cache sentiment cho o test (chay model 1 lan roi luu)
demo_sentences = [
    "This lipstick is amazing, best purchase ever!",
    "Broke me out and irritated my face, would not buy again",
    "The package arrived on time and looked fine",
    "Absolutely love this jacket, worth every penny",
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
    "keyword_trends": recs(trends),
    "series": series,
    "sentiment_examples": examples,
}
path = O / "demo_data.json"
path.write_text(json.dumps(bundle, ensure_ascii=False), encoding="utf-8")
print("Created:", path.name, f"({path.stat().st_size // 1024} KB)")
