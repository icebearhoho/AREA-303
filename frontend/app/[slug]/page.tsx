import { DashboardShell } from "@/components/shell/dashboard-shell";

export const dynamic = "force-dynamic";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { findBySlug, NAV_ITEMS } from "@/lib/nav";

const OWNER_LABEL: Record<string, string> = {
  TL: "Team Lead",
  DA: "Data / ML",
  FS: "Fullstack",
  D1: "Developer 1",
  D2: "Developer 2",
};

export default async function FeaturePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const item = findBySlug(slug);

  if (!item) {
    return (
      <DashboardShell breadcrumb={[{ label: "404" }]}>
        <Card>
          <CardHeader>
            <CardTitle>Not found</CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              No feature matches this route.
            </p>
          </CardHeader>
        </Card>
      </DashboardShell>
    );
  }

  return (
    <DashboardShell
      breadcrumb={[{ label: "Overview", href: "/" }, { label: item.label }]}
    >
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <div className="mono flex items-center gap-2 text-2xs uppercase tracking-wider text-text-dim">
            <span>#{item.id}</span>
            <span>·</span>
            <span>{item.category}</span>
            <span>·</span>
            <span>owner {OWNER_LABEL[item.owner] ?? item.owner}</span>
          </div>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight text-text">
            {item.label}
          </h1>
          <p className="mt-1 flex items-center gap-2 text-sm text-text-muted">
            <span className="mono text-xs text-text-dim">/{item.slug}</span>
            <Badge variant="muted">placeholder</Badge>
          </p>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div>
            <CardTitle>Coming soon</CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              Feature này thuộc phần việc của{" "}
              <span className="text-text">{OWNER_LABEL[item.owner]}</span>. Sẽ được
              wire vào shell khi owner merge.
            </p>
          </div>
          <Badge variant="muted">{item.section}</Badge>
        </CardHeader>
        <CardContent>
          <pre className="mono overflow-x-auto rounded-md border border-border bg-bg-alt p-4 text-xs text-text-muted">
{`route:   ${item.href}
slug:    ${item.slug}
id:      #${item.id}
owner:   ${item.owner} (${OWNER_LABEL[item.owner]})
category: ${item.category}
section: ${item.section}`}
          </pre>

          <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {NAV_ITEMS.filter((i) => i.owner === "FS").slice(0, 4).map((i) => (
              <a
                key={i.slug}
                href={i.href}
                className="rounded-md border border-border bg-surface px-3 py-2 text-xs text-text-muted transition-colors hover:border-accent hover:text-text"
              >
                <span className="mono text-2xs uppercase tracking-wider text-text-dim">
                  #{i.id}
                </span>
                <div className="mt-1 text-sm text-text">{i.label}</div>
              </a>
            ))}
          </div>
        </CardContent>
      </Card>
    </DashboardShell>
  );
}