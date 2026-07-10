# Idea #08 — Social Trend — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

### `tweet_sentiment_clean.parquet`  —  Multilingual tweet sentiment (8 languages, no Vietnamese).

*24,264 rows · 5 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `text` | large_string | Text content. | e.g. نوال الزغبي (الشاب خالد ليس عالمي) هههههههه أتفرجي على ها ال… |
| `label` | int64 | Class label (see decoded values). | `0`=negative; `1`=neutral; `2`=positive |
| `label_name` | large_string | Human-readable form of label. | e.g. negative |
| `language` | large_string | Language of the text. | e.g. arabic |
| `split` | large_string | train / dev / test split. | e.g. test |

### `uit_vsfc_clean.parquet`  —  UIT-VSFC: Vietnamese sentiment corpus (~16k sentences, sentiment + topic labels). Fills the Vietnamese-language gap for #08.

*16,175 rows · 6 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `text` | large_string | Text content. | e.g. nói tiếng anh lưu loát . |
| `sentiment` | int64 | Sentiment derived from rating (see decoded values). | `0`=negative; `1`=neutral; `2`=positive |
| `sentiment_name` | large_string | Human-readable sentiment. | e.g. positive |
| `topic` | int64 | Feedback topic (coded). | `0`=lecturer; `1`=training_program; `2`=facility; `3`=others |
| `topic_name` | large_string | Human-readable feedback topic. | e.g. lecturer |
| `split` | large_string | train / dev / test split. | e.g. train |

### `google_trends_clean.parquet`  —  Google Trends weekly search interest (0-100) for 20 Vietnamese fashion/beauty keywords, Jul 2025-Jul 2026. Long format. The live trend signal for #08.

*1,060 rows · 4 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `date` | timestamp[ns] | Week (Google Trends weekly sampling). | e.g. 2025-07-06 00:00:00 |
| `keyword` | string | Search term tracked. | e.g. cushion |
| `interest` | int64 | Google Trends interest index (0-100, per keyword). | e.g. 11 |
| `group` | string | Keyword group: fashion or beauty. | e.g. beauty |

