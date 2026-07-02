# Idea #14 — Negotiation — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

