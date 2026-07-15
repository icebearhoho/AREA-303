import Link from "next/link";
import { DashboardShell } from "@/components/shell/dashboard-shell";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Sparkles, ArrowRight } from "lucide-react";
import { navForApp, IMPLEMENTED } from "@/lib/nav";

export const dynamic = "force-dynamic";

export default function ShopHome() {
  const items = navForApp("shop");

  return (
    <DashboardShell breadcrumb={[{ label: "Shop", href: "/shop" }, { label: "Home" }]}>
      <div className="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="mono text-2xs uppercase tracking-wider text-text-dim">Shop · discover</div>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-text">
            Mua sắm thông minh hơn với AI
          </h1>
          <p className="mt-1 text-sm text-text-muted">
            Trợ lý mua sắm, gợi ý cá nhân hoá và khám phá sản phẩm thời trang &amp; mỹ phẩm.
          </p>
        </div>
        <Button asChild size="sm" variant="primary">
          <Link href="/shop/personal-shopper"><Sparkles className="h-3.5 w-3.5" />Hỏi Personal Shopper</Link>
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {items.map((item) => {
          const Icon = item.icon;
          const live = IMPLEMENTED.has(item.slug);
          return (
            <Link
              key={item.slug}
              href={item.href}
              className="group flex flex-col rounded-xl border border-border bg-surface p-5 transition-colors hover:border-accent"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-accent/15">
                  <Icon className="h-4 w-4 text-accent" />
                </div>
                <span className="font-medium text-text">{item.label}</span>
                {live ? (
                  <Badge variant="live" className="ml-auto"><span className="live-dot" />live</Badge>
                ) : (
                  <Badge variant="muted" className="ml-auto">soon</Badge>
                )}
              </div>
              <div className="mt-4 flex items-center text-xs text-text-muted">
                <span className="mono text-2xs uppercase tracking-wider text-text-dim">{item.category}</span>
                <ArrowRight className="ml-auto h-4 w-4 text-text-dim transition-transform group-hover:translate-x-0.5 group-hover:text-accent" />
              </div>
            </Link>
          );
        })}
      </div>
    </DashboardShell>
  );
}
