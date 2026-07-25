"""
INVENTORY ALERT (Huong A) - thuan theo xu huong tim kiem Google Trends.
Keyword search dang len -> nen nhap; dang xuong -> nen giam. Khong ghep sentiment.
Loc theo recent_interest de khong canh bao keyword gan nhu khong ai tim.
"""
import sys
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

MIN_INTEREST = 15   # chi canh bao keyword co do quan tam dang ke

kt = pd.read_parquet(config.OUTPUT_DIR / "keyword_trends.parquet")

rows = []
for _, r in kt.iterrows():
    m, ri, kw = r["momentum"], r["recent_interest"], r["keyword"]
    if m >= 20 and ri >= MIN_INTEREST:
        alert = "RESTOCK"
        action = f"Search {r['trend'].lower()} (interest {ri}) → stock up on '{kw}'"
    elif m >= 5:
        alert = "WATCH"
        action = f"Search {r['trend'].lower()} → monitor demand for '{kw}'"
    elif m <= -10 and ri >= MIN_INTEREST:
        alert = "REDUCE"
        action = f"Search {r['trend'].lower()} (interest {ri}) → consider reducing stock of '{kw}'"
    else:
        continue
    rows.append({"keyword": kw, "group": r["group"], "trend": r["trend"],
                 "momentum": m, "recent_interest": ri, "peak_interest": r["peak_interest"],
                 "alert": alert, "action": action})

order = {"RESTOCK": 0, "WATCH": 1, "REDUCE": 2}
alerts = pd.DataFrame(rows).sort_values(
    ["alert", "momentum"], key=lambda s: s.map(order) if s.name == "alert" else -s
).reset_index(drop=True)
alerts.to_parquet(config.OUTPUT_DIR / "keyword_alerts.parquet")
alerts.to_csv(config.OUTPUT_DIR / "keyword_alerts.csv", index=False, encoding="utf-8-sig")

print("=" * 64)
print("   SEARCH-TREND INVENTORY ALERTS (Google Trends)")
print("=" * 64)
icon = {"RESTOCK": "[+] STOCK UP", "WATCH": "[~] MONITOR", "REDUCE": "[-] REDUCE"}
for _, a in alerts.iterrows():
    print(f"\n{icon[a['alert']]}  |  {a['keyword']}  ({a['group']})")
    print(f"   {a['trend']} · momentum {a['momentum']:+.0f} · interest {a['recent_interest']}")
    print(f"   >> {a['action']}")
print(f"\nTong canh bao: {len(alerts)}  |  Da luu: keyword_alerts.csv / .parquet")
