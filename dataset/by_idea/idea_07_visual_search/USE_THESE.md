# Idea #07 - Visual Search

Datasets for this idea (parquet + csv copied into this folder):

- **deepfashion** -> `deepfashion_attributes_clean.parquet` (+ .csv)
- **shopee_id_images** -> `shopee_id_images/<item_id>/01.jpg, 02.jpg, ...` (2,700 real product photos,
  474 cosmetics products, 1024x1024 JPEG) + `shopee_id_images_manifest.csv` (item_id -> local path mapping,
  join to `shopee_id_products_clean.parquet` in `dataset/processed/02_transactions_behavior/` for product
  name/brand/category context)
