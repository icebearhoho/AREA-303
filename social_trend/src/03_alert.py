"""
PHASE 5-REAL - Canh bao nhap hang tu trend brand THAT.
Hien thi: so review/thang gan day (that) + nhan xu huong + % tich cuc.
RESTOCK: dang len + tich cuc cao | WATCH: dang len + tich cuc vua
REDUCE : dang giam + tich cuc thap -> giam ton kho
"""
import sys
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

bt = pd.read_parquet(config.OUTPUT_DIR / "brand_trends.parquet")
POS_RESTOCK = 80

rows = []
# --- Brand dang len + volume du dang ke -> RESTOCK / WATCH ---
candidates = bt[bt["rising"] & (bt["recent_avg"] >= 20)].sort_values("momentum", ascending=False)
for _, r in candidates.head(6).iterrows():
    if r["recent_pos"] >= POS_RESTOCK:
        alert = "RESTOCK"
        action = (f"{r['trend']} (~{r['recent_avg']:.0f} reviews/mo) + {r['recent_pos']}% "
                  f"positive → restock recommended")
    else:
        alert = "WATCH"
        action = (f"{r['trend']} but only {r['recent_pos']}% positive "
                  f"→ monitor quality before restocking")
    rows.append({"brand": r["brand"], "trend": r["trend"], "momentum": r["momentum"],
                 "recent_avg": r["recent_avg"], "recent_pos": r["recent_pos"],
                 "total_reviews": r["total_reviews"], "alert": alert, "action": action})

# --- Brand giam + tich cuc thap -> REDUCE ---
risk = bt[(bt["momentum"] < -30) & (bt["recent_pos"] < 75)].sort_values("momentum").head(3)
for _, r in risk.iterrows():
    rows.append({"brand": r["brand"], "trend": r["trend"], "momentum": r["momentum"],
                 "recent_avg": r["recent_avg"], "recent_pos": r["recent_pos"],
                 "total_reviews": r["total_reviews"], "alert": "REDUCE",
                 "action": (f"{r['trend']} + only {r['recent_pos']}% positive "
                            f"→ consider reducing stock")})

alerts = pd.DataFrame(rows)
alerts.to_parquet(config.OUTPUT_DIR / "brand_alerts.parquet")
alerts.to_csv(config.OUTPUT_DIR / "brand_alerts.csv", index=False, encoding="utf-8-sig")

print("=" * 62)
print("   CANH BAO NHAP HANG (tu review Sephora that)")
print("=" * 62)
icon = {"RESTOCK": "[+] NHAP THEM", "WATCH": "[~] THEO DOI", "REDUCE": "[-] GIAM TON"}
for _, a in alerts.iterrows():
    print(f"\n{icon[a['alert']]}  |  {a['brand']}  ({a['total_reviews']} review)")
    print(f"   {a['trend']} · ~{a['recent_avg']:.0f} review/thang · Tich cuc {a['recent_pos']}%")
    print(f"   >> {a['action']}")
print("\nDa luu: brand_alerts.csv / .parquet")
