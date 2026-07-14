"""
PHASE 3-REAL - Gom du lieu THAT tu Sephora reviews (thay cho BERTopic bia).
Thuc the theo doi = BRAND (chinh) + PRODUCT (drill). Moi con so tra nguoc ve data that.
"""
import sys
import pandas as pd
import config

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ===== 1. Load Sephora reviews (THAT: timestamp + sentiment + brand) =====
df = pd.read_parquet(config.SEPHORA_PARQUET)
print("Tong review:", f"{len(df):,}")
print("Khoang thoi gian THAT:", df["submission_time"].min().date(), "->", df["submission_time"].max().date())

df["month"] = df["submission_time"].values.astype("datetime64[M]")   # ve dau thang
df["is_pos"] = (df["sentiment"] == "positive").astype(int)

# ===== 2. Gom theo BRAND x thang =====
brand_monthly = (df.groupby(["brand_name", "month"])
                   .agg(volume=("review_text", "size"),
                        pct_positive=("is_pos", "mean"),
                        avg_rating=("rating", "mean"))
                   .reset_index())
brand_monthly["pct_positive"] = (brand_monthly["pct_positive"] * 100).round(1)
brand_monthly["avg_rating"] = brand_monthly["avg_rating"].round(2)
brand_monthly.to_parquet(config.OUTPUT_DIR / "brand_monthly.parquet")

# ===== 3. Gom theo PRODUCT x thang (de drill xuong sau) =====
prod_monthly = (df.groupby(["brand_name", "product_name", "month"])
                  .agg(volume=("review_text", "size"),
                       pct_positive=("is_pos", "mean"),
                       avg_rating=("rating", "mean"))
                  .reset_index())
prod_monthly["pct_positive"] = (prod_monthly["pct_positive"] * 100).round(1)
prod_monthly["avg_rating"] = prod_monthly["avg_rating"].round(2)
prod_monthly.to_parquet(config.OUTPUT_DIR / "product_monthly.parquet")

# ===== 4. Kiem tra =====
print("\nbrand_monthly:", brand_monthly.shape, "| so brand:", brand_monthly["brand_name"].nunique())
print("product_monthly:", prod_monthly.shape, "| so product:", prod_monthly["product_name"].nunique())
print("\nDa luu: brand_monthly.parquet, product_monthly.parquet")
print("\nVi du - Glow Recipe theo thang (6 thang dau):")
demo = brand_monthly[brand_monthly["brand_name"] == "Glow Recipe"].head(6)
print(demo.to_string(index=False))
