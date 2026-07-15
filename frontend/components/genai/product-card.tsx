"use client";

import { useState } from "react";
import { Star, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { Product } from "@/lib/mock-data";

const VND = new Intl.NumberFormat("vi-VN", {
  style: "currency",
  currency: "VND",
  maximumFractionDigits: 0,
});

const platformVariant: Record<Product["platform"], "info" | "success" | "warning"> = {
  Shopee: "warning",
  Tiki: "info",
  "TikTok Shop": "success",
};

/** Search URL on the product's marketplace (demo catalog has no canonical URLs). */
function productUrl(p: Product): string {
  const q = encodeURIComponent(p.name);
  if (p.platform === "Tiki") return `https://tiki.vn/search?q=${q}`;
  if (p.platform === "TikTok Shop") return `https://www.tiktok.com/search?q=${q}`;
  return `https://shopee.vn/search?keyword=${q}`;
}

/** Map a product to image keyword(s) so the photo actually matches the item. */
function keyword(p: Product): string {
  const n = `${p.name} ${p.category}`.toLowerCase();
  const has = (...ks: string[]) => ks.some((k) => n.includes(k));
  if (has("son", "lipstick", "môi")) return "lipstick,makeup";
  if (has("serum", "tinh chất", "vitamin c")) return "serum,skincare";
  if (has("mặt nạ", "mask")) return "facemask,skincare";
  if (has("kem", "cream", "dưỡng", "lotion")) return "skincare,cream";
  if (has("nước hoa", "perfume")) return "perfume,bottle";
  if (has("phấn", "foundation", "cushion", "makeup")) return "makeup,cosmetics";
  if (has("túi", "tote", "bag", "balo", "ví")) return "handbag,bag";
  if (has("áo thun", "tee", "t-shirt", "thun")) return "tshirt,apparel";
  if (has("áo", "shirt", "hoodie", "khoác", "jacket")) return "shirt,fashion";
  if (has("váy", "đầm", "dress")) return "dress,fashion";
  if (has("quần", "jean", "pants", "trouser")) return "jeans,fashion";
  if (has("giày", "dép", "shoe", "sneaker", "sandal")) return "shoes,footwear";
  if (has("kính", "glasses", "sunglass")) return "sunglasses";
  if (has("mũ", "nón", "hat", "cap")) return "hat,accessory";
  if (p.category === "Mỹ phẩm") return "cosmetics,beauty";
  if (p.category === "Phụ kiện") return "accessory,fashion";
  return "fashion,clothing";
}

/** Deterministic keyword-matched photo (stable per id). */
function imageUrl(p: Product): string {
  let lock = 0;
  for (const ch of String(p.id)) lock = (lock * 31 + ch.charCodeAt(0)) % 100000;
  return `https://loremflickr.com/600/600/${encodeURIComponent(keyword(p))}?lock=${lock}`;
}

export function ProductCard({
  product,
  similarity,
  className,
}: {
  product: Product;
  similarity?: number;
  className?: string;
}) {
  const href = productUrl(product);
  const [broken, setBroken] = useState(false);

  return (
    <div
      className={cn(
        "flex flex-col gap-2 rounded-2xl border border-border bg-surface p-3 transition-all hover:-translate-y-0.5 hover:shadow-soft",
        className,
      )}
    >
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="group relative block aspect-square w-full overflow-hidden rounded-xl border border-border"
        style={{
          background: `linear-gradient(135deg, hsl(${product.imageHue} 45% 82%), hsl(${(product.imageHue + 30) % 360} 50% 72%))`,
        }}
        title={`Xem "${product.name}" trên ${product.platform}`}
      >
        {!broken && (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={imageUrl(product)}
            alt={product.name}
            loading="lazy"
            onError={() => setBroken(true)}
            className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        )}
        <span className="absolute right-1.5 top-1.5 inline-flex items-center gap-1 rounded-full bg-bg/85 px-2 py-0.5 text-2xs font-semibold text-text">
          <ExternalLink className="h-3 w-3" />
          {product.platform}
        </span>
      </a>

      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="block truncate text-sm font-semibold text-text hover:text-accent"
            title={product.name}
          >
            {product.name}
          </a>
          <div className="truncate text-2xs uppercase tracking-wider text-text-dim">
            {product.brand}
          </div>
        </div>
        {typeof similarity === "number" && (
          <Badge variant="live">
            <span className="mono">{(similarity * 100).toFixed(0)}%</span>
          </Badge>
        )}
      </div>

      <div className="flex items-baseline gap-1.5">
        <span className="mono text-base font-semibold text-text" data-tnum>
          {VND.format(product.priceVnd).replace(/\s*₫/g, "")}
        </span>
        <span className="mono text-2xs text-text-dim">₫</span>
      </div>

      <div className="flex items-center justify-between text-2xs text-text-muted">
        <span className="inline-flex items-center gap-1">
          <Star className="h-3 w-3 fill-warning stroke-warning" />
          <span className="mono text-text">{product.rating.toFixed(1)}</span>
          <span className="mono text-text-dim">({product.reviews.toLocaleString()})</span>
        </span>
        <Badge variant={platformVariant[product.platform]}>{product.platform}</Badge>
      </div>
    </div>
  );
}
