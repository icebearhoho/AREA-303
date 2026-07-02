# AI Brief — Idea #15: Price Sensitivity

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Estimate how demand responds to price (price elasticity).

## Recommended approach
- Double ML / EconML (causal estimate)
- SHAP on XGBoost

## Datasets for this idea

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


### `tiki_catalog_clean.parquet`  —  Tiki.vn fashion catalog (VND) - the target platform.

*41,576 rows · 18 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `id` | int64 |  | e.g. 179731375 |
| `name` | large_string |  | e.g. Balo nữ da dầy thời trang unisex màu sắc tươi sáng TA63 |
| `description` | large_string | Product/description text. | e.g.   Balo nữ da dầy thời trang unisex màu sắc tươi sáng TA63   … |
| `original_price` | int64 | List/original price (before discount). | e.g. 14250 |
| `price` | int64 | Selling price. | e.g. 14250 |
| `fulfillment_type` | large_string | Fulfilment method. | e.g. dropship |
| `brand` | large_string | Brand name. | e.g. OEM |
| `review_count` | int64 | Number of reviews. | e.g. 0 |
| `rating_average` | double | Average star rating. | e.g. 0.0 |
| `favourite_count` | int64 | Times favourited. | values: `0` |
| `pay_later` | bool |  | values: `False`, `True` |
| `current_seller` | large_string | Seller name. | e.g. Thiên Ân Balo |
| `number_of_images` | int64 |  | e.g. 10 |
| `vnd_cashback` | int64 |  | e.g. 0 |
| `has_video` | bool |  | values: `False`, `True` |
| `category` | large_string | Product category. | e.g. Balo nữ |
| `quantity_sold` | int64 | Units sold. | e.g. 0 |
| `discount_pct` | double | Discount percent off the original price. | e.g. 0.0 |

## How to load
```python
import pandas as pd
fashion_retail_sales = pd.read_parquet(r"fashion_retail_sales_clean.parquet")   # or pd.read_csv(r"fashion_retail_sales_clean.csv")
tiki_catalog = pd.read_parquet(r"tiki_catalog_clean.parquet")   # or pd.read_csv(r"tiki_catalog_clean.csv")
```

## Watch out for
- tiki = VND, retail_sales = USD
- retail_sales is small (3,400) — elasticity estimates will be noisy

## Suggested first steps
1. Use fashion_retail_sales + tiki price/quantity
2. Estimate elasticity controlling for confounders (promo, season) with EconML
3. Explain with SHAP

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
