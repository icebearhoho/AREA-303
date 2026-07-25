# Idea #15 — Price Sensitivity — Data Dictionary

Columns of each dataset used by this idea. Coded values are decoded.

### `fashion_retail_sales_clean.parquet`  —  Fashion retail transactions (USD).

*3,400 rows · 6 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `customer_id` | int64 | Customer reference id. | e.g. 4018 |
| `item_purchased` | large_string | Item bought. | e.g. Handbag |
| `purchase_amount_usd` | double | Purchase amount in USD. | e.g. 4619.0 |
| `date_purchase` | timestamp[us] | Purchase date. | e.g. 2023-02-05 00:00:00 |
| `review_rating` | double | Reviewer's star rating. | e.g. 2.0 |
| `payment_method` | large_string | Payment method used. | e.g. Credit Card |

### `tiki_catalog_clean.parquet`  —  Tiki.vn fashion catalog (VND) - the target platform.

*41,576 rows · 18 columns*

| Column | Type | Meaning | Values / example |
|---|---|---|---|
| `id` | int64 |  | e.g. 179731375 |
| `name` | large_string |  | e.g. Balo nữ da dầy thời trang unisex màu sắc tươi sáng TA63 |
| `description` | large_string | Product/description text. | e.g.   Balo nữ da dầy thời trang unisex màu sắc tươi sáng TA63   … |
| `original_price` | int64 | List/original price (before discount). | e.g. 14250 |
| `price` | int64 | Selling price. | e.g. 14250 |
| `fulfillment_type` | large_string | Fulfilment method. | e.g. dropship |
| `brand` | large_string | Brand name. | e.g. OEM |
| `review_count` | int64 | Number of reviews. | e.g. 0 |
| `rating_average` | double | Average star rating. | e.g. 0.0 |
| `favourite_count` | int64 | Times favourited. | values: `0` |
| `pay_later` | bool |  | values: `False`, `True` |
| `current_seller` | large_string | Seller name. | e.g. Thiên Ân Balo |
| `number_of_images` | int64 |  | e.g. 10 |
| `vnd_cashback` | int64 |  | e.g. 0 |
| `has_video` | bool |  | values: `False`, `True` |
| `category` | large_string | Product category. | e.g. Balo nữ |
| `quantity_sold` | int64 | Units sold. | e.g. 0 |
| `discount_pct` | double | Discount percent off the original price. | e.g. 0.0 |

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

