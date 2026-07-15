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

/** Deterministic product photo (stable per id). */
function imageUrl(p: Product): string {
  return `https://picsum.photos/seed/area303-${encodeURIComponent(p.id)}/400/400`;
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
  return (
    <div
      className={cn(
        "flex flex-col gap-2 rounded-[10px] border border-border bg-surface p-3 transition-colors hover:border-border-strong",
        className,
      )}
    >
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="group relative block aspect-square w-full overflow-hidden rounded-md border border-border"
        style={{
          background: `linear-gradient(135deg, hsl(${product.imageHue} 35% 22%), hsl(${(product.imageHue + 30) % 360} 45% 14%))`,
        }}
        title={`Xem "${product.name}" trên ${product.platform}`}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={imageUrl(product)}
          alt={product.name}
          loading="lazy"
          className="absolute inset-0 h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
        />
        <span className="absolute right-1.5 top-1.5 inline-flex items-center gap-1 rounded bg-bg/75 px-1.5 py-0.5 text-2xs text-text">
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
            className="block truncate text-sm font-medium text-text hover:text-accent"
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
        <span className="mono text-base font-medium text-text" data-tnum>
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
