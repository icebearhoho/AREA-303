# AI Brief — Idea #02: Dynamic Pricing

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Recommend/forecast optimal product prices from catalog price + demand signals.

## Recommended approach
- XGBoost / LightGBM + Optuna (price regression)
- LSTM for competitor price-trend

## Datasets for this idea

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


### `asos_catalog_clean.parquet`  —  ASOS clothing catalog (GBP).

*30,501 rows · 9 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `url` | large_string | Source URL. | e.g. https://www.asos.com/stradivarius/stradivarius-faux-leather-… |
| `name` | large_string |  | e.g. New Look trench coat in camel |
| `size` | large_string | Available sizes (comma-joined). | e.g. UK 4,UK 6,UK 8,UK 10,UK 12,UK 14 - Out of stock,UK 16,UK 18 |
| `category` | large_string | Product category. | e.g. New Look trench coat in camel |
| `price` | double | Selling price. | e.g. 49.99 |
| `color` | large_string | Colour. | e.g. Neutral |
| `sku` | double | Stock-keeping unit id. | e.g. 126704571.0 |
| `description` | large_string | Product/description text. | e.g. [{'Product Details': 'Coats & Jackets by New LookLow-key lay… |
| `images` | large_string | Image URL(s). | e.g. ['https://images.asos-media.com/products/new-look-trench-coa… |

## How to load
```python
import pandas as pd
tiki_catalog = pd.read_parquet(r"tiki_catalog_clean.parquet")   # or pd.read_csv(r"tiki_catalog_clean.csv")
asos_catalog = pd.read_parquet(r"asos_catalog_clean.parquet")   # or pd.read_csv(r"asos_catalog_clean.csv")
```

## Watch out for
- tiki = VND, asos = GBP — never mix currencies
- tiki.quantity_sold is the demand proxy; discount_pct already derived

## Suggested first steps
1. Use tiki (VND) and asos (GBP) catalogs; build price / discount / quantity features
2. Model price vs quantity_sold with XGBoost
3. Add time-trend features if modeling over time

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
