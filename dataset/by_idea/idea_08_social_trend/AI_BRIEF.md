# AI Brief — Idea #08: Social Trend

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Detect rising fashion/beauty topics and their sentiment from social posts.

## Recommended approach
- BERTopic (+ PhoBERT backbone)
- Prophet for topic popularity curves

## Datasets for this idea

### `tweet_sentiment_clean.parquet`  —  Multilingual tweet sentiment (8 languages, no Vietnamese).

*24,264 rows · 5 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `text` | large_string | Text content. | e.g. نوال الزغبي (الشاب خالد ليس عالمي) هههههههه أتفرجي على ها ال… |
| `label` | int64 | Class label (see decoded values). | `0`=negative; `1`=neutral; `2`=positive |
| `label_name` | large_string | Human-readable form of label. | e.g. negative |
| `language` | large_string | Language of the text. | e.g. arabic |
| `split` | large_string | train / dev / test split. | e.g. test |

## How to load
```python
import pandas as pd
tweet_sentiment = pd.read_parquet(r"tweet_sentiment_clean.parquet")   # or pd.read_csv(r"tweet_sentiment_clean.csv")
```

## Watch out for
- tweet_sentiment has NO Vietnamese — transfer via PhoBERT or add a VN social source
- The TikTok source was not collected

## Suggested first steps
1. Train a sentiment model on tweet_sentiment (0/1/2)
2. Topic-model posts with BERTopic
3. Track each topic over time with Prophet to catch rising trends

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
