"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ProductCard } from "@/components/genai/product-card";
import { cn } from "@/lib/utils";
import {
  RECSYS_TRADITIONAL,
  RECSYS_AI,
  type Recommendation,
} from "@/lib/mock-data";
import { recsysRecommend } from "@/lib/features";

type Mode = "traditional" | "ai";

const SIGNAL_CHIPS = [
  { label: "skin_type", value: "dry" },
  { label: "skin_tone", value: "light" },
  { label: "bought_30d", value: "BHA serum" },
  { label: "browse_14d", value: "earth-tone canvas" },
  { label: "review_sentiment", value: "+0.71" },
];

export function RecsysPanel() {
  const [mode, setMode] = useState<Mode>("ai");
  const [aiItems, setAiItems] = useState<Recommendation[]>(RECSYS_AI);

  useEffect(() => {
    const signals = Object.fromEntries(SIGNAL_CHIPS.map((s) => [s.label, s.value]));
    recsysRecommend(signals, 8, RECSYS_AI)
      .then((r) => setAiItems(r.items))
      .catch(() => {});
  }, []);

  const items: Recommendation[] = mode === "ai" ? aiItems : RECSYS_TRADITIONAL;

  return (
    <div className="space-y-4">
      {/* Mode switcher */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="inline-flex h-9 items-center rounded-md border border-border bg-surface p-0.5">
          <button
            type="button"
            onClick={() => setMode("traditional")}
            className={cn(
              "mono h-8 rounded-[6px] px-3 text-2xs uppercase tracking-wider transition-colors",
              mode === "traditional"
                ? "bg-surface-3 text-text"
                : "text-text-muted hover:text-text",
            )}
          >
            Traditional CF
          </button>
          <button
            type="button"
            onClick={() => setMode("ai")}
            className={cn(
              "mono h-8 rounded-[6px] px-3 text-2xs uppercase tracking-wider transition-colors",
              mode === "ai"
                ? "bg-accent/15 text-accent"
                : "text-text-muted hover:text-text",
            )}
          >
            AI reasoning
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-1.5">
          <span className="mono text-2xs uppercase tracking-wider text-text-dim">
            Signals
          </span>
          {SIGNAL_CHIPS.map((s) => (
            <Badge key={s.label} variant="muted">
              <span className="mono normal-case tracking-normal">
                {s.label}: <span className="text-text">{s.value}</span>
              </span>
            </Badge>
          ))}
        </div>
      </div>

      {/* Model description */}
      <Card>
        <CardHeader>
          <div>
            <CardTitle>
              {mode === "ai" ? "LightFM + LLM reasoning" : "Collaborative filtering"}
            </CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              {mode === "ai"
                ? "Hybrid CF + content features, kết hợp LLM giải thích 'vì sao' recommendation này phù hợp."
                : "Item-item cosine trên user-item matrix. Không giải thích được lý do cụ thể."}
            </p>
          </div>
          <Badge variant={mode === "ai" ? "live" : "muted"}>
            {mode === "ai" ? "BERT4Rec + Gemini" : "matrix factorization"}
          </Badge>
        </CardHeader>
      </Card>

      {/* Product grid */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {items.map((p, i) => (
          <div key={p.id} className="space-y-2">
            <ProductCard product={p} similarity={p.similarity ?? 0.5 + i * 0.05} />
            <div className="rounded-md border border-border bg-surface px-3 py-2 text-xs text-text-muted">
              <span className="mono text-2xs uppercase tracking-wider text-text-dim">
                {mode === "ai" ? "Why" : "Signal"}
              </span>
              <p className="mt-1 leading-relaxed">{p.reason}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Metric label="Recall@10" value="0.184" delta="+12%" />
        <Metric label="NDCG@10" value="0.221" delta="+8%" />
        <Metric label="Hit rate" value="0.612" delta="+5%" />
        <Metric label="Coverage" value="0.84" delta="+3%" inverted />
      </div>
    </div>
  );
}

function Metric({
  label,
  value,
  delta,
  inverted,
}: {
  label: string;
  value: string;
  delta: string;
  inverted?: boolean;
}) {
  const positive = delta.startsWith("+");
  const good = inverted ? !positive : positive;
  return (
    <Card>
      <CardContent className="space-y-1 py-4">
        <div className="mono text-2xs uppercase tracking-wider text-text-dim">
          {label}
        </div>
        <div className="mono text-xl font-medium text-text" data-tnum>
          {value}
        </div>
        <div
          className={cn(
            "mono text-2xs",
            good ? "text-success" : "text-danger",
          )}
        >
          {delta} vs baseline
        </div>
      </CardContent>
    </Card>
  );
}