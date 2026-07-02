# AI Brief — Idea #17: Seller Intelligence

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Give sellers competitive intelligence: pricing, visual product matches, and review sentiment.

## Recommended approach
- CLIP + FAISS (visual matching) + LangChain multi-agent + Gemini

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


### `deepfashion_attributes_clean.parquet`  —  DeepFashion image-attributes table. Rows are IMAGES (several views per garment) - ~12,889 unique products across 52,591 images. Pixels stay in raw, keyed by item_ID.

*52,591 rows · 8 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `product_id` | large_string | Garment id - groups the multiple photos (views) of one product. | e.g. id_00000080_01 |
| `view` | string | Camera view of the photo: front / side / back / additional / full / flat. | e.g. front |
| `item_ID` | large_string | Per-image id (joins to the actual image in the raw parquet). | e.g. MEN_Denim_id_00000080_01_1_front |
| `category1` | large_string |  | e.g. men |
| `category2` | large_string |  | e.g. denim |
| `category3` | large_string |  | e.g. vests |
| `color` | large_string | Colour. | e.g. Black |
| `description` | large_string | Product/description text. | e.g. Give your trusty blues the day off. In a clean wash, these s… |

## How to load
```python
import pandas as pd
tiki_catalog = pd.read_parquet(r"tiki_catalog_clean.parquet")   # or pd.read_csv(r"tiki_catalog_clean.csv")
deepfashion_attributes = pd.read_parquet(r"deepfashion_attributes_clean.parquet")   # or pd.read_csv(r"deepfashion_attributes_clean.csv")
```

## Watch out for
- deepfashion rows are images (12,889 products) — load pixels from raw, keyed by item_ID
- tiki is the market benchmark (VND)

## Suggested first steps
1. Match competitor products visually via deepfashion/CLIP (load pixels from raw)
2. Benchmark prices/ratings against the tiki market
3. Synthesize a Vietnamese seller report with Gemini agents

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
