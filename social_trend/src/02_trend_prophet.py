"""
PHASE 4-REAL - Trend brand tren THOI GIAN THAT (submission_time cua Sephora).
- Growth: so review trung binh 6 thang dau vs 6 thang cuoi (bounded, de hieu).
- Prophet: du bao 3 thang toi -> luu cho dashboard ve len chart.
Khong bia timestamp.
"""
import sys
import warnings
import pandas as pd
from prophet import Prophet
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
warnings.filterwarnings("ignore")

bm = pd.read_parquet(config.OUTPUT_DIR / "brand_monthly.parquet")
months = pd.date_range(bm["month"].min(), bm["month"].max(), freq="MS")

tot = bm.groupby("brand_name")["volume"].sum().sort_values(ascending=False)
brands = tot[tot >= 500].index.tolist()
print("So brand phan tich (>=500 review):", len(brands))


def series(b):
    d = bm[bm["brand_name"] == b].set_index("month")["volume"].reindex(months, fill_value=0)
    return pd.DataFrame({"ds": months, "y": d.values})


def recent_pos(b, k=6):
    d = bm[bm["brand_name"] == b].sort_values("month").tail(k)
    return round((d["pct_positive"] * d["volume"]).sum() / d["volume"].sum(), 1)


def trend_label(m):
    if m >= 50:  return "Strongly rising"
    if m >= 20:  return "Rising"
    if m > -20:  return "Stable"
    if m > -50:  return "Falling"
    return "Falling fast"

rows, forecast_rows = [], []
for b in brands:
    ts = series(b)
    y = ts["y"]
    first6, last6 = y.iloc[:6].mean(), y.iloc[-6:].mean()
    # momentum bounded [-100, +100] (khong phinh to khi mau so ~0)
    momentum = round((last6 - first6) / (last6 + first6 + 1e-9) * 100, 1)
    recent_avg = round(last6, 1)      # so review/thang gan day (that, tuyet doi)

    # Prophet du bao 3 thang toi
    m = Prophet(weekly_seasonality=False, yearly_seasonality=False, daily_seasonality=False)
    m.fit(ts)
    fc = m.predict(m.make_future_dataframe(periods=3, freq="MS"))
    for _, fr in fc[fc["ds"] > months.max()].iterrows():
        forecast_rows.append({"brand": b, "month": fr["ds"], "yhat": max(round(fr["yhat"]), 0)})

    rows.append({"brand": b, "momentum": momentum, "trend": trend_label(momentum),
                 "recent_avg": recent_avg, "recent_pos": recent_pos(b),
                 "total_reviews": int(y.sum())})

res = pd.DataFrame(rows).sort_values("momentum", ascending=False).reset_index(drop=True)
res["rising"] = res["momentum"] > 20
res.to_parquet(config.OUTPUT_DIR / "brand_trends.parquet")
pd.DataFrame(forecast_rows).to_parquet(config.OUTPUT_DIR / "brand_forecast.parquet")

print("\n=== TOP 12 BRAND MOMENTUM CAO NHAT ===")
print(res.head(12).to_string(index=False))
print("\n=== 5 BRAND GIAM MANH ===")
print(res.tail(5).to_string(index=False))
print("\nSo brand DANG LEN (momentum>20):", int(res["rising"].sum()))
print("Da luu: brand_trends.parquet, brand_forecast.parquet")
