"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, Menu, X } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { NAV_ITEMS, NAV_SECTIONS } from "@/lib/nav";

export function Sidebar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  useEffect(() => setOpen(false), [pathname]);

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={() => setOpen((v) => !v)}
        className="fixed left-4 top-3 z-50 inline-flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-surface text-text lg:hidden"
        aria-label="Toggle navigation"
      >
        {open ? <X className="h-4 w-4" /> : <Menu className="h-4 w-4" />}
      </button>

      {/* Overlay on mobile */}
      {open && (
        <div
          className="fixed inset-0 z-40 bg-black/60 lg:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 flex w-60 flex-col border-r border-border bg-bg-alt transition-transform lg:translate-x-0",
          open ? "translate-x-0" : "-translate-x-full",
        )}
      >
        {/* Brand */}
        <div className="flex h-14 items-center gap-2 border-b border-border px-4">
          <div className="flex h-6 w-6 items-center justify-center rounded-md bg-accent/15">
            <Activity className="h-3.5 w-3.5 text-accent" />
          </div>
          <span className="mono text-sm font-semibold tracking-wider">AREA-303</span>
          <span className="ml-auto mono text-2xs text-text-dim">v0.1</span>
        </div>

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto p-2">
          {NAV_SECTIONS.map((section) => {
            const items = NAV_ITEMS.filter((i) => i.section === section.id);
            return (
              <div key={section.id} className="mb-4">
                <div className="px-3 pb-1.5 pt-2 text-2xs uppercase tracking-wider text-text-dim">
                  {section.title}
                </div>
                <ul className="space-y-0.5">
                  {items.map((item) => {
                    const Icon = item.icon;
                    const active = isActive(item.href);
                    return (
                      <li key={item.slug}>
                        <Link
                          href={item.href}
                          className={cn(
                            "group relative flex h-9 items-center gap-2.5 rounded-md px-3 text-sm transition-colors",
                            active
                              ? "bg-surface-3 text-text"
                              : "text-text-muted hover:bg-surface-2 hover:text-text",
                          )}
                        >
                          {active && (
                            <span className="absolute left-0 top-1/2 h-5 w-0.5 -translate-y-1/2 rounded-r bg-accent" />
                          )}
                          <Icon className="h-4 w-4 shrink-0" />
                          <span className="truncate">{item.label}</span>
                          <span className="mono ml-auto text-2xs text-text-dim tracking-wider">
                            #{item.id}
                          </span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            );
          })}
        </nav>

        {/* Footer status */}
        <div className="border-t border-border p-3">
          <div className="flex items-center gap-2 rounded-md bg-surface px-3 py-2">
            <span className="live-dot" />
            <span className="text-xs text-text-muted">17/17 features online</span>
            <span className="mono ml-auto text-2xs text-text-dim">v0.1</span>
          </div>
        </div>
      </aside>
    </>
  );
}