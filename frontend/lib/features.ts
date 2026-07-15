/**
 * Feature API layer — connects the GenAI panels to the FastAPI backend
 * (endpoints under /api/v1). Every call maps the backend snake_case shapes to
 * the frontend camelCase types and falls back to the supplied mock data when the
 * backend is unreachable or NEXT_PUBLIC_DEMO_MODE=true — so the UI never breaks.
 */
import { api } from "@/lib/api";
import type {
  Product,
  Recommendation,
  ContentVariant,
  AuditStep,
  RoadmapWeek,
} from "@/lib/mock-data";

const DEMO = process.env.NEXT_PUBLIC_DEMO_MODE === "true";

// --- backend wire shapes -------------------------------------------------
type BackendProduct = {
  id: string; name: string; brand: string; category: string; platform: string;
  price_vnd: number; rating: number; reviews: number; similarity: number; image_hue?: number;
};
type BackendRec = Omit<BackendProduct, "id" | "image_hue"> & { product_id: string; reason: string };
type BackendVariant = {
  platform: string; title: string; body: string; predicted_ctr: number; rationale: string;
};

function mapProduct(p: BackendProduct): Product {
  return {
    id: p.id, name: p.name, brand: p.brand,
    category: p.category as Product["category"],
    platform: p.platform as Product["platform"],
    priceVnd: p.price_vnd, rating: p.rating, reviews: p.reviews,
    similarity: p.similarity, imageHue: p.image_hue ?? 215, description: "",
  };
}

async function post<T>(path: string, body: unknown): Promise<T | null> {
  if (DEMO) return null;
  try {
    const env = await api.post<T>(path, body);
    return env.data as T;
  } catch {
    return null;
  }
}

async function get<T>(path: string): Promise<T | null> {
  if (DEMO) return null;
  try {
    const env = await api.get<T>(path);
    return env.data as T;
  } catch {
    return null;
  }
}

// --- #03 Personal Shopper -------------------------------------------------
export async function shopperProducts(
  query: string, topK: number, fallback: Product[],
): Promise<{ products: Product[]; live: boolean }> {
  const data = await get<{ products: BackendProduct[] }>(
    `/personal-shopper/products?query=${encodeURIComponent(query)}&top_k=${topK}`,
  );
  if (!data?.products?.length) return { products: fallback, live: false };
  return { products: data.products.map(mapProduct), live: true };
}

// --- #11 Recsys -----------------------------------------------------------
export async function recsysRecommend(
  signals: Record<string, string>, topK: number, fallback: Recommendation[],
): Promise<{ items: Recommendation[]; live: boolean; model?: string }> {
  const data = await post<{ items: BackendRec[]; model: string }>(
    "/recsys/", { signals, top_k: topK },
  );
  if (!data?.items?.length) return { items: fallback, live: false };
  const items = data.items.map((r) => ({
    ...mapProduct({ ...r, id: r.product_id }), reason: r.reason,
  }));
  return { items, live: true, model: data.model };
}

// --- #09 Content Generator ------------------------------------------------
export async function contentGenerate(
  productName: string, features: string, platforms: string[], fallback: ContentVariant[],
): Promise<{ variants: ContentVariant[]; live: boolean }> {
  const data = await post<{ variants: BackendVariant[] }>(
    "/content-generator/", { product_name: productName, features, platforms },
  );
  if (!data?.variants?.length) return { variants: fallback, live: false };
  const variants = data.variants.map((v) => ({
    platform: v.platform as ContentVariant["platform"],
    title: v.title, body: v.body, predictedCtr: v.predicted_ctr, rationale: v.rationale,
  }));
  return { variants, live: true };
}

// --- #01 Review Sentiment -------------------------------------------------
export type Sentiment = { sentiment: "positive" | "neutral" | "negative"; confidence: number; reason: string };

export async function analyzeSentiment(text: string, rating?: number): Promise<Sentiment | null> {
  return post<Sentiment>("/review-sentiment/", { text, rating: rating ?? null });
}

// --- #05 Fake Review ------------------------------------------------------
export type FakeVerdict = { is_fake: boolean; confidence: number; signals: string[]; reason: string };

export async function detectFake(text: string, rating?: number, category?: string): Promise<FakeVerdict | null> {
  return post<FakeVerdict>("/fake-review/", { text, rating: rating ?? null, category: category ?? null });
}

// --- #17 Seller Coach -----------------------------------------------------
export async function sellerCoach(
  fallback: { overall: number; audit: AuditStep[]; roadmap: RoadmapWeek[] },
): Promise<{ overall: number; audit: AuditStep[]; roadmap: RoadmapWeek[]; live: boolean }> {
  const data = await post<{ overall: number; audit: AuditStep[]; roadmap: RoadmapWeek[] }>(
    "/seller-coach/", {},
  );
  if (!data?.audit?.length) return { ...fallback, live: false };
  return { overall: data.overall, audit: data.audit, roadmap: data.roadmap, live: true };
}
