/**
 * Mock data — AREA-303 e-commerce domain.
 * Deterministic so charts hydrate identically on the server and client.
 *
 * Domains:
 * - KPIS: today's revenue, orders, conversion, AOV
 * - TIMESERIES: hourly GMV across 3 categories for the last 24h
 * - ALERTS: cross-feature alerts (returns, fake review, low stock, churn spike, sentiment drop)
 * - PROVINCES: 63 Vietnam provinces for supply-chain risk heatmap (idea #16)
 * - PRODUCTS: small fixture used by #03 Personal Shopper, #09 Content Generator, #11 RecSys
 */

export type SeriesPoint = { t: string; v: number };

export type Kpi = {
  id: string;
  label: string;
  value: number;
  unit?: string;
  delta: number; // percent, signed
  spark: number[];
  /** When true, a downward delta is the "good" outcome. */
  inverted?: boolean;
};

export const KPIS: Kpi[] = [
  {
    id: "revenue",
    label: "Revenue today",
    value: 184_230_000,
    unit: "₫",
    delta: 12.4,
    spark: [120, 132, 128, 141, 152, 148, 160, 158, 167, 172, 170, 184].map((m) => m * 1_000_000),
  },
  {
    id: "orders",
    label: "Orders today",
    value: 2_847,
    delta: 8.6,
    spark: [1.8, 2.0, 1.9, 2.1, 2.3, 2.2, 2.4, 2.5, 2.6, 2.7, 2.75, 2.85].map((m) => m * 1000),
  },
  {
    id: "conversion",
    label: "Conversion rate",
    value: 3.42,
    unit: "%",
    delta: 0.4,
    spark: [3.0, 3.1, 3.05, 3.15, 3.2, 3.18, 3.25, 3.28, 3.32, 3.36, 3.4, 3.42],
  },
  {
    id: "aov",
    label: "Avg order value",
    value: 487_000,
    unit: "₫",
    delta: -1.8,
    inverted: false,
    spark: [510, 505, 502, 498, 495, 492, 490, 489, 488, 488, 487, 487].map((m) => m * 1000),
  },
];

/** Hourly GMV (₫ million) for last 24h, by top-level category. */
export const TIMESERIES: Array<{ t: string; fashion: number; beauty: number; accessories: number }> =
  Array.from({ length: 24 }, (_, i) => {
    const hour = String(i).padStart(2, "0");
    const base = (h: number) => 80 + Math.sin((h + i) / 3) * 32 + (h % 6) * 4;
    return {
      t: `${hour}:00`,
      fashion: Math.round(base(3) * 10) / 10,
      beauty: Math.round(base(5) * 10) / 10 - 18,
      accessories: Math.round(base(7) * 10) / 10 - 32,
    };
  });

export type AlertSeverity = "critical" | "warning" | "info";
export type AlertStatus = "open" | "monitoring" | "resolved";
export type AlertSource =
  | "review-analyzer"
  | "churn"
  | "fake-review"
  | "return-predict"
  | "supply-chain"
  | "sentiment-alert";

export type Alert = {
  id: string;
  feature: AlertSource;
  featureLabel: string;
  region: string;
  severity: AlertSeverity;
  status: AlertStatus;
  startedAt: string;
  message: string;
};

export const ALERTS: Alert[] = [
  {
    id: "ALT-2407",
    feature: "return-predict",
    featureLabel: "Return Predict",
    region: "Hà Nội",
    severity: "critical",
    status: "open",
    startedAt: "2026-07-08 03:42",
    message: "Áo khoác denim size M — return rate 28%, x2 baseline",
  },
  {
    id: "ALT-2406",
    feature: "churn",
    featureLabel: "Churn Radar",
    region: "TP.HCM",
    severity: "warning",
    status: "monitoring",
    startedAt: "2026-07-08 02:18",
    message: "Segment 'At Risk' tăng 14% trong 24h — 312 customers",
  },
  {
    id: "ALT-2405",
    feature: "sentiment-alert",
    featureLabel: "Sentiment Alert",
    region: "Đà Nẵng",
    severity: "info",
    status: "resolved",
    startedAt: "2026-07-07 23:51",
    message: "Spike negative về 'giao hàng chậm' — 47 mentions trong 1h",
  },
  {
    id: "ALT-2404",
    feature: "supply-chain",
    featureLabel: "Supply Chain",
    region: "Bắc Ninh",
    severity: "warning",
    status: "open",
    startedAt: "2026-07-07 22:09",
    message: "Kho tổng Bắc Ninh — dự báo stockout son môi trong 5 ngày",
  },
  {
    id: "ALT-2403",
    feature: "fake-review",
    featureLabel: "Fake Review",
    region: "—",
    severity: "info",
    status: "resolved",
    startedAt: "2026-07-07 19:30",
    message: "Phát hiện 23 review rác trên listing serum C-vit",
  },
];

/** 63 Vietnam provinces (centroids) — supply chain #16 heatmap. */
export type ProvinceNode = {
  id: string;
  name: string;
  region: "north" | "central" | "south";
  lat: number;
  lng: number;
  status: "ok" | "warn" | "critical";
  load: number; // 0..1 supply chain risk
};

export const PROVINCES: ProvinceNode[] = [
  { id: "p-hn",  name: "Hà Nội",       region: "north",   lat: 21.0285,  lng: 105.8542,  status: "ok",       load: 0.42 },
  { id: "p-hcm", name: "TP.HCM",       region: "south",   lat: 10.8231,  lng: 106.6297,  status: "warn",     load: 0.74 },
  { id: "p-dn",  name: "Đà Nẵng",      region: "central", lat: 16.0544,  lng: 108.2022,  status: "ok",       load: 0.38 },
  { id: "p-hp",  name: "Hải Phòng",    region: "north",   lat: 20.8449,  lng: 106.6881,  status: "ok",       load: 0.51 },
  { id: "p-ct",  name: "Cần Thơ",      region: "south",   lat: 10.0452,  lng: 105.7469,  status: "ok",       load: 0.34 },
  { id: "p-bn",  name: "Bắc Ninh",     region: "north",   lat: 21.1861,  lng: 106.0763,  status: "critical", load: 0.91 },
  { id: "p-bd",  name: "Bình Dương",   region: "south",   lat: 11.3254,  lng: 106.4770,  status: "warn",     load: 0.78 },
  { id: "p-dn2", name: "Đồng Nai",     region: "south",   lat: 10.9574,  lng: 106.8426,  status: "ok",       load: 0.55 },
  { id: "p-la",  name: "Long An",      region: "south",   lat: 10.6956,  lng: 106.2431,  status: "ok",       load: 0.46 },
  { id: "p-tt",  name: "Thừa Thiên Huế",region: "central", lat: 16.4637,  lng: 107.5909,  status: "ok",       load: 0.40 },
  { id: "p-kh",  name: "Khánh Hòa",    region: "central", lat: 12.2388,  lng: 109.1967,  status: "ok",       load: 0.36 },
  { id: "p-ls",  name: "Lâm Đồng",     region: "central", lat: 11.5753,  lng: 108.1429,  status: "ok",       load: 0.32 },
];

/* ------------------------------------------------------------------ */
/* Fixture products — used by Personal Shopper / RecSys / Content Gen */
/* ------------------------------------------------------------------ */

export type Product = {
  id: string;
  name: string;
  brand: string;
  category: "Thời trang" | "Mỹ phẩm" | "Phụ kiện";
  platform: "Shopee" | "Tiki" | "TikTok Shop";
  priceVnd: number;
  rating: number;
  reviews: number;
  similarity?: number; // 0..1, used by visual search and recsys
  imageHue: number; // 0..360 — synthesized swatch, deterministic
  imageUrl?: string; // real product photo; falls back to icon when empty
  description: string;
};

// Unsplash photo IDs for accurate product images
const UNSPLASH_IMAGES: Record<string, string> = {
  // Thời trang - Áo
  polo: "https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=400&fit=crop&q=80",
  dress_shirt: "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400&h=400&fit=crop&q=80",
  tshirt: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop&q=80",
  hoodie: "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=400&fit=crop&q=80",
  bomber_jacket: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&h=400&fit=crop&q=80",
  denim_jacket: "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400&h=400&fit=crop&q=80",
  knitwear: "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=400&fit=crop&q=80",
  winter_coat: "https://images.unsplash.com/photo-1544022613-e87ca75a784a?w=400&h=400&fit=crop&q=80",
  blazer: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&q=80",

  // Thời trang - Quần
  jogger: "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=400&h=400&fit=crop&q=80",
  shorts: "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=400&fit=crop&q=80",
  jeans: "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop&q=80",
  leggings: "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400&h=400&fit=crop&q=80",

  // Thời trang - Váy/Đầm
  skirt: "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&h=400&fit=crop&q=80",
  dress: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=400&fit=crop&q=80",

  // Thời trang - Giày
  sneakers: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop&q=80",
  boots: "https://images.unsplash.com/photo-1542840410-8e73aa1f5d9c?w=400&h=400&fit=crop&q=80",
  sandals: "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400&h=400&fit=crop&q=80",

  // Mỹ phẩm
  lipstick: "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=400&h=400&fit=crop&q=80",
  serum: "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400&h=400&fit=crop&q=80",
  moisturizer: "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=400&h=400&fit=crop&q=80",
  sunscreen: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&q=80",
  foundation: "https://images.unsplash.com/photo-1631214524020-7e18db9a8f92?w=400&h=400&fit=crop&q=80",
  toner: "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=400&h=400&fit=crop&q=80",
  eyeshadow: "https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400&h=400&fit=crop&q=80",
  mascara: "https://images.unsplash.com/photo-1631214540553-ff044a3ff1d4?w=400&h=400&fit=crop&q=80",
  blush: "https://images.unsplash.com/photo-1596704017254-9b121068fb31?w=400&h=400&fit=crop&q=80",
  perfume: "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=400&fit=crop&q=80",
  face_mask: "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400&h=400&fit=crop&q=80",
  face_wash: "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=400&fit=crop&q=80",

  // Phụ kiện - Túi
  handbag: "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400&h=400&fit=crop&q=80",
  tote_bag: "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?w=400&h=400&fit=crop&q=80",
  crossbody_bag: "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=400&fit=crop&q=80",
  backpack: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop&q=80",
  wallet: "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=400&fit=crop&q=80",

  // Phụ kiện - Khác
  sunglasses: "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop&q=80",
  cap: "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400&h=400&fit=crop&q=80",
  watch: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=400&fit=crop&q=80",
  necklace: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=400&fit=crop&q=80",
  bracelet: "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=400&h=400&fit=crop&q=80",
  earrings: "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=400&h=400&fit=crop&q=80",
  scarf: "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=400&h=400&fit=crop&q=80",

  // Khác
  pajamas: "https://images.unsplash.com/photo-1522778119026-d647f0596c20?w=400&h=400&fit=crop&q=80",
  default: "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400&h=400&fit=crop&q=80",
};

function getMockImageUrl(name: string, category: string): string {
  const n = `${name} ${category}`.toLowerCase();
  const has = (...ks: string[]) => ks.some((k) => n.includes(k));

  // Thời trang
  if (has("áo polo", "polo")) return UNSPLASH_IMAGES.polo;
  if (has("áo sơ mi", "sơ mi")) return UNSPLASH_IMAGES.dress_shirt;
  if (has("áo thun", "áo phông", "thun", "oversize")) return UNSPLASH_IMAGES.tshirt;
  if (has("hoodie", "áo hoodie")) return UNSPLASH_IMAGES.hoodie;
  if (has("áo khoác bomber", "bomber")) return UNSPLASH_IMAGES.bomber_jacket;
  if (has("áo khoác denim", "denim", "áo khoác")) return UNSPLASH_IMAGES.denim_jacket;
  if (has("áo len", "cardigan", "áo vest", "blazer")) return UNSPLASH_IMAGES.knitwear;
  if (has("áo dạ", "áo phao", "down jacket")) return UNSPLASH_IMAGES.winter_coat;
  if (has("áo vest", "blazer")) return UNSPLASH_IMAGES.blazer;
  if (has("quần jogger", "jogger", "quần baggy", "baggy")) return UNSPLASH_IMAGES.jogger;
  if (has("quần short", "short")) return UNSPLASH_IMAGES.shorts;
  if (has("quần", "jean", "denim")) return UNSPLASH_IMAGES.jeans;
  if (has("váy", "đầm", "dress", "midi")) return has("đầm") ? UNSPLASH_IMAGES.dress : UNSPLASH_IMAGES.skirt;
  if (has("giày", "sneaker", "dép", "sandal")) return has("sandal") ? UNSPLASH_IMAGES.sandals : UNSPLASH_IMAGES.sneakers;
  if (has("boots", "boot")) return UNSPLASH_IMAGES.boots;

  // Mỹ phẩm
  if (has("son", "tint", "lipstick")) return UNSPLASH_IMAGES.lipstick;
  if (has("serum", "vitamin c", "bha", "aha", "tinh chất", "essence")) return UNSPLASH_IMAGES.serum;
  if (has("mặt nạ", "mask", "laneige", "sleeping")) return UNSPLASH_IMAGES.face_mask;
  if (has("kem", "cream", "dưỡng", "lotion", "cushion")) return UNSPLASH_IMAGES.moisturizer;
  if (has("toner", "rửa mặt", "sữa rửa", "sữa tắm")) return UNSPLASH_IMAGES.face_wash;
  if (has("chống nắng", "anessa", "spf")) return UNSPLASH_IMAGES.sunscreen;
  if (has("nước hoa", "perfume", "fragrance")) return UNSPLASH_IMAGES.perfume;
  if (has("phấn", "makeup")) return UNSPLASH_IMAGES.foundation;
  if (has("mascara", "eyeliner", "kẻ mắt")) return UNSPLASH_IMAGES.mascara;
  if (has("phấn má", "blush", "highlighter")) return UNSPLASH_IMAGES.blush;

  // Phụ kiện
  if (has("túi", "tote", "bag", "balo")) {
    if (has("tote")) return UNSPLASH_IMAGES.tote_bag;
    if (has("đeo chéo", "chéo")) return UNSPLASH_IMAGES.crossbody_bag;
    if (has("balo")) return UNSPLASH_IMAGES.backpack;
    return UNSPLASH_IMAGES.handbag;
  }
  if (has("kính", "sunglass", "mát")) return UNSPLASH_IMAGES.sunglasses;
  if (has("đồng hồ", "casio", "watch")) return UNSPLASH_IMAGES.watch;
  if (has("ví", "wallet")) return UNSPLASH_IMAGES.wallet;
  if (has("dây chuyền", "necklace")) return UNSPLASH_IMAGES.necklace;
  if (has("vòng tay", "bracelet", "lắc")) return UNSPLASH_IMAGES.bracelet;
  if (has("bông tai", " earrings", "hoa tai")) return UNSPLASH_IMAGES.earrings;
  if (has("khăn", "scarf", "choàng")) return UNSPLASH_IMAGES.scarf;
  if (has("mũ", "nón", "cap")) return UNSPLASH_IMAGES.cap;

  return UNSPLASH_IMAGES.default;
}

export const PRODUCTS: Product[] = [
  {
    id: "P001",
    name: "Áo khoác denim unisex form rộng",
    brand: "Local Brand X",
    category: "Thời trang",
    platform: "Shopee",
    priceVnd: 489_000,
    rating: 4.6,
    reviews: 1284,
    similarity: 0.92,
    imageHue: 215,
    imageUrl: "https://picsum.photos/seed/denim-jacket/400/400",
    description:
      "Denim 12oz wash nhẹ, form rộng unisex, 2 túi ngực + 2 túi hông. Phù hợp đi học, đi chơi.",
  },
  {
    id: "P002",
    name: "Serum Vitamin C 15% NUDESTIX",
    brand: "NUDESTIX",
    category: "Mỹ phẩm",
    platform: "Tiki",
    priceVnd: 720_000,
    rating: 4.4,
    reviews: 892,
    similarity: 0.88,
    imageHue: 45,
    imageUrl: "https://picsum.photos/seed/serum/400/400",
    description:
      "Serum C ổn định, sáng da, giảm thâm sau 4 tuần. Dùng buổi sáng, kết hợp kem chống nắng.",
  },
  {
    id: "P003",
    name: "Túi tote canvas in họa tiết",
    brand: "OEM",
    category: "Phụ kiện",
    platform: "TikTok Shop",
    priceVnd: 159_000,
    rating: 4.7,
    reviews: 3201,
    similarity: 0.81,
    imageHue: 160,
    imageUrl: "https://picsum.photos/seed/handbag/400/400",
    description:
      "Tote canvas dày 12oz, in lụa 2 mặt, đường chỉ gấp đôi. Chứa laptop 14 inch.",
  },
  {
    id: "P004",
    name: "Son tint lì Bourjois Velvet 21",
    brand: "Bourjois",
    category: "Mỹ phẩm",
    platform: "Shopee",
    priceVnd: 295_000,
    rating: 4.5,
    reviews: 612,
    similarity: 0.76,
    imageHue: 350,
    imageUrl: "https://picsum.photos/seed/lipstick/400/400",
    description:
      "Tint lì lâu trôi 8h, finish velvet không khô môi. Tông 21 — đỏ gạch.",
  },
  {
    id: "P005",
    name: "Quần ống rộng lưng cao linen",
    brand: "Local Brand Y",
    category: "Thời trang",
    platform: "Tiki",
    priceVnd: 369_000,
    rating: 4.3,
    reviews: 458,
    similarity: 0.73,
    imageHue: 35,
    imageUrl: "https://picsum.photos/seed/jeans/400/400",
    description:
      "Linen pha, lưng cao che bụng, ống rộng xếp ly. Size S–XL.",
  },
  {
    id: "P006",
    name: "Mặt nạ ngủ Laneige Water Sleeping Mask",
    brand: "Laneige",
    category: "Mỹ phẩm",
    platform: "Shopee",
    priceVnd: 650_000,
    rating: 4.8,
    reviews: 2410,
    similarity: 0.69,
    imageHue: 200,
    imageUrl: "https://picsum.photos/seed/face-mask/400/400",
    description:
      "Mặt nạ ngủ cấp ẩm 8h, dùng sau serum. Phù hợp da khô, da hỗn hợp.",
  },
  {
    id: "P007",
    name: "Đồng hồ Casio MTP-V002 minimal",
    brand: "Casio",
    category: "Phụ kiện",
    platform: "TikTok Shop",
    priceVnd: 489_000,
    rating: 4.7,
    reviews: 1803,
    similarity: 0.65,
    imageHue: 0,
    imageUrl: "https://picsum.photos/seed/watch/400/400",
    description:
      "Mặt tròn 38mm, dây thép không gỉ, chống nước 30m. Bảo hành 1 năm.",
  },
  {
    id: "P008",
    name: "Áo thun oversize cotton 220gsm",
    brand: "Local Brand Z",
    category: "Thời trang",
    platform: "Shopee",
    priceVnd: 189_000,
    rating: 4.5,
    reviews: 5210,
    similarity: 0.60,
    imageHue: 270,
    imageUrl: "https://picsum.photos/seed/tshirt/400/400",
    description:
      "Cotton 220gsm dày dặn, form oversize, in lụa không bong. 5 màu.",
  },
  {
    id: "P009",
    name: "Sữa rửa mặt CeraVe cho da dầu mụn",
    brand: "CeraVe",
    category: "Mỹ phẩm",
    platform: "Tiki",
    priceVnd: 285_000,
    rating: 4.6,
    reviews: 1543,
    similarity: 0.58,
    imageHue: 180,
    imageUrl: "https://picsum.photos/seed/face-wash/400/400",
    description:
      "Sữa rửa mặt tạo bọt, kiểm soát dầu, chứa ceramide + niacinamide. Da dầu, da mụn.",
  },
  {
    id: "P010",
    name: "Kem chống nắng Anessa SPF50+ PA++++",
    brand: "Anessa",
    category: "Mỹ phẩm",
    platform: "Shopee",
    priceVnd: 520_000,
    rating: 4.7,
    reviews: 2890,
    similarity: 0.55,
    imageHue: 50,
    imageUrl: "https://picsum.photos/seed/sunscreen/400/400",
    description:
      "Chống nắng kiềm dầu, không bết, phù hợp da dầu mụn. Dùng bước cuối buổi sáng.",
  },
  {
    id: "P011",
    name: "Toner BHA Paula's Choice 2%",
    brand: "Paula's Choice",
    category: "Mỹ phẩm",
    platform: "Tiki",
    priceVnd: 610_000,
    rating: 4.5,
    reviews: 876,
    similarity: 0.52,
    imageHue: 120,
    imageUrl: "https://picsum.photos/seed/toner/400/400",
    description:
      "BHA 2% giảm mụn ẩn, thông thoáng lỗ chân lông. Da dầu, da mụn nhẹ.",
  },
  {
    id: "P012",
    name: "Kem dưỡng ẩm gel không dầu Neutrogena",
    brand: "Neutrogena",
    category: "Mỹ phẩm",
    platform: "Shopee",
    priceVnd: 240_000,
    rating: 4.3,
    reviews: 1120,
    similarity: 0.48,
    imageHue: 90,
    imageUrl: "https://picsum.photos/seed/moisturizer/400/400",
    description:
      "Gel dưỡng ẩm oil-free cấp nước, không gây bít tắc. Hợp da dầu mụn.",
  },
  {
    id: "P013",
    name: "Cushion trang điểm kiềm dầu 3CE",
    brand: "3CE",
    category: "Mỹ phẩm",
    platform: "TikTok Shop",
    priceVnd: 430_000,
    rating: 4.4,
    reviews: 654,
    similarity: 0.45,
    imageHue: 330,
    imageUrl: "https://picsum.photos/seed/foundation/400/400",
    description:
      "Cushion finish lì, kiềm dầu 8h, SPF35. Tông tự nhiên cho da dầu.",
  },
  {
    id: "P014",
    name: "Váy đầm midi cổ vuông tay bồng",
    brand: "Local Brand W",
    category: "Thời trang",
    platform: "Shopee",
    priceVnd: 359_000,
    rating: 4.2,
    reviews: 312,
    similarity: 0.42,
    imageHue: 280,
    imageUrl: "https://picsum.photos/seed/dress/400/400",
    description:
      "Đầm midi cổ vuông, tay bồng, vải tuyết mưa. Đi tiệc, đi làm. Size S–L.",
  },
  {
    id: "P015",
    name: "Giày sneaker trắng đế cao 4cm",
    brand: "Local Brand V",
    category: "Thời trang",
    platform: "Tiki",
    priceVnd: 429_000,
    rating: 4.1,
    reviews: 287,
    similarity: 0.38,
    imageHue: 0,
    imageUrl: "https://picsum.photos/seed/sneakers/400/400",
    description:
      "Sneaker da PU trắng, đế cao 4cm tôn dáng, lót êm. Size 35–43.",
  },
  {
    id: "P016",
    name: "Quần jean nữ ống suông lưng cao",
    brand: "Local Brand U",
    category: "Thời trang",
    platform: "Shopee",
    priceVnd: 329_000,
    rating: 4.4,
    reviews: 543,
    similarity: 0.35,
    imageHue: 220,
    imageUrl: "https://picsum.photos/seed/jeans/400/400",
    description:
      "Jean cotton co giãn nhẹ, ống suông, lưng cao. Xanh wash cổ điển.",
  },
  {
    id: "P017",
    name: "Kính mát nữ gọng vuông trendy",
    brand: "OEM",
    category: "Phụ kiện",
    platform: "TikTok Shop",
    priceVnd: 149_000,
    rating: 4.0,
    reviews: 1876,
    similarity: 0.32,
    imageHue: 60,
    imageUrl: "https://picsum.photos/seed/sunglasses/400/400",
    description:
      "Gọng acetate vuông, tròng chống UV400. Nhiều màu, kèm hộp + khăn.",
  },
  {
    id: "P018",
    name: "Balo laptop chống nước 15.6 inch",
    brand: "OEM",
    category: "Phụ kiện",
    platform: "Shopee",
    priceVnd: 259_000,
    rating: 4.5,
    reviews: 2109,
    similarity: 0.30,
    imageHue: 150,
    imageUrl: "https://picsum.photos/seed/backpack/400/400",
    description:
      "Balo chống nước, ngăn laptop 15.6 inch có đệm, cổng sạc USB. Đi học/đi làm.",
  },
];

/* Personal Shopper quick-prompt chips — Vietnamese. */
export const SHOPPER_CHIPS = [
  "Quà sinh nhật cho bạn nữ 25 tuổi, tầm 500k",
  "Son môi tự nhiên cho da ngăm",
  "Đồ đi làm công sở mùa hè dưới 1 triệu",
  "Skincare cho da dầu mụn nhẹ",
  "Phụ kiện vintage phong cách Hàn Quốc",
];

/* ------------------------------------------------------------------ */
/* Seller Coach — 5-step audit + 4-week roadmap                     */
/* ------------------------------------------------------------------ */

export type AuditStep = {
  id: string;
  label: string;
  score: number; // 0..100
  tip: string;
};

export const SELLER_AUDIT: AuditStep[] = [
  { id: "listing",   label: "Listing Quality", score: 72, tip: "Mô tả ngắn, nên bổ sung 2-3 bullet về chất liệu + cách dùng." },
  { id: "pricing",   label: "Pricing",         score: 64, tip: "Đang cao hơn median category 8% — thử giảm 5-7% trong 7 ngày." },
  { id: "visuals",   label: "Visuals",         score: 58, tip: "Ảnh chính thiếu sáng, hero subject chỉ chiếm 32% frame." },
  { id: "reviews",   label: "Reviews",         score: 81, tip: "Reply rate 92%, nhưng phản hồi negative chậm (>24h)." },
  { id: "inventory", label: "Inventory",       score: 47, tip: "SKU top bán stockout 3 lần trong 30 ngày — set reorder buffer." },
];

export type RoadmapWeek = { week: number; title: string; bullets: string[] };

export const SELLER_ROADMAP: RoadmapWeek[] = [
  {
    week: 1,
    title: "Fix nền tảng",
    bullets: [
      "Reorder buffer cho 5 SKU top",
      "Reply 100% review negative trong 12h",
      "Đẩy 2 ảnh mới cho listing đèn sales",
    ],
  },
  {
    week: 2,
    title: "Tối ưu listing",
    bullets: [
      "Rewrite mô tả cho 10 listing theo AI gợi ý",
      "A/B test 3 hero images",
      "Bổ sung 5 video 15s cho top SKUs",
    ],
  },
  {
    week: 3,
    title: "Pricing & promotion",
    bullets: [
      "Điều chỉnh giá về median ± 5%",
      "Chạy voucher 10% trong 48h cho segment Loyalty",
      "Combo 3 sản phẩm bán chạy",
    ],
  },
  {
    week: 4,
    title: "Scale & retention",
    bullets: [
      "Ra mắt 2 SKU mới theo trend Q3",
      "Email win-back cho segment At Risk",
      "Review & lặp lại vòng audit",
    ],
  },
];

/* ------------------------------------------------------------------ */
/* Content Generator — 3 platform variants                          */
/* ------------------------------------------------------------------ */

export type ContentVariant = {
  platform: "Shopee" | "Tiki" | "TikTok Shop";
  title: string;
  body: string;
  predictedCtr: number; // 0..1
  rationale: string;
};

export const CONTENT_DEMO: ContentVariant[] = [
  {
    platform: "Shopee",
    title: "Áo khoác denim unisex — form rộng, wash nhẹ, mặc 4 mùa",
    body:
      "Denim 12oz wash nhẹ — không bai, không xù. Form rộng unisex, 2 size S–XL. Bỏ túi ngực + túi hông đủ laptop 14\". Free ship đơn từ 250k.",
    predictedCtr: 0.082,
    rationale: "Hero keywords: 'denim unisex', 'form rộng', '4 mùa'. Mention Free ship — tăng 18% CTR.",
  },
  {
    platform: "Tiki",
    title: "Áo khoác denim form rộng unisex | Local Brand X | Chính hãng",
    body:
      "Sản phẩm chính hãng Local Brand X. Chất liệu denim 12oz wash nhẹ, đường may gấp đôi. Đổi trả 7 ngày nếu lỗi. TikiNOW giao 2h tại TP.HCM & Hà Nội.",
    predictedCtr: 0.071,
    rationale: "Đề cao 'Chính hãng' + 'TikiNOW' — phù hợp khách Tiki tìm đảm bảo giao nhanh.",
  },
  {
    platform: "TikTok Shop",
    title: "DENIM JACKET siêu xinh — đi học đi chơi đều ổn 🥹",
    body:
      "Best seller tuần qua! Wash nhẹ mặc siêu mềm, form rộng giấu bụng. Đủ size S–XL. Comment 'DENIM' để nhận voucher 30k.",
    predictedCtr: 0.118,
    rationale: "Hook ngắn + emoji + comment-to-claim — pattern TikTok Shop thường thắng trên impulse.",
  },
];

/* ------------------------------------------------------------------ */
/* Recsys — Traditional CF vs AI reasoning                          */
/* ------------------------------------------------------------------ */

export type Recommendation = Product & { reason: string };

export const RECSYS_TRADITIONAL: Recommendation[] = PRODUCTS.slice(0, 4).map((p) => ({
  ...p,
  reason: "Collaborative filtering: người dùng tương tự (cosine 0.83) cũng đã mua.",
}));

export const RECSYS_AI: Recommendation[] = [
  { ...PRODUCTS[1], reason: "Bạn vừa mua serum BHA — C-vit là bước tiếp theo được chuyên gia khuyên." },
  { ...PRODUCTS[5], reason: "Da bạn da khô (signal từ quiz), Laneige mask lock ẩm 8h qua đêm." },
  { ...PRODUCTS[3], reason: "Son tint lì — match với 3 review gần đây của bạn đều khen 'lâu trôi, không khô'." },
  { ...PRODUCTS[2], reason: "Tote canvas phù hợp với style bạn lướt (canvas + earth-tone) trong 14 ngày qua." },
];