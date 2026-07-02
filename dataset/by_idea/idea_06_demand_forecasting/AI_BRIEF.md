# AI Brief — Idea #06: Demand Forecasting

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Forecast product demand to plan stock and promotions.

## Recommended approach
- Prophet (seasonal baseline)
- TimesFM / Chronos zero-shot before training

## Datasets for this idea

### `fashion_trend_clean.parquet`  —  Fashion product trend/sales 2018-2022 (incl. stockouts).

*660 rows · 20 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `product_id` | int64 | Garment id - groups the multiple photos (views) of one product. | e.g. 1001 |
| `product_name` | large_string | Product name. | e.g. Biker Jacket |
| `gender` | large_string |  | e.g. Male |
| `category` | large_string | Product category. | e.g. Shirt |
| `pattern` | large_string |  | e.g. Geometric |
| `color` | large_string | Colour. | e.g. White |
| `age_group` | large_string |  | e.g. 25-35 |
| `season` | large_string | Season the product sells in. | e.g. Spring |
| `price` | double | Selling price. | e.g. 70.36 |
| `material` | large_string |  | e.g. Synthetic |
| `sales_count` | int64 | Units sold. | e.g. 75 |
| `reviews_count` | int64 |  | e.g. 65 |
| `average_rating` | double | Average rating. | e.g. 4.9 |
| `out_of_stock_times` | int64 | How often it went out of stock. | values: `3`, `6`, `4`, `2`, `5`, `1` |
| `brand` | large_string | Brand name. | e.g. ZARA |
| `discount` | double |  | e.g. 0.2 |
| `last_stock_date` | timestamp[us] |  | e.g. 2018-01-28 00:00:00 |
| `wish_list_count` | int64 | Times added to a wishlist. | e.g. 211 |
| `month_of_sale` | int64 |  | e.g. 1 |
| `year_of_sale` | int64 |  | values: `2018`, `2019`, `2020`, `2021`, `2022` |

## How to load
```python
import pandas as pd
fashion_trend = pd.read_parquet(r"fashion_trend_clean.parquet")   # or pd.read_csv(r"fashion_trend_clean.csv")
```

## Watch out for
- fashion_trend is small (660) and looks synthetic — prototype only

## Suggested first steps
1. Use fashion_trend (sales_count, season, month/year_of_sale)
2. Fit Prophet for seasonality; try TimesFM zero-shot
3. Add live Google Trends (pytrends) as an external signal

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
