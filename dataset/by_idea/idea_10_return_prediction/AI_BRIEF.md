# AI Brief — Idea #10: Return Prediction

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Predict which orders are likely to be returned.

## Recommended approach
- XGBoost + SHAP
- SDV (synthetic data) if real return labels are missing

## Datasets for this idea

### `kanchana_zalando_clean.parquet`  —  Zalando women's clothing catalog (GBP).

*10,947 rows · 8 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `name` | large_string |  | e.g. Blouse - off white |
| `brand` | large_string | Brand name. | e.g. Anna Field |
| `original_price_gbp` | double | Original price in GBP. | e.g. 25.99 |
| `promo_price_gbp` | double | Promotional price in GBP. | e.g. 22.0 |
| `discount_pct` | double | Discount percent off the original price. | e.g. 15.0 |
| `size_count` | int64 | Number of available sizes. | e.g. 10 |
| `sizes` | large_string | Available sizes (comma-joined). | e.g. 6, 8, 10, 12, 16, 18, 20, 22, 24, 26 |
| `skus` | large_string |  | e.g. AN621E0AO-A110034000, AN621E0AO-A110036000, AN621E0AO-A11003… |


### `fashion_retail_sales_clean.parquet`  —  Fashion retail transactions (USD).

*3,400 rows · 6 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `customer_id` | int64 | Customer reference id. | e.g. 4018 |
| `item_purchased` | large_string | Item bought. | e.g. Handbag |
| `purchase_amount_usd` | double | Purchase amount in USD. | e.g. 4619.0 |
| `date_purchase` | timestamp[us] | Purchase date. | e.g. 2023-02-05 00:00:00 |
| `review_rating` | double | Reviewer's star rating. | e.g. 2.0 |
| `payment_method` | large_string | Payment method used. | e.g. Credit Card |

## How to load
```python
import pandas as pd
kanchana_zalando = pd.read_parquet(r"kanchana_zalando_clean.parquet")   # or pd.read_csv(r"kanchana_zalando_clean.csv")
fashion_retail_sales = pd.read_parquet(r"fashion_retail_sales_clean.parquet")   # or pd.read_csv(r"fashion_retail_sales_clean.csv")
```

## Watch out for
- kanchana = GBP, retail_sales = USD
- No explicit return flag — may need SDV/synthetic labels; retail_sales has 324 null ratings

## Suggested first steps
1. Use kanchana (sizing/price) + fashion_retail_sales (transactions)
2. Engineer return-risk features (size variance, price, rating)
3. Train XGBoost; SHAP for drivers

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
