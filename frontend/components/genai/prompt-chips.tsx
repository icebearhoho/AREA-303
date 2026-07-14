"use client";

import { cn } from "@/lib/utils";

export function PromptChips({
  items,
  onSelect,
  className,
}: {
  items: string[];
  onSelect?: (value: string) => void;
  className?: string;
}) {
  return (
    <div className={cn("flex flex-wrap gap-2", className)}>
      {items.map((it) => (
        <button
          key={it}
          type="button"
          onClick={() => onSelect?.(it)}
          className="rounded-full border border-border bg-surface px-3 py-1 text-xs text-text-muted transition-colors hover:border-accent hover:text-text"
        >
          {it}
        </button>
      ))}
    </div>
  );
}