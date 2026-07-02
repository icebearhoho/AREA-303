# AI Brief — Idea #11: Recsys

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Recommend cosmetics/fashion products to users.

## Recommended approach
- BERT4Rec (sequential, RecBole)
- LightFM (hybrid collaborative + content)

## Datasets for this idea

### `sephora_reviews_clean.parquet`  —  Sephora cosmetics reviews (English, ~1.09M).

*1,092,967 rows · 15 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `author_id` | large_string | Anonymized reviewer id. | e.g. 1741593524 |
| `rating` | int64 | Star rating given (1-5). | values: `5`, `1`, `4`, `2`, `3` |
| `is_recommended` | double | 1 if the reviewer recommends the product, else 0. | e.g. 1.0 |
| `helpfulness` | double | Helpfulness ratio of the review. | e.g. 1.0 |
| `total_feedback_count` | int64 |  | e.g. 2 |
| `submission_time` | timestamp[us] | When the review was submitted. | e.g. 2023-02-01 00:00:00 |
| `review_text` | large_string | Review body text. | e.g. I use this with the Nudestix “Citrus Clean Balm & Make-Up Me… |
| `review_title` | large_string | Review title. | e.g. Taught me how to double cleanse! |
| `skin_tone` | large_string | Reviewer's skin tone. | e.g. light |
| `skin_type` | large_string | Reviewer's skin type. | e.g. dry |
| `product_id` | large_string | Garment id - groups the multiple photos (views) of one product. | e.g. P504322 |
| `product_name` | large_string | Product name. | e.g. Gentle Hydra-Gel Face Cleanser |
| `brand_name` | large_string | Brand name. | e.g. NUDESTIX |
| `price_usd` | double | Price in USD. | e.g. 19.0 |
| `sentiment` | large_string | Sentiment derived from rating (see decoded values). | `negative`=1-2 stars; `neutral`=3 stars; `positive`=4-5 stars |


### `sephora_products_clean.parquet`  —  Sephora product catalog (join to reviews on product_id).

*8,494 rows · 27 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `product_id` | large_string | Garment id - groups the multiple photos (views) of one product. | e.g. P473671 |
| `product_name` | large_string | Product name. | e.g. Fragrance Discovery Set |
| `brand_id` | int64 | Brand id. | e.g. 6342 |
| `brand_name` | large_string | Brand name. | e.g. 19-69 |
| `loves_count` | int64 | Times 'loved' on Sephora. | e.g. 6320 |
| `rating` | double | Star rating given (1-5). | e.g. 3.6364 |
| `reviews` | double |  | e.g. 11.0 |
| `size` | large_string | Available sizes (comma-joined). | e.g. 3.4 oz/ 100 mL |
| `variation_type` | large_string |  | e.g. Size + Concentration + Formulation |
| `variation_value` | large_string |  | e.g. 3.4 oz/ 100 mL |
| `variation_desc` | large_string |  | e.g. rosy-brown |
| `ingredients` | large_string | Product ingredients list. | e.g. ['Capri Eau de Parfum:', 'Alcohol Denat. (SD Alcohol 39C), P… |
| `price_usd` | double | Price in USD. | e.g. 35.0 |
| `value_price_usd` | double |  | e.g. 42.0 |
| `sale_price_usd` | double |  | e.g. 82.0 |
| `limited_edition` | int64 |  | values: `0`, `1` |
| `new` | int64 |  | values: `0`, `1` |
| `online_only` | int64 |  | values: `1`, `0` |
| `out_of_stock` | int64 |  | values: `0`, `1` |
| `sephora_exclusive` | int64 |  | values: `0`, `1` |
| `highlights` | large_string |  | e.g. ['Unisex/ Genderless Scent', 'Warm &Spicy Scent', 'Woody & E… |
| `primary_category` | large_string |  | e.g. Fragrance |
| `secondary_category` | large_string |  | e.g. Value & Gift Sets |
| `tertiary_category` | large_string |  | e.g. Perfume Gift Sets |
| `child_count` | int64 |  | e.g. 0 |
| `child_max_price` | double |  | e.g. 85.0 |
| `child_min_price` | double |  | e.g. 30.0 |

## How to load
```python
import pandas as pd
sephora_reviews = pd.read_parquet(r"sephora_reviews_clean.parquet")   # or pd.read_csv(r"sephora_reviews_clean.csv")
sephora_products = pd.read_parquet(r"sephora_products_clean.parquet")   # or pd.read_csv(r"sephora_products_clean.csv")
```

## Watch out for
- sephora rating is skewed — use the sentiment column or implicit signals
- ~9% duplicate reviews — dedupe first

## Suggested first steps
1. Build user-item interactions from sephora_reviews + content from sephora_products
2. LightFM for cold-start, BERT4Rec for purchase sequences
3. Evaluate recall@k / NDCG

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
