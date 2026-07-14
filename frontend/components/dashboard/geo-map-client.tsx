"use client";

import dynamic from "next/dynamic";
import type { PROVINCES } from "@/lib/mock-data";

/**
 * Client-only wrapper around <GeoMap> so that react-leaflet (which
 * touches `window` at module init) is never evaluated during SSR.
 */
const GeoMapClient = dynamic(
  () => import("@/components/dashboard/geo-map").then((m) => m.GeoMap),
  { ssr: false, loading: () => <GeoMapSkeleton /> },
);

function GeoMapSkeleton() {
  return (
    <div className="h-72 w-full animate-pulse rounded-lg border border-border bg-surface-2" />
  );
}

export type GeoMapClientProps = { nodes: typeof PROVINCES };

export { GeoMapClient as GeoMap };