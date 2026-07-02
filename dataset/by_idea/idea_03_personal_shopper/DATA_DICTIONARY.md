# Idea #03 — Personal Shopper — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

