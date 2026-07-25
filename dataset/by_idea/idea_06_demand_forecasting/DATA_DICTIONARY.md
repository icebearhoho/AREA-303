# Idea #06 — Demand Forecasting — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

### `fashion_trend_clean.parquet`  —  Fashion product trend/sales 2018-2022 (incl. stockouts).

*660 rows · 20 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `product_id` | int64 | Garment id - groups the multiple photos (views) of one product. | e.g. 1001 |
| `product_name` | large_string | Product name. | e.g. Biker Jacket |
| `gender` | large_string |  | e.g. Male |
| `category` | large_string | Product category. | e.g. Shirt |
| `pattern` | large_string |  | e.g. Geometric |
| `color` | large_string | Colour. | e.g. White |
| `age_group` | large_string |  | e.g. 25-35 |
| `season` | large_string | Season the product sells in. | e.g. Spring |
| `price` | double | Selling price. | e.g. 70.36 |
| `material` | large_string |  | e.g. Synthetic |
| `sales_count` | int64 | Units sold. | e.g. 75 |
| `reviews_count` | int64 |  | e.g. 65 |
| `average_rating` | double | Average rating. | e.g. 4.9 |
| `out_of_stock_times` | int64 | How often it went out of stock. | values: `3`, `6`, `4`, `2`, `5`, `1` |
| `brand` | large_string | Brand name. | e.g. ZARA |
| `discount` | double |  | e.g. 0.2 |
| `last_stock_date` | timestamp[us] |  | e.g. 2018-01-28 00:00:00 |
| `wish_list_count` | int64 | Times added to a wishlist. | e.g. 211 |
| `month_of_sale` | int64 |  | e.g. 1 |
| `year_of_sale` | int64 |  | values: `2018`, `2019`, `2020`, `2021`, `2022` |

### `shopee_id_products_clean.parquet`  —  Shopee Indonesia cosmetics/skincare product-day snapshots (IDR), 10 shops x 3 days.

*1,419 rows · 38 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `platform` | object | Source platform. | e.g. Shopee |
| `country_code` | object | ISO country code. | e.g. id |
| `date` | object | Snapshot date (daily tracked). | e.g. 2026-07-01 |
| `shop_id` | int64 | Seller/shop id. | e.g. 1112776376 |
| `shop_slug` | object | Shop URL slug. | e.g. scoraofficial |
| `shop_name` | object | Shop display name. | e.g. Scora Official Store |
| `location` | object | Shop's registered city. | e.g. KOTA TANGERANG |
| `item_id` | int64 | Product id. | e.g. 42657274673 |
| `product_name` | object | Product title. | e.g. [Hero] 2,5% D-Panthenol Barrier Shield Moisturizer 40ml |
| `url` | object | Product page URL. | e.g. https://shopee.co.id/product/... |
| `image_url` | object | Main image URL. | e.g. https://down-id.img.susercontent.com/... |
| `images` | object | All image URLs (JSON list). | e.g. ["https://...", ...] |
| `seller_flag` | object | Seller badges (JSON list). | e.g. ["OFFICIAL_SHOP"] |
| `seller_flag_hash` | object | Badge icon hash(es). | e.g. ["id-11134258-..."] |
| `image_overlay` | object | Promo banner text overlaid on the listing image. | e.g. FSS+Promo_Xtra+Pilih_Lokal_New |
| `image_overlay_hash` | object | Overlay image hash. | e.g. id-11134258-82250-... |
| `is_ad` | bool | Whether the listing is a paid ad slot. | values: `False`, `True` |
| `is_sold_out` | bool | Out-of-stock flag. | values: `False`, `True` |
| `shopee_verified` | bool | Shopee verification badge. | values: `False`, `True` |
| `ctime` | int64 | Listing creation time (Unix epoch). | e.g. 1751611517 |
| `price` | int64 | Current selling price (IDR). | e.g. 33900 |
| `price_original` | int64 | List price before discount (IDR). | e.g. 70000 |
| `price_before_promo` | int64 | Price before the current promo/voucher stack (IDR). | e.g. 33900 |
| `discount_percent` | float64 | % off price_original; null when no discount (price==price_original). | e.g. 52.0 |
| `promotion_id` | int64 | Active promotion id. | e.g. 476081375416399 |
| `history_sold_value` | float64 | Lifetime units sold. | e.g. 10000.0 |
| `monthly_sold_value` | float64 | Units sold in the last 30 days. | e.g. 1000.0 |
| `rating` | float64 | Average star rating (0-5). | e.g. 4.91 |
| `rating_count` | int64 | Total number of ratings. | e.g. 8058 |
| `rating_count_detail` | object | Rating count by star, 1-5 (JSON list). | e.g. [6, 2, 69, 543, 7438] |
| `vouchers` | object | Active voucher labels shown on the listing (JSON list). | e.g. ["Pilih Lokal"] |
| `brand` | object | Brand name; null for ~3.6% of rows (untagged products). | e.g. SCORA |
| `brand_id` | float64 | Brand id; null paired with brand. | e.g. 4114566.0 |
| `catid` | int64 | Shopee category id. | e.g. 100630 |
| `global_catids` | object | All matching global category ids (JSON list). | e.g. [100630, 100664, 100893] |
| `liked_count` | int64 | Times added to wishlist/liked. | e.g. 2832 |
| `tier_variation_name` | object | Variant axis name (e.g. size/bundle); null when no variants. | e.g. Bundle Set |
| `tier_variation_options` | object | Variant option list; `[""]` placeholder when no variants (not a true null). | e.g. [""] |

Cleaning applied: dropped 1 junk row with sentinel price 999999999, dropped 6 always-null raw columns
(`key`, `voucher_code`, `voucher_discount`, `voucher_start_time`, `voucher_end_time`, `voucher_min_spend`),
trimmed `shop_name` whitespace.

### `shopee_id_category_list_clean.parquet`  —  Per-shop category taxonomy with daily item counts.

*237 rows · 11 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `shop_id` | int64 | Seller/shop id. | e.g. 1112776376 |
| `shop_category_id` | int64 | Shop-defined category id. | e.g. 258324793 |
| `display_name` | object | Category label as shown in-shop. | e.g. Bright Me Up ! Sunscreen SPF 40 PA ++++ |
| `total` | int64 | Number of items in this category. | e.g. 5 |
| `is_parent_category` | bool | Whether this is a top-level category. | values: `False`, `True` |
| `is_sub_category` | bool | Whether this is a child category. | values: `False`, `True` |
| `parent_shop_category_id` | float64 | Parent category id; null for top-level categories. | e.g. 258831358.0 |
| `image` | object | Category image key. | e.g. mms@id-11134204-... |
| `category_type` | int64 | Shopee-internal category type code. | e.g. 1 |
| `country_code` | object | ISO country code. | e.g. id |
| `date` | object | Snapshot date (daily tracked). | e.g. 2026-07-01 |

