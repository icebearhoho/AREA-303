# AI Brief — Idea #01: Review Sentiment

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Classify the sentiment of Vietnamese product reviews (positive / neutral / negative) so sellers see how customers feel.

## Recommended approach
- Primary: PhoBERT or ViSoBERT fine-tuned (HuggingFace Transformers + PyTorch)
- Baseline: multilingual-e5 embeddings + logistic regression

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


### `shopee_clean.parquet`  —  Real Shopee Vietnam product reviews with sentiment labels.

*9,599 rows · 4 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `id` | large_string |  | e.g. 74263765409 |
| `text` | large_string | Text content. | e.g. Hương vị:thom  Chắc do bên giao hàng bị vỡ mấy gói |
| `rating` | int64 | Star rating given (1-5). | e.g. 3 |
| `label` | large_string | Class label (see decoded values). | `negative`=rating <=3; `positive`=rating >=4 |

## How to load
```python
import pandas as pd
vispam = pd.read_parquet(r"vispam_clean.parquet")   # or pd.read_csv(r"vispam_clean.csv")
shopee = pd.read_parquet(r"shopee_clean.parquet")   # or pd.read_csv(r"shopee_clean.csv")
```

## Watch out for
- Vietnamese text — use a Vietnamese/multilingual model, not English BERT
- shopee labels are binary (3★ counts as negative); vispam keeps rating 1–5
- Filter vispam with in_domain==True if you want fashion/beauty/footwear only

## Suggested first steps
1. Combine vispam + shopee text; map ratings/labels to one sentiment scheme
2. Fine-tune PhoBERT; evaluate with macro-F1 (robust to class imbalance)
3. Hold out a test split and compare against the baseline

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
