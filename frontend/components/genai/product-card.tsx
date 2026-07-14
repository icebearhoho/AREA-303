import { Star } from "lucide-react";
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

/**
 * Deterministic swatch derived from `imageHue`.
 * Stands in for product imagery when the real image is not yet fetched.
 */
function ProductSwatch({ hue }: { hue: number }) {
  return (
    <div
      className="relative aspect-square w-full overflow-hidden rounded-md border border-border"
      style={{
        background: `linear-gradient(135deg, hsl(${hue} 35% 22%), hsl(${(hue + 30) % 360} 45% 14%))`,
      }}
    >
      <div
        className="absolute inset-0 opacity-60"
        style={{
          backgroundImage: `radial-gradient(circle at 30% 30%, hsl(${hue} 70% 60% / 0.35), transparent 55%)`,
        }}
      />
      <div className="mono absolute bottom-1.5 left-1.5 rounded bg-bg/70 px-1.5 py-0.5 text-2xs text-text-dim">
        img
      </div>
    </div>
  );
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
  return (
    <div
      className={cn(
        "flex flex-col gap-2 rounded-[10px] border border-border bg-surface p-3 transition-colors hover:border-border-strong",
        className,
      )}
    >
      <ProductSwatch hue={product.imageHue} />

      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="truncate text-sm font-medium text-text" title={product.name}>
            {product.name}
          </div>
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
        <Badge variant={platformVariant[product.platform]}>
          {product.platform}
        </Badge>
      </div>
    </div>
  );
}