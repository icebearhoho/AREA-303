# Idea #01 — Review Sentiment — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

