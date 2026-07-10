# AI Brief — Idea #14: Negotiation

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
A chatbot that negotiates price with buyers within seller guardrails.

## Recommended approach
- LangChain + Gemini (dialogue + memory)
- PhoBERT intent classifier (accept / counter / abandon)

## Datasets for this idea

### `craigslist_clean.parquet`  —  Buyer/seller price-negotiation dialogues.

*6,682 rows · 10 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `split` | large_string | train / dev / test split. | e.g. test |
| `item_category` | large_string | Category of the item being negotiated. | e.g. electronics |
| `item_list_price` | float | Listed price in the negotiation. | e.g. 65.0 |
| `n_turns` | int64 | Number of dialogue turns. | e.g. 4 |
| `dialogue_text` | large_string | Full negotiation dialogue (turns joined). | e.g. I am interested in purchasing this item, but since it is use… |
| `agent_info` | struct<Bottomline: list<element: string>, Role: list<element: string>, Target: list<element: float>> |  | (nested struct/list) |
| `agent_turn` | list<element: int32> |  | (nested struct/list) |
| `dialogue_acts` | struct<intent: list<element: string>, price: list<element: float>> |  | (nested struct/list) |
| `utterance` | list<element: string> |  | (nested struct/list) |
| `items` | struct<Category: list<element: string>, Images: list<element: string>, Price: list<element: float>, Description: list<element: string>, Title: list<element: string>> |  | (nested struct/list) |


### `deal_no_deal_clean.parquet`  —  Deal or No Deal multi-issue bargaining dialogues (Facebook AI). 2nd source for #14, non-gated replacement for ChicagoHAI.

*20,406 rows · 6 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `split` | large_string | train / dev / test split. | e.g. test |
| `dialogue_text` | large_string | Full negotiation dialogue (turns joined). | e.g. THEM: i need that ball so bad ! what do you want ?
 YOU: i m… |
| `n_turns` | double | Number of dialogue turns. | e.g. 6.0 |
| `output` | large_string | Final agreed item allocation (the deal outcome). | e.g. item0=2 item1=3 item2=0 item0=0 item1=0 item2=1 |
| `my_item_counts` | list<element: int32> | How many of each item are available. | (nested struct/list) |
| `my_item_values` | list<element: int32> | This agent's point value for each item. | (nested struct/list) |

## How to load
```python
import pandas as pd
craigslist = pd.read_parquet(r"craigslist_clean.parquet")   # or pd.read_csv(r"craigslist_clean.csv")
deal_no_deal = pd.read_parquet(r"deal_no_deal_clean.parquet")   # or pd.read_csv(r"deal_no_deal_clean.csv")
```

## Watch out for
- Both sources are English negotiation patterns — adapt to Vietnamese
- deal_no_deal is multi-issue item bargaining; craigslist is price haggling — use both for varied strategies

## Suggested first steps
1. Study craigslist + deal_no_deal dialogues (dialogue_text, n_turns)
2. Build an intent classifier; define price floor/ceiling guardrails
3. Wire a LangChain agent with conversation memory

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
