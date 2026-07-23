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

### `shopee_id_images/`  —  Real Shopee Indonesia cosmetics product photos, already on disk as JPEGs (no raw-file lookup needed, unlike deepfashion).

*2,700 files across 474 product folders, 1024x1024 (or 1001x1001) JPEG, ~982MB total*

| Path / Column | Type | Meaning | Values / example |
|---|---|---|---|
| `shopee_id_images/<item_id>/` | folder | One folder per unique product. | e.g. `shopee_id_images/42657274673/` |
| `shopee_id_images/<item_id>/NN.jpg` | JPEG file | One product photo, 01-09 per product (avg 5.7). | e.g. `01.jpg` |
| `shopee_id_images_manifest.csv: item_id` | int64 | Product id — join to `shopee_id_products_clean.parquet`. | e.g. 42657274673 |
| `shopee_id_images_manifest.csv: shop_id` | int64 | Seller/shop id. | e.g. 1112776376 |
| `shopee_id_images_manifest.csv: product_name` | object | Product title. | e.g. [Hero] 2,5% D-Panthenol Barrier Shield Moisturizer 40ml |
| `shopee_id_images_manifest.csv: url` | object | Original Shopee CDN source URL. | e.g. https://down-id.img.susercontent.com/file/... |
| `shopee_id_images_manifest.csv: local_path` | object | Path to the downloaded file, or `FAILED`. | e.g. `shopee_id_images/42657274673/01.jpg` |

## How to load
```python
import pandas as pd
from PIL import Image

deepfashion_attributes = pd.read_parquet(r"deepfashion_attributes_clean.parquet")   # or pd.read_csv(r"deepfashion_attributes_clean.csv")

# shopee_id: pixels are already local, no raw-file join needed
shopee_manifest = pd.read_csv(r"shopee_id_images_manifest.csv")
img = Image.open(shopee_manifest["local_path"].iloc[0])
```

## Watch out for
- The clean deepfashion attributes table has NO pixels — load images from raw, keyed by item_ID.
  shopee_id_images is the opposite: pixels are already on disk, no raw lookup needed.
- deepfashion rows are images (multiple views per garment); use product_id to dedupe to products.
  shopee_id_images is already folder-per-product (item_id), 1-9 images each.
- deepfashion = clothing only, English/global; shopee_id_images = cosmetics only, Indonesian market —
  they cover different product categories, don't assume visual similarity crosses between them
- shopee_id_images is small (474 products) — good for testing/demo-ing the cosmetics-search path,
  not enough alone to train an embedding model from scratch (use CLIP zero-shot, not fine-tuning)

## Suggested first steps
1. Load images from the RAW deepfashion parquet (keyed by item_ID)
2. Encode with CLIP, build a FAISS index
3. Query by image; group hits by product_id
4. Repeat the CLIP+FAISS pipeline on shopee_id_images to demo visual search on the cosmetics category
   (deepfashion has zero cosmetics coverage) — join manifest.csv to shopee_id_products_clean.parquet for
   price/brand/rating metadata alongside search results

---
*Currencies/languages differ across datasets — see notes above. Cleaning is reproducible via clean_pipeline*.py; full project overview in DATA_REPORT.md.*
