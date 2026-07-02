# AI Brief — Idea #05: Fake Review

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Detect spam / fake reviews to keep the review system trustworthy.

## Recommended approach
- PhoBERT + metadata features (HuggingFace + scikit-learn)
- ViSoBERT for VN social text

## Datasets for this idea

### `vispam_clean.parquet`  —  Vietnamese e-commerce spam/review dataset (UIT ViSpamReviews v2).

*19,870 rows · 12 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `comment` | large_string | Review text (Vietnamese). | e.g. sản phẩm đúng quảng cáo. giao hàng hơi chậm nhg vẫn cho 5 sa… |
| `rating` | int64 | Star rating given (1-5). | values: `5`, `2`, `4`, `1`, `3` |
| `category` | large_string | Product category. | e.g. Đồ Chơi |
| `in_domain` | bool | True if category is fashion/beauty/footwear (your focus). | values: `False`, `True` |
| `label` | int64 | Class label (see decoded values). | `0`=not spam; `1`=spam |
| `spam_label_name` | large_string | Human-readable form of the binary spam label. | e.g. not_spam |
| `spam_label` | int64 | Type of spam (see decoded values). | `0`=no-spam; `1`=SPAM-1 fake review (deceptive neg. comments / fake seeding); `2`=SPAM-2 talks only about brand/seller, not product quality; `3`=SPAM-3 non-review (irrelevant, doesn't mention the product) |
| `product_name` | large_string | Product name. | e.g. Nước Xả Làm Mềm Vải Comfort Chăm Sóc Dịu Nhẹ Cho Da Nhạy Cảm… |
| `description` | large_string | Product/description text. | e.g. Số lượng quà tặng sẽ thay đổi tùy theo chương … |
| `num_sold` | int64 | Units sold. | e.g. 535 |
| `num_review` | int64 | Number of reviews. | e.g. 75 |
| `split` | large_string | train / dev / test split. | e.g. train |


### `fake_reviews_clean.parquet`  —  English computer-generated vs genuine reviews.

*40,432 rows · 6 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `category` | large_string | Product category. | e.g. Home_and_Kitchen_5 |
| `rating` | double | Star rating given (1-5). | e.g. 5.0 |
| `label` | large_string | Class label (see decoded values). | `CG`=computer-generated (fake); `OR`=original (genuine) |
| `label_name` | large_string | Human-readable form of label. | e.g. fake |
| `is_fake` | int64 | 1 = fake (computer-generated), 0 = genuine. | values: `1`, `0` |
| `text` | large_string | Text content. | e.g. Love this!  Well made, sturdy, and very comfortable.  I love… |


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

## How to load
```python
import pandas as pd
vispam = pd.read_parquet(r"vispam_clean.parquet")   # or pd.read_csv(r"vispam_clean.csv")
fake_reviews = pd.read_parquet(r"fake_reviews_clean.parquet")   # or pd.read_csv(r"fake_reviews_clean.csv")
sephora_reviews = pd.read_parquet(r"sephora_reviews_clean.parquet")   # or pd.read_csv(r"sephora_reviews_clean.csv")
```

## Watch out for
- spam_label: 0 no-spam, 1 fake, 2 brand-only, 3 non-review
- Mixed Vietnamese (vispam) + English (fake_reviews) — use multilingual or train separately

## Suggested first steps
1. Target = vispam label (0/1) or spam_label (type); add metadata (num_sold, num_review)
2. Add fake_reviews (EN) + sephora for volume
3. Fine-tune; evaluate macro-F1

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
