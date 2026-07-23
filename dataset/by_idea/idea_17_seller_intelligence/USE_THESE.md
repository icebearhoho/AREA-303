# Idea #17 - Seller Intelligence

Datasets for this idea (parquet + csv copied into this folder):

- **tiki** -> `tiki_catalog_clean.parquet` (+ .csv)
- **deepfashion** -> `deepfashion_attributes_clean.parquet` (+ .csv)
- **shopee_id_shop_info** -> `shopee_id_shop_info_clean.parquet` (+ .csv) — real seller telemetry, 10 shops, 1 row/shop (rating, follower_count, response_rate, etc.)
- **shopee_id_products** -> `shopee_id_products_clean.parquet` (+ .csv) — join on shop_id for per-seller product/pricing/sales behavior, 1,419 rows
