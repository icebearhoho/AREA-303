# AI Brief — Idea #07: Visual Search

*Paste this whole file into your AI assistant. It contains the idea, the recommended approach, the exact datasets (with decoded columns), how to load them, the pitfalls, and first steps.*

## Goal
Find visually similar fashion items from an image query.

## Recommended approach
- CLIP ViT-L/14 + FAISS (IVFFlat index)

## Datasets for this idea

### `deepfashion_attributes_clean.parquet`  —  DeepFashion image-attributes table. Rows are IMAGES (several views per garment) - ~12,889 unique products across 52,591 images. Pixels stay in raw, keyed by item_ID.

*52,591 rows · 8 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `product_id` | large_string | Garment id - groups the multiple photos (views) of one product. | e.g. id_00000080_01 |
| `view` | string | Camera view of the photo: front / side / back / additional / full / flat. | e.g. front |
| `item_ID` | large_string | Per-image id (joins to the actual image in the raw parquet). | e.g. MEN_Denim_id_00000080_01_1_front |
| `category1` | large_string |  | e.g. men |
| `category2` | large_string |  | e.g. denim |
| `category3` | large_string |  | e.g. vests |
| `color` | large_string | Colour. | e.g. Black |
| `description` | large_string | Product/description text. | e.g. Give your trusty blues the day off. In a clean wash, these s… |

## How to load
```python
import pandas as pd
deepfashion_attributes = pd.read_parquet(r"deepfashion_attributes_clean.parquet")   # or pd.read_csv(r"deepfashion_attributes_clean.csv")
```

## Watch out for
- The clean attributes table has NO pixels — load images from raw
- Rows are images (multiple views per garment); use product_id to dedupe to products

## Suggested first steps
1. Load images from the RAW deepfashion parquet (keyed by item_ID)
2. Encode with CLIP, build a FAISS index
3. Query by image; group hits by product_id

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
