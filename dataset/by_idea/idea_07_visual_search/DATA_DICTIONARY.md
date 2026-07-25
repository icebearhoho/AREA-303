# Idea #07 — Visual Search — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

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

### `shopee_id_images/`  —  Real Shopee Indonesia cosmetics product photos, downloaded locally (not a table — a folder of JPEGs, pixels already on disk, no raw-parquet lookup needed).

*2,700 files across 474 product folders*

| Path / Column | Type | Meaning | Values / example |
|---|---|---|---|
| `shopee_id_images/<item_id>/` | folder | One folder per unique product. | e.g. `shopee_id_images/42657274673/` |
| `shopee_id_images/<item_id>/NN.jpg` | JPEG file | One product photo, 01-09 per product (avg 5.7). 1024x1024 or 1001x1001, RGB. | e.g. `01.jpg` |
| `shopee_id_images_manifest.csv: item_id` | int64 | Product id — join to `shopee_id_products_clean.parquet`'s `item_id`. | e.g. 42657274673 |
| `shopee_id_images_manifest.csv: shop_id` | int64 | Seller/shop id. | e.g. 1112776376 |
| `shopee_id_images_manifest.csv: product_name` | object | Product title (for eyeballing without opening images). | e.g. [Hero] 2,5% D-Panthenol Barrier Shield Moisturizer 40ml |
| `shopee_id_images_manifest.csv: url` | object | Original Shopee CDN source URL. | e.g. https://down-id.img.susercontent.com/file/... |
| `shopee_id_images_manifest.csv: local_path` | object | Path to the downloaded file, or `FAILED`. | e.g. `shopee_id_images/42657274673/01.jpg` |

Downloaded via `code/download_shopee_id_images.py` (run locally — Shopee's image CDN is blocked from the
Cowork sandbox's network allowlist). All 2,700/2,700 downloaded successfully, 0 failures, ~982MB total.

