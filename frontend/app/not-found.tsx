import Link from "next/link";
import { DashboardShell } from "@/components/shell/dashboard-shell";

export const dynamic = "force-dynamic";

import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <DashboardShell breadcrumb={[{ label: "Not found" }]}>
      <div className="flex flex-col items-start gap-4">
        <div className="mono text-2xs uppercase tracking-wider text-text-dim">
          404 — no route
        </div>
        <h1 className="text-2xl font-semibold tracking-tight text-text">
          This page does not exist
        </h1>
        <p className="text-sm text-text-muted">
          Route này không thuộc 17 AI features của AREA-303.
        </p>
        <Button asChild variant="secondary">
          <Link href="/">Back to overview</Link>
        </Button>
      </div>
    </DashboardShell>
  );
}