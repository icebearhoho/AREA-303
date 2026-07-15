"use client";

import { useState } from "react";
import {
  Star, ExternalLink, Shirt, ShoppingBag, Footprints, Glasses, SprayCan,
  Droplet, Palette, Sparkles, Flower2, Watch, Package, type LucideIcon,
} from "lucide-react";
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

function productUrl(p: Product): string {
  const q = encodeURIComponent(p.name);
  if (p.platform === "Tiki") return `https://tiki.vn/search?q=${q}`;
  if (p.platform === "TikTok Shop") return `https://www.tiktok.com/search?q=${q}`;
  return `https://shopee.vn/search?keyword=${q}`;
}

/** One precise image tag per product so the photo matches the item type. */
function imageTag(p: Product): string {
  const n = `${p.name} ${p.category}`.toLowerCase();
  const has = (...ks: string[]) => ks.some((k) => n.includes(k));
  if (has("son", "lipstick", "môi")) return "lipstick";
  if (has("serum", "tinh chất", "vitamin")) return "serum";
  if (has("mặt nạ", "mask")) return "facemask";
  if (has("kem", "cream", "dưỡng", "lotion", "toner", "rửa mặt", "chống nắng", "cushion", "phấn")) return "skincare";
  if (has("nước hoa", "perfume")) return "perfume";
  if (has("túi", "tote", "bag", "balo", "ví")) return "handbag";
  if (has("giày", "dép", "shoe", "sneaker", "sandal")) return "sneakers";
  if (has("kính", "glasses", "sunglass")) return "sunglasses";
  if (has("đồng hồ", "watch")) return "watch";
  if (has("váy", "đầm", "dress")) return "dress";
  if (has("quần", "jean")) return "jeans";
  if (has("áo thun", "tee", "thun")) return "tshirt";
  if (has("áo", "khoác", "hoodie", "shirt")) return "shirt";
  if (p.category === "Mỹ phẩm") return "cosmetics";
  if (p.category === "Phụ kiện") return "accessory";
  return "clothing";
}

function imageUrl(p: Product): string {
  let lock = 1;
  for (const ch of String(p.id)) lock = (lock * 31 + ch.charCodeAt(0)) % 100000;
  return `https://loremflickr.com/600/600/${imageTag(p)}/all?lock=${lock}`;
}

/** Fallback icon if the photo fails to load. */
function productIcon(p: Product): LucideIcon {
  const t = imageTag(p);
  const map: Record<string, LucideIcon> = {
    lipstick: Palette, serum: Droplet, facemask: Sparkles, skincare: Droplet,
    perfume: SprayCan, handbag: ShoppingBag, sneakers: Footprints, sunglasses: Glasses,
    watch: Watch, dress: Shirt, jeans: Shirt, tshirt: Shirt, shirt: Shirt,
    cosmetics: Flower2, accessory: Package, clothing: Shirt,
  };
  return map[t] ?? Shirt;
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
  const Icon = productIcon(product);
  const hue = product.imageHue;

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
        className="group relative grid aspect-square w-full place-items-center overflow-hidden rounded-xl border border-border"
        style={{
          background: `linear-gradient(135deg, hsl(${hue} 62% 92%), hsl(${(hue + 32) % 360} 66% 84%))`,
        }}
        title={`Xem "${product.name}" trên ${product.platform}`}
      >
        {broken ? (
          <Icon className="h-1/3 w-1/3" strokeWidth={1.5} style={{ color: `hsl(${hue} 45% 38%)` }} />
        ) : (
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
