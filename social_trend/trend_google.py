"""
TREND DETECTOR (Google Trends) - Huong A.
Do hot tim kiem theo tuan la mot duong xu huong THAT san -> khong can Prophet.
Chi tinh momentum (8 tuan cuoi vs 8 tuan dau) de biet keyword dang len / xuong.
"""
import sys
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

RECENT_W = 8   # so tuan de tinh momentum


def trend_label(m: float) -> str:
    if m >= 20:  return "Strongly rising"
    if m >= 5:   return "Rising"
    if m > -10:  return "Stable"
    if m > -20:  return "Falling"
    return "Falling fast"


def main() -> None:
    if not config.GOOGLE_TRENDS_PARQUET.exists():
        raise FileNotFoundError(f"Khong tim thay: {config.GOOGLE_TRENDS_PARQUET}")
    g = pd.read_parquet(config.GOOGLE_TRENDS_PARQUET)
    print("Rows:", len(g), "| keywords:", g["keyword"].nunique(),
          "| weeks:", g["date"].nunique())
    print("Range:", g["date"].min().date(), "->", g["date"].max().date())

    rows = []
    for kw, d in g.groupby("keyword"):
        d = d.sort_values("date")
        first = d["interest"].head(RECENT_W).mean()
        last = d["interest"].tail(RECENT_W).mean()
        momentum = round((last - first) / (last + first + 1e-9) * 100, 1)  # bounded [-100,100]
        rows.append({
            "keyword": kw,
            "group": d["group"].iloc[0],
            "momentum": momentum,
            "trend": trend_label(momentum),
            "recent_interest": round(last, 1),
            "peak_interest": int(d["interest"].max()),
        })

    res = (pd.DataFrame(rows)
           .sort_values("momentum", ascending=False)
           .reset_index(drop=True))
    res["rising"] = res["momentum"] >= 5
    res.to_parquet(config.OUTPUT_DIR / "keyword_trends.parquet")

    print("\n=== XU HUONG KEYWORD (Google Trends) ===")
    print(res.to_string(index=False))
    print(f"\nKeyword dang len (momentum>=5): {int(res['rising'].sum())}")
    print("Da luu: keyword_trends.parquet")


if __name__ == "__main__":
    main()
