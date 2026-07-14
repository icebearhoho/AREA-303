import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import type { ReactNode } from "react";

export function FeatureHeader({
  id,
  title,
  subtitle,
  category,
  owner,
  demoMode = true,
  action,
}: {
  id: string;
  title: string;
  subtitle: string;
  category: string;
  owner: "TL" | "DA" | "FS" | "D1" | "D2";
  demoMode?: boolean;
  action?: ReactNode;
}) {
  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <div className="mono flex items-center gap-2 text-2xs uppercase tracking-wider text-text-dim">
          <span>#{id}</span>
          <span>·</span>
          <span>{category}</span>
          <span>·</span>
          <span>owner {owner}</span>
        </div>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight text-text">
          {title}
        </h1>
        <p className="mt-1 max-w-2xl text-sm text-text-muted">{subtitle}</p>
      </div>

      <div className="flex flex-col items-end gap-2">
        <div className="flex items-center gap-2">
          {demoMode && (
            <Badge variant="warning">demo mode</Badge>
          )}
          <Badge variant="muted">v0.1</Badge>
        </div>
        {action ?? (
          <Button asChild variant="ghost" size="sm">
            <Link href="/">← Overview</Link>
          </Button>
        )}
      </div>
    </div>
  );
}