# Idea #06 — Demand Forecasting — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

