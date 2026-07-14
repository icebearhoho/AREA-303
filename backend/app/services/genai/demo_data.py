"""Pre-generated fixtures for the GenAI services.

Used in two places:

1. :class:`InMemoryRetriever` — the catalog rows serve as the RAG
   knowledge base in demo mode.
2. Canned outputs for the 4 fullstack endpoints (#03, #09, #11, #17).
   The frontend reads the same shape; when DEMO_MODE is on, the backend
   never calls an LLM.
"""

from __future__ import annotations

# --------------------------------------------------------------------- #
# Catalog — used by RAG
# --------------------------------------------------------------------- #

DEMO_CATALOG: list[dict] = [
    {
        "id": "P001",
        "title": "Áo khoác denim unisex form rộng",
        "text": (
            "Denim 12oz wash nhẹ, form rộng unisex, 2 túi ngực + 2 túi hông. "
            "Phù hợp đi học, đi chơi. Free ship đơn từ 250k."
        ),
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 489_000},
    },
    {
        "id": "P002",
        "title": "Serum Vitamin C 15% NUDESTIX",
        "text": (
            "Serum C ổn định, sáng da, giảm thâm sau 4 tuần. Dùng buổi sáng, "
            "kết hợp kem chống nắng."
        ),
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 720_000},
    },
    {
        "id": "P003",
        "title": "Túi tote canvas in họa tiết",
        "text": (
            "Tote canvas dày 12oz, in lụa 2 mặt, đường chỉ gấp đôi. Chứa laptop 14 inch."
        ),
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 159_000},
    },
    {
        "id": "P004",
        "title": "Son tint lì Bourjois Velvet 21",
        "text": (
            "Tint lì lâu trôi 8h, finish velvet không khô môi. Tông 21 — đỏ gạch."
        ),
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 295_000},
    },
    {
        "id": "P005",
        "title": "Quần ống rộng lưng cao linen",
        "text": "Linen pha, lưng cao che bụng, ống rộng xếp ly. Size S–XL.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 369_000},
    },
    {
        "id": "P006",
        "title": "Mặt nạ ngủ Laneige Water Sleeping Mask",
        "text": "Mặt nạ ngủ cấp ẩm 8h, dùng sau serum. Phù hợp da khô, da hỗn hợp.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 650_000},
    },
    {
        "id": "P007",
        "title": "Đồng hồ Casio MTP-V002 minimal",
        "text": "Mặt tròn 38mm, dây thép không gỉ, chống nước 30m. Bảo hành 1 năm.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 489_000},
    },
    {
        "id": "P008",
        "title": "Áo thun oversize cotton 220gsm",
        "text": "Cotton 220gsm dày dặn, form oversize, in lụa không bong. 5 màu.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 189_000},
    },
]


# --------------------------------------------------------------------- #
# Canned outputs per feature — used when demo_mode=true and the LLM
# cannot be reached.  The shape MUST match the typed endpoint schema.
# --------------------------------------------------------------------- #


SHOPPER_DEMO_REPLY = (
    "Dựa trên câu hỏi của bạn, mình gợi ý 4 sản phẩm phù hợp từ catalog "
    "Shopee · Tiki · TikTok Shop:\n\n"
    "1. Áo khoác denim unisex — Local Brand X (Shopee, 4.6★)\n"
    "2. Serum Vitamin C 15% — NUDESTIX (Tiki, 4.4★)\n"
    "3. Túi tote canvas — OEM (TikTok Shop, 4.7★)\n"
    "4. Son tint Bourjois Velvet 21 — Bourjois (Shopee, 4.5★)\n\n"
    "Bạn muốn mình đi sâu hơn vào tiêu chí nào (giá, brand, rating)?"
)

SHOPPER_DEMO_PRODUCT_IDS = ["P001", "P002", "P003", "P004"]


CONTENT_DEMO_VARIANTS: list[dict] = [
    {
        "platform": "Shopee",
        "title": "Áo khoác denim unisex — form rộng, wash nhẹ, mặc 4 mùa",
        "body": (
            "Denim 12oz wash nhẹ — không bai, không xù. Form rộng unisex, 2 size S–XL. "
            "Bỏ túi ngực + túi hông đủ laptop 14\". Free ship đơn từ 250k."
        ),
        "predicted_ctr": 0.082,
        "rationale": "Hero keywords: 'denim unisex', 'form rộng', '4 mùa'. Mention Free ship — tăng 18% CTR.",
    },
    {
        "platform": "Tiki",
        "title": "Áo khoác denim form rộng unisex | Local Brand X | Chính hãng",
        "body": (
            "Sản phẩm chính hãng Local Brand X. Chất liệu denim 12oz wash nhẹ, đường may gấp đôi. "
            "Đổi trả 7 ngày nếu lỗi. TikiNOW giao 2h tại TP.HCM & Hà Nội."
        ),
        "predicted_ctr": 0.071,
        "rationale": "Đề cao 'Chính hãng' + 'TikiNOW' — phù hợp khách Tiki tìm đảm bảo giao nhanh.",
    },
    {
        "platform": "TikTok Shop",
        "title": "DENIM JACKET siêu xinh — đi học đi chơi đều ổn 🥹",
        "body": (
            "Best seller tuần qua! Wash nhẹ mặc siêu mềm, form rộng giấu bụng. "
            "Đủ size S–XL. Comment 'DENIM' để nhận voucher 30k."
        ),
        "predicted_ctr": 0.118,
        "rationale": "Hook ngắn + emoji + comment-to-claim — pattern TikTok Shop thường thắng trên impulse.",
    },
]


RECSYS_TRADITIONAL: list[dict] = [
    {
        "product_id": "P001",
        "name": "Áo khoác denim unisex form rộng",
        "brand": "Local Brand X",
        "category": "Thời trang",
        "platform": "Shopee",
        "price_vnd": 489_000,
        "rating": 4.6,
        "reviews": 1284,
        "similarity": 0.92,
        "reason": "Collaborative filtering: người dùng tương tự (cosine 0.83) cũng đã mua.",
    },
    {
        "product_id": "P002",
        "name": "Serum Vitamin C 15% NUDESTIX",
        "brand": "NUDESTIX",
        "category": "Mỹ phẩm",
        "platform": "Tiki",
        "price_vnd": 720_000,
        "rating": 4.4,
        "reviews": 892,
        "similarity": 0.88,
        "reason": "CF: cụm user 'beauty enthusiast' (k=4) co-purchase với item này.",
    },
    {
        "product_id": "P003",
        "name": "Túi tote canvas in họa tiết",
        "brand": "OEM",
        "category": "Phụ kiện",
        "platform": "TikTok Shop",
        "price_vnd": 159_000,
        "rating": 4.7,
        "reviews": 3201,
        "similarity": 0.81,
        "reason": "Item-item cosine 0.79 với 'Túi tote vải bố' bạn vừa xem.",
    },
    {
        "product_id": "P004",
        "name": "Son tint lì Bourjois Velvet 21",
        "brand": "Bourjois",
        "category": "Mỹ phẩm",
        "platform": "Shopee",
        "price_vnd": 295_000,
        "rating": 4.5,
        "reviews": 612,
        "similarity": 0.76,
        "reason": "Cụm user 'lipstick lover' co-purchase rate 14%.",
    },
]


RECSYS_AI: list[dict] = [
    {
        "product_id": "P002",
        "name": "Serum Vitamin C 15% NUDESTIX",
        "brand": "NUDESTIX",
        "category": "Mỹ phẩm",
        "platform": "Tiki",
        "price_vnd": 720_000,
        "rating": 4.4,
        "reviews": 892,
        "similarity": 0.88,
        "reason": "Bạn vừa mua serum BHA — C-vit là bước tiếp theo được chuyên gia khuyên.",
    },
    {
        "product_id": "P006",
        "name": "Mặt nạ ngủ Laneige Water Sleeping Mask",
        "brand": "Laneige",
        "category": "Mỹ phẩm",
        "platform": "Shopee",
        "price_vnd": 650_000,
        "rating": 4.8,
        "reviews": 2410,
        "similarity": 0.69,
        "reason": "Da bạn da khô (signal từ quiz), Laneige mask lock ẩm 8h qua đêm.",
    },
    {
        "product_id": "P004",
        "name": "Son tint lì Bourjois Velvet 21",
        "brand": "Bourjois",
        "category": "Mỹ phẩm",
        "platform": "Shopee",
        "price_vnd": 295_000,
        "rating": 4.5,
        "reviews": 612,
        "similarity": 0.76,
        "reason": "Son tint lì — match với 3 review gần đây của bạn đều khen 'lâu trôi, không khô'.",
    },
    {
        "product_id": "P003",
        "name": "Túi tote canvas in họa tiết",
        "brand": "OEM",
        "category": "Phụ kiện",
        "platform": "TikTok Shop",
        "price_vnd": 159_000,
        "rating": 4.7,
        "reviews": 3201,
        "similarity": 0.81,
        "reason": "Tote canvas phù hợp với style bạn lướt (canvas + earth-tone) trong 14 ngày qua.",
    },
]


SELLER_AUDIT: list[dict] = [
    {"id": "listing",   "label": "Listing Quality", "score": 72,
     "tip": "Mô tả ngắn, nên bổ sung 2-3 bullet về chất liệu + cách dùng."},
    {"id": "pricing",   "label": "Pricing",         "score": 64,
     "tip": "Đang cao hơn median category 8% — thử giảm 5-7% trong 7 ngày."},
    {"id": "visuals",   "label": "Visuals",         "score": 58,
     "tip": "Ảnh chính thiếu sáng, hero subject chỉ chiếm 32% frame."},
    {"id": "reviews",   "label": "Reviews",         "score": 81,
     "tip": "Reply rate 92%, nhưng phản hồi negative chậm (>24h)."},
    {"id": "inventory", "label": "Inventory",       "score": 47,
     "tip": "SKU top bán stockout 3 lần trong 30 ngày — set reorder buffer."},
]


SELLER_ROADMAP: list[dict] = [
    {
        "week": 1,
        "title": "Fix nền tảng",
        "bullets": [
            "Reorder buffer cho 5 SKU top",
            "Reply 100% review negative trong 12h",
            "Đẩy 2 ảnh mới cho listing đèn sales",
        ],
    },
    {
        "week": 2,
        "title": "Tối ưu listing",
        "bullets": [
            "Rewrite mô tả cho 10 listing theo AI gợi ý",
            "A/B test 3 hero images",
            "Bổ sung 5 video 15s cho top SKUs",
        ],
    },
    {
        "week": 3,
        "title": "Pricing & promotion",
        "bullets": [
            "Điều chỉnh giá về median ± 5%",
            "Chạy voucher 10% trong 48h cho segment Loyalty",
            "Combo 3 sản phẩm bán chạy",
        ],
    },
    {
        "week": 4,
        "title": "Scale & retention",
        "bullets": [
            "Ra mắt 2 SKU mới theo trend Q3",
            "Email win-back cho segment At Risk",
            "Review & lặp lại vòng audit",
        ],
    },
]