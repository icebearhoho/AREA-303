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

