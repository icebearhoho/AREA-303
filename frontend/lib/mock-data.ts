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
  description: string;
};

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
    description:
      "Cotton 220gsm dày dặn, form oversize, in lụa không bong. 5 màu.",
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