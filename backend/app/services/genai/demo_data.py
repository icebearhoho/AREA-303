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
# Image URL helper — returns Unsplash URL for a product
# Using specific photo IDs from Unsplash for accurate product images
# --------------------------------------------------------------------- #

# Unsplash photo IDs for accurate product images
_UNSPLASH_IMAGES = {
    # Thời trang - Áo
    "polo": "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&q=80",
    "dress_shirt": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop&q=80",
    "tshirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&q=80",
    "hoodie": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&q=80",
    "bomber_jacket": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=400&fit=crop&q=80",
    "denim_jacket": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400&h=400&fit=crop&q=80",
    "knitwear": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=400&fit=crop&q=80",
    "winter_coat": "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400&h=400&fit=crop&q=80",
    "blazer": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&q=80",
    "crop_top": "https://images.unsplash.com/photo-1485968579580-b6d095142e6e?w=400&h=400&fit=crop&q=80",
    
    # Thời trang - Quần
    "jogger": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop&q=80",
    "shorts": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop&q=80",
    "jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop&q=80",
    "leggings": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400&h=400&fit=crop&q=80",
    
    # Thời trang - Váy/Đầm
    "skirt": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&h=400&fit=crop&q=80",
    "dress": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop&q=80",
    
    # Thời trang - Giày
    "sneakers": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&q=80",
    "boots": "https://images.unsplash.com/photo-1542840410-8e73aa1f5d9c?w=400&h=400&fit=crop&q=80",
    "sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400&h=400&fit=crop&q=80",
    "oxford_shoes": "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=400&h=400&fit=crop&q=80",
    
    # Mỹ phẩm - Son
    "lipstick": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop&q=80",
    
    # Mỹ phẩm - Serum/Kem
    "serum": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=400&fit=crop&q=80",
    "moisturizer": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop&q=80",
    "sunscreen": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&q=80",
    "foundation": "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400&h=400&fit=crop&q=80",
    "toner": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&h=400&fit=crop&q=80",
    
    # Mỹ phẩm - Makeup
    "eyeshadow": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop&q=80",
    "mascara": "https://images.unsplash.com/photo-1631214540553-ff044a3ff1d4?w=400&h=400&fit=crop&q=80",
    "blush": "https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=400&h=400&fit=crop&q=80",
    "perfume": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop&q=80",
    "face_mask": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&h=400&fit=crop&q=80",
    "face_wash": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&q=80",
    
    # Phụ kiện - Túi
    "handbag": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=400&fit=crop&q=80",
    "tote_bag": "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400&h=400&fit=crop&q=80",
    "crossbody_bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop&q=80",
    "backpack": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&q=80",
    "wallet": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop&q=80",
    "clutch_bag": "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d?w=400&h=400&fit=crop&q=80",
    
    # Phụ kiện - Kính/Mũ
    "sunglasses": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop&q=80",
    "cap": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&q=80",
    
    # Phụ kiện - Đồng hồ/Trang sức
    "watch": "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop&q=80",
    "necklace": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop&q=80",
    "bracelet": "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop&q=80",
    "earrings": "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&h=400&fit=crop&q=80",
    "scarf": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400&h=400&fit=crop&q=80",
    "belt": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&q=80",
    
    # Khác
    "pajamas": "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=400&h=400&fit=crop&q=80",
    "default": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop&q=80",
}


def get_product_image_url(title: str) -> str:
    """Return a consistent image URL based on product title keywords."""
    t = title.lower()
    
    # Thời trang - Áo
    if any(k in t for k in ['áo polo', 'polo']):
        return _UNSPLASH_IMAGES["polo"]
    if any(k in t for k in ['áo sơ mi', 'sơ mi', 'oxford']):
        return _UNSPLASH_IMAGES["dress_shirt"]
    if any(k in t for k in ['áo phông', 'áo thun', 'tshirt', 't-shirt', 'áo thun oversize']):
        return _UNSPLASH_IMAGES["tshirt"]
    if any(k in t for k in ['áo hoodie', 'hoodie']):
        return _UNSPLASH_IMAGES["hoodie"]
    if any(k in t for k in ['áo khoác bomber', 'bomber']):
        return _UNSPLASH_IMAGES["bomber_jacket"]
    if any(k in t for k in ['áo khoác denim', 'áo khoác', 'denim']):
        return _UNSPLASH_IMAGES["denim_jacket"]
    if any(k in t for k in ['áo len', 'len cổ lọ', 'cardigan', 'áo cổ lọ']):
        return _UNSPLASH_IMAGES["knitwear"]
    if any(k in t for k in ['áo dạ', 'áo phao', 'áo lông', 'down jacket', 'áo gió']):
        return _UNSPLASH_IMAGES["winter_coat"]
    if any(k in t for k in ['áo croptop', 'croptop', 'crop top']):
        return _UNSPLASH_IMAGES["crop_top"]
    if any(k in t for k in ['áo nịt', 'corset']):
        return _UNSPLASH_IMAGES["crop_top"]
    if any(k in t for k in ['áo vest', 'blazer', 'vest']):
        return _UNSPLASH_IMAGES["blazer"]
    if any(k in t for k in ['áo hai dây', 'bra top', 'bra', 'áo yếm']):
        return _UNSPLASH_IMAGES["crop_top"]
    
    # Thời trang - Quần
    if any(k in t for k in ['quần jogger', 'jogger']):
        return _UNSPLASH_IMAGES["jogger"]
    if any(k in t for k in ['quần short', 'short']):
        return _UNSPLASH_IMAGES["shorts"]
    if any(k in t for k in ['quần baggy', 'baggy']):
        return _UNSPLASH_IMAGES["jogger"]
    if any(k in t for k in ['quần jeans', 'jeans', 'quần jean']):
        return _UNSPLASH_IMAGES["jeans"]
    if any(k in t for k in ['quần bó', 'quần thể thao', 'legging', 'sport', 'quần ống rộng', 'ống rộng']):
        return _UNSPLASH_IMAGES["leggings"]
    if any(k in t for k in ['quần yếm', 'yếm']):
        return _UNSPLASH_IMAGES["jeans"]
    if any(k in t for k in ['quần culottes', 'culottes', 'quần ống suông']):
        return _UNSPLASH_IMAGES["leggings"]
    if any(k in t for k in ['quần cargo']):
        return _UNSPLASH_IMAGES["jogger"]
    
    # Thời trang - Váy/Đầm
    if any(k in t for k in ['váy chữ a', 'váy a', 'váy maxi', 'váy tennis', 'váy', 'váy đầm']):
        return _UNSPLASH_IMAGES["skirt"]
    if any(k in t for k in ['đầm', 'đầm midi', 'đầm maxi', 'dress']):
        return _UNSPLASH_IMAGES["dress"]
    if any(k in t for k in ['váy tennis', 'tennis skirt']):
        return _UNSPLASH_IMAGES["skirt"]
    
    # Thời trang - Giày
    if any(k in t for k in ['giày oxford', 'oxford']):
        return _UNSPLASH_IMAGES["oxford_shoes"]
    if any(k in t for k in ['boots', 'boot', 'bootcut']):
        return _UNSPLASH_IMAGES["boots"]
    if any(k in t for k in ['dép sandal', 'sandal', 'dép', 'dép xuồng']):
        return _UNSPLASH_IMAGES["sandals"]
    if any(k in t for k in ['giày thể thao', 'giày chạy', 'sneaker', 'giày sneaker', 'giày']):
        return _UNSPLASH_IMAGES["sneakers"]
    
    # Thời trang - Khác
    if any(k in t for k in ['pajamas', 'bộ pajamas', 'đồ ngủ', 'đồ ngủ nữ']):
        return _UNSPLASH_IMAGES["pajamas"]
    if any(k in t for k in ['jumpsuit']):
        return _UNSPLASH_IMAGES["dress"]
    
    # Mỹ phẩm - Son
    if any(k in t for k in ['son dưỡng', 'son kem', 'son', 'lipstick', 'lip glow', 'tint', 'son tint']):
        return _UNSPLASH_IMAGES["lipstick"]
    
    # Mỹ phẩm - Kem
    if any(k in t for k in ['kem nền', 'foundation', 'cushion']):
        return _UNSPLASH_IMAGES["foundation"]
    if any(k in t for k in ['kem dưỡng', 'moisturizer', 'kem body', 'kem ẩm']):
        return _UNSPLASH_IMAGES["moisturizer"]
    if any(k in t for k in ['kem chống nắng', 'sunscreen', 'chống nắng']):
        return _UNSPLASH_IMAGES["sunscreen"]
    if any(k in t for k in ['kem mắt', 'eye cream', 'kem trị mụn']):
        return _UNSPLASH_IMAGES["serum"]
    if any(k in t for k in ['kem trị']):
        return _UNSPLASH_IMAGES["serum"]
    
    # Mỹ phẩm - Serum/Active
    if any(k in t for k in ['serum', 'essence', 'vitamin c', 'bha', 'aha', 'tinh chất']):
        return _UNSPLASH_IMAGES["serum"]
    
    # Mỹ phẩm - Cleansing
    if any(k in t for k in ['sữa rửa mặt', 'face wash', 'nước tẩy trang', 'rửa mặt']):
        return _UNSPLASH_IMAGES["face_wash"]
    if any(k in t for k in ['toner', 'nước hoa hồng']):
        return _UNSPLASH_IMAGES["toner"]
    if any(k in t for k in ['sữa tắm', 'body wash', 'tắm']):
        return _UNSPLASH_IMAGES["face_wash"]
    
    # Mỹ phẩm - Makeup
    if any(k in t for k in ['phấn mắt', 'eyeshadow', 'palette']):
        return _UNSPLASH_IMAGES["eyeshadow"]
    if any(k in t for k in ['mascara']):
        return _UNSPLASH_IMAGES["mascara"]
    if any(k in t for k in ['eyeliner', 'kẻ mắt']):
        return _UNSPLASH_IMAGES["mascara"]
    if any(k in t for k in ['phấn má', 'blush', 'má hồng']):
        return _UNSPLASH_IMAGES["blush"]
    if any(k in t for k in ['highlighter']):
        return _UNSPLASH_IMAGES["blush"]
    if any(k in t for k in ['phấn nén', 'powder', 'phấn']):
        return _UNSPLASH_IMAGES["foundation"]
    
    # Mỹ phẩm - Fragrance
    if any(k in t for k in ['nước hoa', 'perfume', 'xịt thơm']):
        return _UNSPLASH_IMAGES["perfume"]
    
    # Mỹ phẩm - Hair
    if any(k in t for k in ['dầu gội', 'shampoo', 'dầu xả', 'conditioner', 'gội đầu']):
        return _UNSPLASH_IMAGES["face_wash"]
    if any(k in t for k in ['mặt nạ', 'face mask', 'mask', 'mặt nạ ngủ']):
        return _UNSPLASH_IMAGES["face_mask"]
    if any(k in t for k in ['xịt khoáng', 'face mist', 'xịt thơm']):
        return _UNSPLASH_IMAGES["toner"]
    
    # Phụ kiện - Túi
    if any(k in t for k in ['túi clutch', 'clutch']):
        return _UNSPLASH_IMAGES["clutch_bag"]
    if any(k in t for k in ['túi đeo chéo', 'túi chéo', 'crossbody', 'đeo chéo']):
        return _UNSPLASH_IMAGES["crossbody_bag"]
    if any(k in t for k in ['túi xách', 'túi làm việc', 'túi đeo vai']):
        return _UNSPLASH_IMAGES["handbag"]
    if any(k in t for k in ['túi tote', 'tote', 'túi trống']):
        return _UNSPLASH_IMAGES["tote_bag"]
    if any(k in t for k in ['túi belt', 'belt bag', 'fanny pack']):
        return _UNSPLASH_IMAGES["crossbody_bag"]
    if any(k in t for k in ['ví đựng điện thoại', 'ví phone', 'ví điện thoại']):
        return _UNSPLASH_IMAGES["wallet"]
    if any(k in t for k in ['ví', 'wallet', 'ví nam', 'ví nữ']):
        return _UNSPLASH_IMAGES["wallet"]
    if any(k in t for k in ['balo', 'ba lô', 'backpack']):
        return _UNSPLASH_IMAGES["backpack"]
    
    # Phụ kiện - Mũ/Kính
    if any(k in t for k in ['mũ lưỡi trai', 'snapback', 'mũ snapback', 'nón lưỡi trai', 'nón']):
        return _UNSPLASH_IMAGES["cap"]
    if any(k in t for k in ['kính râm', 'sunglasses', 'kính', 'mắt kính', 'gọng kính']):
        return _UNSPLASH_IMAGES["sunglasses"]
    
    # Phụ kiện - Trang sức
    if any(k in t for k in ['dây chuyền', 'necklace', 'chain']):
        return _UNSPLASH_IMAGES["necklace"]
    if any(k in t for k in ['vòng tay', 'bracelet', 'lắc tay']):
        return _UNSPLASH_IMAGES["bracelet"]
    if any(k in t for k in ['bông tai', ' earrings', 'hoa tai', 'khuyên tai']):
        return _UNSPLASH_IMAGES["earrings"]
    if any(k in t for k in ['bộ trang sức', 'trang sức']):
        return _UNSPLASH_IMAGES["necklace"]
    
    # Phụ kiện - Thắt lưng/Găng
    if any(k in t for k in ['thắt lưng', 'belt', 'dây nịt']):
        return _UNSPLASH_IMAGES["belt"]
    if any(k in t for k in ['găng tay', 'gloves']):
        return _UNSPLASH_IMAGES["scarf"]
    
    # Phụ kiện - Khăn
    if any(k in t for k in ['khăn choàng', 'scarf', 'khăn', 'khăn quàng']):
        return _UNSPLASH_IMAGES["scarf"]
    
    # Phụ kiện - Đồng hồ
    if any(k in t for k in ['đồng hồ', 'watch', 'đồng hồ nam', 'đồng hồ nữ']):
        return _UNSPLASH_IMAGES["watch"]
    if any(k in t for k in ['dây đồng hồ', 'dây apple watch', 'dây đeo']):
        return _UNSPLASH_IMAGES["watch"]
    
    # Phụ kiện - Hair accessories
    if any(k in t for k in ['nơ tóc', 'hair bow', 'hair ribbon']):
        return _UNSPLASH_IMAGES["earrings"]
    if any(k in t for k in ['kẹp tóc', 'hair clip', 'hair claw']):
        return _UNSPLASH_IMAGES["earrings"]
    if any(k in t for k in ['dây buộc tóc', 'hair tie']):
        return _UNSPLASH_IMAGES["bracelet"]
    if any(k in t for k in ['móc khóa']):
        return _UNSPLASH_IMAGES["bracelet"]
    if any(k in t for k in ['gương makeup', 'gương']):
        return _UNSPLASH_IMAGES["handbag"]
    
    # Default fallback
    return _UNSPLASH_IMAGES["default"]


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
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 489_000, "image_url": ""},
    },
    {
        "id": "P002",
        "title": "Serum Vitamin C 15% NUDESTIX",
        "text": (
            "Serum C ổn định, sáng da, giảm thâm sau 4 tuần. Dùng buổi sáng, "
            "kết hợp kem chống nắng."
        ),
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 720_000, "image_url": ""},
    },
    {
        "id": "P003",
        "title": "Túi tote canvas in họa tiết",
        "text": (
            "Tote canvas dày 12oz, in lụa 2 mặt, đường chỉ gấp đôi. Chứa laptop 14 inch."
        ),
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 159_000, "image_url": ""},
    },
    {
        "id": "P004",
        "title": "Son tint lì Bourjois Velvet 21",
        "text": (
            "Tint lì lâu trôi 8h, finish velvet không khô môi. Tông 21 — đỏ gạch."
        ),
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 295_000, "image_url": ""},
    },
    {
        "id": "P005",
        "title": "Quần ống rộng lưng cao linen",
        "text": "Linen pha, lưng cao che bụng, ống rộng xếp ly. Size S–XL.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 369_000, "image_url": ""},
    },
    {
        "id": "P006",
        "title": "Mặt nạ ngủ Laneige Water Sleeping Mask",
        "text": "Mặt nạ ngủ cấp ẩm 8h, dùng sau serum. Phù hợp da khô, da hỗn hợp.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 650_000, "image_url": ""},
    },
    {
        "id": "P007",
        "title": "Đồng hồ Casio MTP-V002 minimal",
        "text": "Mặt tròn 38mm, dây thép không gỉ, chống nước 30m. Bảo hành 1 năm.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 489_000, "image_url": ""},
    },
    {
        "id": "P008",
        "title": "Áo thun oversize cotton 220gsm",
        "text": "Cotton 220gsm dày dặn, form oversize, in lụa không bong. 5 màu.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 189_000, "image_url": ""},
    },
    # --- more cosmetics / skincare ---
    {
        "id": "P009",
        "title": "Sữa rửa mặt CeraVe cho da dầu mụn",
        "text": "Sữa rửa mặt tạo bọt, kiểm soát dầu, chứa ceramide + niacinamide. Da dầu, da mụn.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 285_000, "image_url": ""},
    },
    {
        "id": "P010",
        "title": "Kem chống nắng Anessa SPF50+ PA++++",
        "text": "Chống nắng kiềm dầu, không bết, phù hợp da dầu mụn. Dùng bước cuối buổi sáng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 520_000, "image_url": ""},
    },
    {
        "id": "P011",
        "title": "Toner BHA Paula's Choice 2%",
        "text": "BHA 2% giảm mụn ẩn, thông thoáng lỗ chân lông. Da dầu, da mụn nhẹ.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 610_000, "image_url": ""},
    },
    {
        "id": "P012",
        "title": "Kem dưỡng ẩm gel không dầu Neutrogena",
        "text": "Gel dưỡng ẩm oil-free cấp nước, không gây bít tắc. Hợp da dầu mụn.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 240_000, "image_url": ""},
    },
    {
        "id": "P013",
        "title": "Cushion trang điểm kiềm dầu 3CE",
        "text": "Cushion finish lì, kiềm dầu 8h, SPF35. Tông tự nhiên cho da dầu.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 430_000, "image_url": ""},
    },
    # --- more fashion / accessories ---
    {
        "id": "P014",
        "title": "Váy đầm midi cổ vuông tay bồng",
        "text": "Đầm midi cổ vuông, tay bồng, vải tuyết mưa. Đi tiệc, đi làm. Size S–L.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 359_000, "image_url": ""},
    },
    {
        "id": "P015",
        "title": "Giày sneaker trắng đế cao 4cm",
        "text": "Sneaker da PU trắng, đế cao 4cm tôn dáng, lót êm. Size 35–43.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 429_000, "image_url": ""},
    },
    {
        "id": "P016",
        "title": "Quần jean nữ ống suông lưng cao",
        "text": "Jean cotton co giãn nhẹ, ống suông, lưng cao. Xanh wash cổ điển.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 329_000, "image_url": ""},
    },
    {
        "id": "P017",
        "title": "Kính mát nữ gọng vuông trendy",
        "text": "Gọng acetate vuông, tròng chống UV400. Nhiều màu, kèm hộp + khăn.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 149_000, "image_url": ""},
    },
    {
        "id": "P018",
        "title": "Balo laptop chống nước 15.6 inch",
        "text": "Balo chống nước, ngăn laptop 15.6 inch có đệm, cổng sạc USB. Đi học/đi làm.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 259_000, "brand": "OEM", "image_url": ""},
    },
    # ========== THEM SAN PHAM MOI ==========
    # --- Thoi trang: 30 san pham ---
    {
        "id": "P019",
        "title": "Áo polo pique cotton nam form slim",
        "text": "Polo pique cotton 100%, form slim vừa vặn, màu trơn 8 tùy chọn. Thấm hút mồ hôi tốt.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 299_000, "brand": "Local Brand", "image_url": ""},
    },
    {
        "id": "P020",
        "title": "Quần jogger nam co giãn 4 chiều",
        "text": "Jogger vải co giãn 4 chiều, cạp chun có dây rút. Phong cách streetwear, đi chơi hoặc gym.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 349_000, "brand": "Sporty", "image_url": ""},
    },
    {
        "id": "P021",
        "title": "Áo sơ mi lụa nữ cổ V dáng suông",
        "text": "Sơ mi lụa mịn, cổ V nhẹ, dáng suông thoáng mát. Màu pastel thanh lịch. Đi làm hoặc đi chơi.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 389_000, "brand": "Elegance", "image_url": ""},
    },
    {
        "id": "P022",
        "title": "Set bộ thể thao nữ crop top + quần bó",
        "text": "Set crop top + quần bó, vải thun lạnh co giãn, màu đen/xanh/nude. Phù hợp yoga, gym, chạy bộ.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 259_000, "brand": "FitStyle", "image_url": ""},
    },
    {
        "id": "P023",
        "title": "Áo khoác bomber nhung tăm unisex",
        "text": "Bomber nhung tăm phong cách Hàn Quốc, cổ đứng, bo gấu + bo tay. Unisex, size M–2XL.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 549_000, "brand": "KStyle", "image_url": ""},
    },
    {
        "id": "P024",
        "title": "Váy chữ A maxi phối ren",
        "text": "Váy chữ A maxi dài qua gối, phối viền ren mềm mại. Màu trắng, be, đen. Đi dạo phố, cà phê.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 329_000, "brand": "Femme", "image_url": ""},
    },
    {
        "id": "P025",
        "title": "Giày boots da nam gót vuông 5cm",
        "text": "Boots da PU cao cổ, gót vuông 5cm đứng vững. Đen/nâu. Đi làm, đi chơi đều phù hợp.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 589_000, "brand": "Masculine", "image_url": ""},
    },
    {
        "id": "P026",
        "title": "Áo hoodie nỉ bông form rộng",
        "text": "Hoodie nỉ bông cotton 80%, form rộng oversize, có túi kangaroo. Có mũ trùm đầu. Unisex.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 399_000, "brand": "Comfy", "image_url": ""},
    },
    {
        "id": "P027",
        "title": "Quần short nam cargo 5 túi",
        "text": "Short cargo ống rộng, 5 túi thực dụng, vải katé thoáng mát. Đi phố, dã ngoại.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 279_000, "brand": "Urban", "image_url": ""},
    },
    {
        "id": "P028",
        "title": "Đầm suông cổ tròn tay phồng",
        "text": "Đầm suông cổ tròn, tay phồng nhẹ, dáng dài qua gối. Vải voan nhẹ nhàng. 5 màu.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 429_000, "brand": "Ladies", "image_url": ""},
    },
    {
        "id": "P029",
        "title": "Áo hai dây bra top nữ ren",
        "text": "Bra top ren mỏng nhẹ, đệm lót vừa phải, dây đeo điều chỉnh được. Mặc trong hoặc ra ngoài.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 149_000, "brand": "Delicate", "image_url": ""},
    },
    {
        "id": "P030",
        "title": "Dép sandal nữ đế b平台的 3cm",
        "text": "Sandal đế b平台的 3cm, quai ngang da PU, lót đệm mềm. Phong cách tối giản Nhật Bản.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 219_000, "brand": "Minimal", "image_url": ""},
    },
    {
        "id": "P031",
        "title": "Áo len nữ cổ lọ dệt kim",
        "text": "Áo len cổ lọ dệt kim mịn, vải len pha mềm mại, không cào da. Màu be, xám, trắng sữa.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 459_000, "brand": "WarmKnit", "image_url": ""},
    },
    {
        "id": "P032",
        "title": "Quần yếm jeans nữ lưng cao",
        "text": "Yếm jeans lưng cao, dây đeo có khóa, ống baggy thoải mái. Phối áo phông hoặc sơ mi đều đẹp.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 389_000, "brand": "Vintage", "image_url": ""},
    },
    {
        "id": "P033",
        "title": "Áo vest nữ blazer phong cách Hàn",
        "text": "Blazer vest nữ phong cách Hàn Quốc, form vừa, vải nỉ nhẹ. Đi làm, đi phỏng vấn.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 499_000, "brand": "KOffice", "image_url": ""},
    },
    {
        "id": "P034",
        "title": "Giày Oxford nam da bóng",
        "text": "Oxford da bóng classic, đế gỗ, dây buộc thanh lịch. Phong cách công sở, dự tiệc.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 699_000, "brand": "Classic", "image_url": ""},
    },
    {
        "id": "P035",
        "title": "Áo phao nữ dáng dài phong cách Hàn",
        "text": "Áo phao dáng dài qua gối, lông vũ 80%, chống lạnh -10 độ. Phong cách Hàn Quốc.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 899_000, "brand": "KWinter", "image_url": ""},
    },
    {
        "id": "P036",
        "title": "Quần culottes lụa nữ ống rộng",
        "text": "Culottes lụa ống rộng lưng thun, dài qua gối. Mát mẻ, phong cách thanh lịch. Đi làm hoặc dạo phố.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 349_000, "brand": "SilkFlow", "image_url": ""},
    },
    {
        "id": "P037",
        "title": "Đầm bodycon cổ tim ghim ngực",
        "text": "Đầm bodycon cổ tim, ghim ngực ren, dáng ôm sát. Màu đen, đỏ, xanh navy. Đi tiệc, đi bar.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 389_000, "brand": "Glam", "image_url": ""},
    },
    {
        "id": "P038",
        "title": "Bộ pajamas nỉ nhung nữ",
        "text": "Bộ pajamas nỉ nhung mềm mại, áo cổ tròn + quần dáng rộng. Màu hồng, xanh mint, xám. Mặc nhà siêu thoải mái.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 299_000, "brand": "CozyHome", "image_url": ""},
    },
    {
        "id": "P039",
        "title": "Áo croptop body nữ tay ngắn",
        "text": "Croptop body ôm vừa, tay ngắn, cổ tròn. Phối quần high waisted cực đẹp. Nhiều màu.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 159_000, "brand": "Y2K", "image_url": ""},
    },
    {
        "id": "P040",
        "title": "Áo cardigan nữ len đan mỏng",
        "text": "Cardigan len đan dệt kim mỏng, cổ V, dáng thướt tha. Mùa thu đông, phối đồ tối giản.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 429_000, "brand": "Knitwear", "image_url": ""},
    },
    {
        "id": "P041",
        "title": "Quần thể thao nam chạy bộ ưa thích",
        "text": "Quần thể thao chạy bộ ống suông, vải thun lạnh thoáng khí, có túi zip. Chạy bộ, gym.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 329_000, "brand": "RunPro", "image_url": ""},
    },
    {
        "id": "P042",
        "title": "Đầm xòe bồng bềnh dạ tiệc",
        "text": "Đầm xòe dạ tiệc, chất dạ mềm, phồng nhẹ, ngắn trên gối. Màu đỏ, đen, vàng gold. Tiệc cưới.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 659_000, "brand": "Elegant", "image_url": ""},
    },
    {
        "id": "P043",
        "title": "Áo sơ mi nam oxford cotton cổ đức",
        "text": "Sơ mi oxford cotton 100%, cổ đức lịch lãm, dáng slim vừa. Đi làm, công sở.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 349_000, "brand": "OfficeMan", "image_url": ""},
    },
    {
        "id": "P044",
        "title": "Váy tennis nữ skirt plisode",
        "text": "Váy tennis skirt plisode ngắn, có quần short bên trong. Vải thể thao co giãn, màu tươi sáng.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 229_000, "brand": "SportyGirl", "image_url": ""},
    },
    {
        "id": "P045",
        "title": "Áo nịt ngực corset nữ ren",
        "text": "Corset nịt ngực ren, có gọng định hình, dây đeo điều chỉnh. Tôn dáng, mặc dưới áo dài.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 289_000, "brand": "Sculpt", "image_url": ""},
    },
    {
        "id": "P046",
        "title": "Quần baggy nam jeans rách gối",
        "text": "Baggy jeans ống rộng, rách nhẹ đầu gối, phong cách grunge. Unisex, phối áo thun oversize.",
        "metadata": {"category": "Thời trang", "platform": "Shopee", "price_vnd": 449_000, "brand": "Grunge", "image_url": ""},
    },
    {
        "id": "P047",
        "title": "Áo dạ nữ phong cách Nhật Bản",
        "text": "Áo dạ dáng ngắn phong cách Nhật, cổ lọ, viền nhung. Màu đen, xanh navy. Mùa đông.",
        "metadata": {"category": "Thời trang", "platform": "TikTok Shop", "price_vnd": 599_000, "brand": "JapanStyle", "image_url": ""},
    },
    {
        "id": "P048",
        "title": "Váy chênh lệch xoắn eo hai lớp",
        "text": "Váy chênh lệch lớp ngoài xoắn eo, lớp trong ôm nhẹ. Màu đen, trắng, hồng. Đi chơi.",
        "metadata": {"category": "Thời trang", "platform": "Tiki", "price_vnd": 319_000, "brand": "Asymmetry", "image_url": ""},
    },
    # --- My pham: 30 san pham ---
    {
        "id": "P049",
        "title": "Kem dưỡng mắt Laneige gốc peptide",
        "text": "Kem mắt peptide giảm quầng thâm, nếp nhăn vùng mắt. Tan trong, không bết. Dùng sáng và tối.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 580_000, "brand": "Laneige", "image_url": ""},
    },
    {
        "id": "P050",
        "title": "Son dưỡng môi Lip Glow Dior 004",
        "text": "Son dưỡng môi Lip Glow có màu nhẹ, chuyển sắc theo pH môi. Dưỡng ẩm 12h, màu san hô tự nhiên.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 650_000, "brand": "Dior", "image_url": ""},
    },
    {
        "id": "P051",
        "title": "Kem nền Fenty Beauty matte 140",
        "text": "Kem nền matte Fenty, che phủ vừa, finish lì mịn. 40 tông màu, chống nắng SPF 15.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 890_000, "brand": "Fenty Beauty", "image_url": ""},
    },
    {
        "id": "P052",
        "title": "Phấn mắt palette 12 màu hồng gold",
        "text": "Palette phấn mắt 12 màu hồng gold cổ điển, finish matte/shimmer. Đủ cho look tự nhiên và dramatic.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 480_000, "brand": "3CE", "image_url": ""},
    },
    {
        "id": "P053",
        "title": "Nước hoa nữ Chanel Coco Mademoiselle",
        "text": "Nước hoa Chanel Coco Mademoiselle EDT 50ml. Hương hoa hồng, hoa nhài Pháp. Lưu hương 6h.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 2_450_000, "brand": "Chanel", "image_url": ""},
    },
    {
        "id": "P054",
        "title": "Dầu gội đầu bưởi giảm rụng Haircode",
        "text": "Dầu gội bưởi Organic giảm rụng 30%, kích thích mọc tóc mới. Dành cho tóc yếu, gãy rụng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 189_000, "brand": "Haircode", "image_url": ""},
    },
    {
        "id": "P055",
        "title": "Kem chống nắng Skin1004 centella SPF50",
        "text": "Kem chống nắng centella mỏng nhẹ, không white cast, kiềm dầu. SPF50 PA++++. Phù hợp da nhạy cảm.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 289_000, "brand": "Skin1004", "image_url": ""},
    },
    {
        "id": "P056",
        "title": "Son kem lì Romand Glasting Water 08",
        "text": "Son kem Romand bóng nhẹ, finish thủy trinh long lanh. Màu 08 đào hồng. Lâu trôi 6h.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 195_000, "brand": "Romand", "image_url": ""},
    },
    {
        "id": "P057",
        "title": "Sữa rửa mặt innisfree green tea foam",
        "text": "Sữa rửa mặt trà xanh dịu nhẹ, tạo bọt mịn, cấp ẩm sau rửa. Da khô, da hỗn hợp.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 245_000, "brand": "innisfree", "image_url": ""},
    },
    {
        "id": "P058",
        "title": "Kem dưỡng ẩm Simple Kind to Skin",
        "text": "Kem dưỡng ẩm Simple không mùi, không màu, không paraben. Cấp ẩm 24h, phù hợp da nhạy cảm.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 199_000, "brand": "Simple", "image_url": ""},
    },
    {
        "id": "P059",
        "title": "Mascara Maybelline Lash Sensational",
        "text": "Mascara Maybelline lông mi cong, đen tuyền, chống lem. Công nghệ Aquatex, lông mi mỗi sợi.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 159_000, "brand": "Maybelline", "image_url": ""},
    },
    {
        "id": "P060",
        "title": "Xịt khoáng Avene thermal water 150ml",
        "text": "Xịt khoáng Avene nước nóng thiên nhiên Pháp, làm dịu da, cấp ẩm tức thì. Da nhạy cảm, kích ứng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 320_000, "brand": "Avene", "image_url": ""},
    },
    {
        "id": "P061",
        "title": "Serum trị mụn Cosrx AHA BHA 7",
        "text": "Serum Cosrx AHA 7% BHA 1% giảm mụn đầu đen, thâm sau mụn. Dùng buổi tối, 2-3 lần/tuần.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 385_000, "brand": "Cosrx", "image_url": ""},
    },
    {
        "id": "P062",
        "title": "Kem nền Mac Studio Fix NC25",
        "text": "Kem nền Mac Studio Fix powder foundation, che phủ full, finish satin. Bền 24h, không lem.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 750_000, "brand": "MAC", "image_url": ""},
    },
    {
        "id": "P063",
        "title": "Nước tẩy trang Bioderma hồng",
        "text": "Nước tẩy trang Bioderma Sensibio H2O 500ml. Tẩy sạch makeup, nước hoa, không cần rửa lại.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 395_000, "brand": "Bioderma", "image_url": ""},
    },
    {
        "id": "P064",
        "title": "Kem body trắng da Lactacyd om和保护",
        "text": "Kem dưỡng thể Lactacyd 200ml, dưỡng trắng, mềm mịn. Hương hoa nhài thơm nhẹ. Dùng sau tắm.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 129_000, "brand": "Lactacyd", "image_url": ""},
    },
    {
        "id": "P065",
        "title": "Eyeliner dạ nước black Perfect Diary",
        "text": "Eyeliner dạ nước Perfect Diary đen tuyền, đầu bút mảnh 0.1mm, chống thấm nước. Kẻ mắt chuẩn.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 135_000, "brand": "Perfect Diary", "image_url": ""},
    },
    {
        "id": "P066",
        "title": "Toner Klairs supple preparation unscented",
        "text": "Toner Klairs không mùi, cấp ẩm sâu, làm dịu da sau cleansing. Centella, green tea, licorice.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 445_000, "brand": "Klairs", "image_url": ""},
    },
    {
        "id": "P067",
        "title": "Phấn má hồng Nars Orgasm",
        "text": "Phấn má hồng Nars Orgasm błyszczący, màu san hô hồng ánh kim. Lên màu tự nhiên, finish satin.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 680_000, "brand": "Nars", "image_url": ""},
    },
    {
        "id": "P068",
        "title": "Kem trị nám Transino whitening essence",
        "text": "Essence trị nám Transino chứa tranexamic acid, giảm thâm nám, dưỡng trắng. Dùng 2 lần/ngày.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 890_000, "brand": "Transino", "image_url": ""},
    },
    {
        "id": "P069",
        "title": "Sữa tắm dưỡng ẩm Dove Deep Moisture",
        "text": "Sữa tắm Dove Deep Moisture 750ml, công nghệ Nutritive Serum giữ ẩm 48h. Da mềm mịn sau tắm.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 165_000, "brand": "Dove", "image_url": ""},
    },
    {
        "id": "P070",
        "title": "Highlighter Fenty Beauty Trophy Wife",
        "text": "Highlighter Fenty Trophy Wife gold kim loại, chunky glitter. Body highlighter, highlight mắt.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 720_000, "brand": "Fenty Beauty", "image_url": ""},
    },
    {
        "id": "P071",
        "title": "Kem chống lão hóa Olay Regenerist retinol",
        "text": "Kem chống lão hóa Olay retinol 24, giảm nếp nhăn, cấp ẩm sâu. Dùng buổi tối.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 495_000, "brand": "Olay", "image_url": ""},
    },
    {
        "id": "P072",
        "title": "Dầu xả L'Oreal Elvive hương cam chanh",
        "text": "Dầu xả L'Oreal Elvive Protein, phục hồi tóc hư tổn, mềm mượt. Hương cam chanh tươi mát.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 145_000, "brand": "L'Oreal", "image_url": ""},
    },
    {
        "id": "P073",
        "title": "Serum Vitamin C The Ordinary 23% HA",
        "text": "Serum Vitamin C The Ordinary 23% + HA spheres 2%, làm sáng, giảm thâm. Dùng buổi sáng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 215_000, "brand": "The Ordinary", "image_url": ""},
    },
    {
        "id": "P074",
        "title": "Phấn nén trang điểm Shiseido Boundless",
        "text": "Phấn nén Shiseido Foundation che phủ vừa, finish tự nhiên như da. SPF 20. 4 tông da.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 650_000, "brand": "Shiseido", "image_url": ""},
    },
    {
        "id": "P075",
        "title": "Kem đánh răng Sensodyne trị êm buốt",
        "text": "Kem đánh răng Sensodyne Nova 75g, giảm êm buốt răng nhạy cảm. Dùng 2 lần/ngày.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 125_000, "brand": "Sensodyne", "image_url": ""},
    },
    {
        "id": "P076",
        "title": "Mặt nạ giấy naruko gấc tam sao thất bản",
        "text": "Mặt nạ giấy Naruko gấc tam sao thất bản, cấp ẩm, sáng da, thu nhỏ lỗ chân lông. 10 miếng/hộp.",
        "metadata": {"category": "Mỹ phẩm", "platform": "TikTok Shop", "price_vnd": 175_000, "brand": "Naruko", "image_url": ""},
    },
    {
        "id": "P077",
        "title": "Nước hoa nam Dior Sauvage EDT 100ml",
        "text": "Nước hoa Dior Sauvage EDT 100ml, hương gỗ rang, bergamot tươi mát. Lưu hương 8h. Sang trọng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Tiki", "price_vnd": 2_890_000, "brand": "Dior", "image_url": ""},
    },
    {
        "id": "P078",
        "title": "Kem mắt Kiehl's coriander cấp ẩm",
        "text": "Kem mắt Kiehl's coriander hạt chia, cấp ẩm vùng mắt, giảm bọng. Nhẹ nhàng, không kích ứng.",
        "metadata": {"category": "Mỹ phẩm", "platform": "Shopee", "price_vnd": 1_150_000, "brand": "Kiehl's", "image_url": ""},
    },
    # --- Phu kien: 30 san pham ---
    {
        "id": "P079",
        "title": "Túi đeo chéo nam da PU phong cách Hàn",
        "text": "Túi đeo chéo da PU phong cách Hàn Quốc, ngăn chính + ngăn phụ. Đen, nâu, xanh. Đi học, đi chơi.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 289_000, "brand": "KAccessory", "image_url": ""},
    },
    {
        "id": "P080",
        "title": "Ví đựng thẻ da nam cổ điển",
        "text": "Ví thẻ da PU cổ điển, 8 ngăn thẻ, 2 ngăn tiền, passport. Mỏng nhẹ, bỏ túi áo sơ mi.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 159_000, "brand": "Classic", "image_url": ""},
    },
    {
        "id": "P081",
        "title": "Dây đồng hồ nam da Italy 22mm",
        "text": "Dây đồng hồ da Italy genuine 22mm, các mặt bấm dễ dàng. Nâu, đen. Tương thích nhiều đồng hồ.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 349_000, "brand": "Italian", "image_url": ""},
    },
    {
        "id": "P082",
        "title": "Kính râm nam gọng tròn vintage",
        "text": "Kính râm gọng tròn phong cách vintage, tròng polarized chống UV400. Vàng gold, bạc. Lịch lãm.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 229_000, "brand": "Retro", "image_url": ""},
    },
    {
        "id": "P083",
        "title": "Mũ lưỡi trai snapback nam thêu logo",
        "text": "Mũ snapback thêu logo phong cách streetwear, độ sâu vừa, có nút điều chỉnh. Đen, trắng, đỏ.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 129_000, "brand": "Street", "image_url": ""},
    },
    {
        "id": "P084",
        "title": "Thắt lưng nam da bò đen 3.5cm",
        "text": "Thắt lưng da bò genuine 3.5cm, khóa kim loại chống gỉ, đường chỉ đều. Cổ điển, bền đẹp.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 389_000, "brand": "Genuine", "image_url": ""},
    },
    {
        "id": "P085",
        "title": "Túi clutch nữ da bóng phong cách đi tiệc",
        "text": "Clutch da bóng nhỏ gọn, cầm tay hoặc xách. Màu vàng gold, bạc. Đi tiệc, dự sự kiện.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 299_000, "brand": "GlamNight", "image_url": ""},
    },
    {
        "id": "P086",
        "title": "Bông tai nam stainless steel tròn",
        "text": "Bông tai nam stainless steel 316L không gỉ, thiết kế tròn đơn giản. Bạc, đen. Nam tính.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 89_000, "brand": "Steel", "image_url": ""},
    },
    {
        "id": "P087",
        "title": "Balo du lịch 50L có ngăn laptop 17 inch",
        "text": "Balo du lịch 50L, ngăn laptop 17 inch đệm êm, chống sốc. Có ngăn giày, quần áo riêng. Đi phượt.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 659_000, "brand": "TravelPro", "image_url": ""},
    },
    {
        "id": "P088",
        "title": "Khăn choàng nữ lụa 70x200cm",
        "text": "Khăn choàng lụa mềm mại 70x200cm, in hoa văn thanh lịch. Buộc tóc, quấn cổ, phối đồ.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 189_000, "brand": "SilkScarf", "image_url": ""},
    },
    {
        "id": "P089",
        "title": "Găng tay da nam chống nắng",
        "text": "Găng tay da PU chống nắng, lòng bàn tay có đệm. Bảo vệ tay khi lái xe, đạp xe.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 149_000, "brand": "HandGuard", "image_url": ""},
    },
    {
        "id": "P090",
        "title": "Dây chuyền nam vàng 18k mặt tròn",
        "text": "Dây chuyền nam vàng 18K, mặt tròn đơn giản thanh lịch. Dây 50cm có móc cài. Sang trọng.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 1_890_000, "brand": "GoldJewel", "image_url": ""},
    },
    {
        "id": "P091",
        "title": "Túi xách nữ da PU cỡ vừa đi làm",
        "text": "Túi xách da PU cỡ vừa, 3 ngăn chính, có khóa. Màu đen, nâu, be. Đi làm, đi học.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 389_000, "brand": "WorkBag", "image_url": ""},
    },
    {
        "id": "P092",
        "title": "Nơ tóc nữ ren phong cách cô dâu",
        "text": "Nơ tóc ren mỏng nhẹ, phong cách cô dâu thanh lịch. Cài tóc, buộc tóc, trang trí.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 79_000, "brand": "Bridal", "image_url": ""},
    },
    {
        "id": "P093",
        "title": "Đồng hồ thông minh Huawei Watch GT 4",
        "text": "Huawei Watch GT 4 46mm AMOLED, GPS, theo dõi sức khỏe, 14 ngày pin. Vòng bezel kim loại.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 4_990_000, "brand": "Huawei", "image_url": ""},
    },
    {
        "id": "P094",
        "title": "Túi đựng giày du lịch chống thấm",
        "text": "Túi đựng giày du lịch vải chống thấm, 2 ngăn đựng 2 đôi. Gấp gọn, nhẹ. Đi du lịch.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 99_000, "brand": "TravelGear", "image_url": ""},
    },
    {
        "id": "P095",
        "title": "Kẹp tóc kim loại vàng rose hair claw",
        "text": "Kẹp tóc hair claw kim loại vàng rose, size lớn. Bắt tóc, điểm xuyết. Phong cách Pháp.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 69_000, "brand": "ParisClaw", "image_url": ""},
    },
    {
        "id": "P096",
        "title": "Vòng tay nam da vàng khóa bướu",
        "text": "Vòng tay nam da bọc vải kết hợp charm vàng, khóa bướu. Phong cách Boho, vintage.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 189_000, "brand": "BohoStyle", "image_url": ""},
    },
    {
        "id": "P097",
        "title": "Túi belt bag nam chống nước",
        "text": "Belt bag nam vải chống nước, đeo chéo hoặc quấn eo. Ngăn zip an toàn. Phượt, dạo phố.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 229_000, "brand": "UrbanGear", "image_url": ""},
    },
    {
        "id": "P098",
        "title": "Mắt kính bluetooth nam chống bụi",
        "text": "Kính nam có bluetooth tích hợp, chống bụi UV, loa 2 bên. Nghe nhạc, gọi điện khi lái xe.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 459_000, "brand": "TechVision", "image_url": ""},
    },
    {
        "id": "P099",
        "title": "Bộ trang sức nữ mạ vàng trắng phong cách sang",
        "text": "Bộ trang sức gồm vòng cổ + vòng tay + bông tai mạ vàng trắng. Phong cách thanh lịch.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 389_000, "brand": "LuxJewel", "image_url": ""},
    },
    {
        "id": "P100",
        "title": "Dây đeo Apple Watch silicone 40mm nhiều màu",
        "text": "Dây silicone Apple Watch 38-40-41mm, nhiều màu sắc tươi sáng. Thay nhanh, nhẹ êm.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 79_000, "brand": "WatchBand", "image_url": ""},
    },
    {
        "id": "P101",
        "title": "Nón lưỡi trai nữ dây rút satin",
        "text": "Nón lưỡi trai nữ satin mềm mại, dây rút buộc tóc. Màu pastel, đen, trắng. Phong cách Y2K.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 119_000, "brand": "Y2KHat", "image_url": ""},
    },
    {
        "id": "P102",
        "title": "Ví đựng điện thoại nam da PU thẻ ngang",
        "text": "Ví phone case da PU tích hợp đựng thẻ, tiền, tai nghe. Mỏng 8mm. Iphone, Samsung các dòng.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 199_000, "brand": "PhoneCase", "image_url": ""},
    },
    {
        "id": "P103",
        "title": "Túi tote da vegan phong cách tối giản",
        "text": "Tote da vegan thuần chay, form trụ đứng, không bến. Laptop 14 inch. Phong cách tối giản.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 349_000, "brand": "Minimalist", "image_url": ""},
    },
    {
        "id": "P104",
        "title": "Bông tai drop nữ ngọc trai freshwater",
        "text": "Bông tai drop ngọc trai freshwater 8mm, khóa stainless. Phong cách Nhật Bản thanh lịch.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 259_000, "brand": "PearlDrop", "image_url": ""},
    },
    {
        "id": "P105",
        "title": "Gương makeup tròn có đèn LED mini",
        "text": "Gương tròn để bàn có đèn LED cảm ứng, zoom 5x. Sạc USB. Trang điểm chuẩn.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 229_000, "brand": "LEDMirror", "image_url": ""},
    },
    {
        "id": "P106",
        "title": "Dây buộc tóc lụa satin 5cm 8 cái",
        "text": "Bộ dây buộc tóc lụa satin 8 cái, 5cm, nhiều màu pastel. Mềm mại không gây rụng tóc.",
        "metadata": {"category": "Phụ kiện", "platform": "Shopee", "price_vnd": 49_000, "brand": "SatinTie", "image_url": ""},
    },
    {
        "id": "P107",
        "title": "Móc khóa da handmade nam personalized",
        "text": "Móc khóa da handmade khắc tên, có khe đựng thẻ nhỏ. Quà tặng ý nghĩa. Cá nhân hóa.",
        "metadata": {"category": "Phụ kiện", "platform": "TikTok Shop", "price_vnd": 89_000, "brand": "HandCraft", "image_url": ""},
    },
    {
        "id": "P108",
        "title": "Túi trống nam canvas phong cách vintage",
        "text": "Túi trống canvas vintage, 2 ngăn chính, có khóa zip. Phong cách du lịch, festival.",
        "metadata": {"category": "Phụ kiện", "platform": "Tiki", "price_vnd": 299_000, "brand": "VintageBag", "image_url": ""},
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