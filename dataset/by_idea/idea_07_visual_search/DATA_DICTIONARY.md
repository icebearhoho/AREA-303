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

