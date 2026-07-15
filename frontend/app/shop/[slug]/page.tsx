import { DashboardShell } from "@/components/shell/dashboard-shell";
import { FeatureHeader } from "@/components/genai/feature-header";
import { FeaturePanel } from "@/components/features/feature-registry";
import { ComingSoon } from "@/components/shell/coming-soon";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { findBySlug, IMPLEMENTED, SUBTITLE } from "@/lib/nav";

export const dynamic = "force-dynamic";

export default async function ShopFeaturePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const item = findBySlug(slug);

  if (!item || item.app !== "shop") {
    return (
      <DashboardShell breadcrumb={[{ label: "Shop", href: "/shop" }, { label: "Not found" }]}>
        <Card>
          <CardHeader>
            <CardTitle>Not found</CardTitle>
            <p className="mt-1 text-xs text-text-muted">No Shop feature matches this route.</p>
          </CardHeader>
        </Card>
      </DashboardShell>
    );
  }

  return (
    <DashboardShell breadcrumb={[{ label: "Shop", href: "/shop" }, { label: item.label }]}>
      <FeatureHeader
        id={item.id}
        title={item.label}
        subtitle={SUBTITLE[slug] ?? "Feature thuộc app Shop."}
        category={item.category}
        owner={item.owner}
      />
      {IMPLEMENTED.has(slug) ? <FeaturePanel slug={slug} /> : <ComingSoon item={item} />}
    </DashboardShell>
  );
}
