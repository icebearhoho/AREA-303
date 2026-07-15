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

/** Search URL on the product's marketplace (demo catalog has no canonical URLs). */
function productUrl(p: Product): string {
  const q = encodeURIComponent(p.name);
  if (p.platform === "Tiki") return `https://tiki.vn/search?q=${q}`;
  if (p.platform === "TikTok Shop") return `https://www.tiktok.com/search?q=${q}`;
  return `https://shopee.vn/search?keyword=${q}`;
}

/**
 * Category line-art icon — the demo catalog has no real product photos, so we
 * render a clean icon that always matches the item type (on-theme flat line-art)
 * instead of a random/mismatched stock photo.
 */
function productIcon(p: Product): LucideIcon {
  const n = `${p.name} ${p.category}`.toLowerCase();
  const has = (...ks: string[]) => ks.some((k) => n.includes(k));
  if (has("son", "lipstick", "môi", "phấn", "foundation", "cushion", "makeup", "má hồng")) return Palette;
  if (has("serum", "tinh chất", "kem", "cream", "dưỡng", "lotion", "toner", "vitamin")) return Droplet;
  if (has("mặt nạ", "mask")) return Sparkles;
  if (has("nước hoa", "perfume", "xịt")) return SprayCan;
  if (has("túi", "tote", "bag", "balo", "ví", "clutch")) return ShoppingBag;
  if (has("giày", "dép", "shoe", "sneaker", "sandal", "boot")) return Footprints;
  if (has("kính", "glasses", "sunglass")) return Glasses;
  if (has("đồng hồ", "watch")) return Watch;
  if (has("áo", "váy", "đầm", "quần", "dress", "shirt", "jean", "hoodie", "khoác", "thun")) return Shirt;
  if (p.category === "Mỹ phẩm") return Flower2;
  if (p.category === "Phụ kiện") return Package;
  return Shirt;
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
        <Icon
          className="h-1/3 w-1/3 transition-transform duration-300 group-hover:scale-110"
          strokeWidth={1.5}
          style={{ color: `hsl(${hue} 45% 38%)` }}
        />
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
