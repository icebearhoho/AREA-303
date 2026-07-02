# AI Brief — Idea #09: Content Generator

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Auto-generate accurate Vietnamese product descriptions.

## Recommended approach
- Gemini 1.5 Pro via LangChain RAG
- Llama 3.1 8B local fallback

## Datasets for this idea

### `wikipedia_vi_clean.parquet`  —  Vietnamese Wikipedia corpus (RAG knowledge base).

*1,288,680 rows · 5 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `id` | large_string |  | e.g. 4 |
| `url` | large_string | Source URL. | e.g. https://vi.wikipedia.org/wiki/Internet%20Society |
| `title` | large_string | Article/title text. | e.g. Internet Society |
| `text` | large_string | Text content. | e.g. Internet Society hay ISOC là một tổ chức quốc tế hoạt động p… |
| `char_count` | int64 |  | e.g. 1218 |


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
wikipedia_vi = pd.read_parquet(r"wikipedia_vi_clean.parquet")   # or pd.read_csv(r"wikipedia_vi_clean.csv")
tiki_catalog = pd.read_parquet(r"tiki_catalog_clean.parquet")   # or pd.read_csv(r"tiki_catalog_clean.csv")
```

## Watch out for
- wikipedia is large (1.29M rows) — chunk text for retrieval
- Requires a Gemini API key

## Suggested first steps
1. Use wikipedia_vi as the knowledge base + tiki product specs
2. RAG: retrieve context, generate the description with Gemini
3. Ground every output in real product fields

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
