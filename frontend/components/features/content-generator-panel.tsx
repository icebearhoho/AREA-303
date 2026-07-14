"use client";

import { useState } from "react";
import { Copy, Check, RefreshCw, Wand2 } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { CONTENT_DEMO, type ContentVariant } from "@/lib/mock-data";

const PLATFORMS = ["Shopee", "Tiki", "TikTok Shop"] as const;
type Platform = (typeof PLATFORMS)[number];

const PLATFORM_VARIANT: Record<Platform, "warning" | "info" | "success"> = {
  Shopee: "warning",
  Tiki: "info",
  "TikTok Shop": "success",
};

function CtrBar({ value }: { value: number }) {
  const pct = Math.round(value * 1000) / 10;
  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between text-2xs">
        <span className="mono uppercase tracking-wider text-text-dim">
          predicted CTR
        </span>
        <span className="mono text-text" data-tnum>
          {pct.toFixed(1)}‰
        </span>
      </div>
      <div className="h-1.5 w-full overflow-hidden rounded-full bg-surface-2">
        <div
          className="h-full rounded-full bg-accent transition-all"
          style={{ width: `${Math.min(100, pct * 8)}%` }}
        />
      </div>
    </div>
  );
}

export function ContentGeneratorPanel() {
  const [productName, setProductName] = useState("Áo khoác denim unisex form rộng");
  const [features, setFeatures] = useState("Denim 12oz, wash nhẹ, 2 size, unisex, free ship");
  const [activePlatform, setActivePlatform] = useState<Platform>("Shopee");
  const [copied, setCopied] = useState(false);
  const [generating, setGenerating] = useState(false);

  function copy(text: string) {
    if (typeof navigator !== "undefined" && navigator.clipboard) {
      navigator.clipboard.writeText(text).catch(() => {});
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  }

  function generate() {
    setGenerating(true);
    window.setTimeout(() => setGenerating(false), 900);
  }

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      {/* Left: input form */}
      <Card className="lg:col-span-4">
        <CardHeader>
          <div>
            <CardTitle>Product input</CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              Prompt + RAG context từ wikipedia_vi + tiki catalog.
            </p>
          </div>
          <Badge variant="muted">few-shot</Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          <Field label="Tên sản phẩm">
            <Input
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              placeholder="Áo khoác denim unisex form rộng"
            />
          </Field>
          <Field label="Đặc điểm nổi bật">
            <textarea
              value={features}
              onChange={(e) => setFeatures(e.target.value)}
              rows={4}
              className="flex w-full rounded-lg border border-border-strong bg-bg-alt px-3 py-2 text-sm text-text placeholder:text-text-dim focus-visible:border-accent focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
              placeholder="Mỗi dòng 1 đặc điểm"
            />
          </Field>

          <Field label="Platform">
            <div className="grid grid-cols-3 gap-2">
              {PLATFORMS.map((p) => (
                <button
                  key={p}
                  type="button"
                  onClick={() => setActivePlatform(p)}
                  className={cn(
                    "flex h-9 items-center justify-center rounded-md border text-xs transition-colors",
                    activePlatform === p
                      ? "border-accent bg-accent/10 text-accent"
                      : "border-border bg-surface text-text-muted hover:border-border-strong hover:text-text",
                  )}
                >
                  {p}
                </button>
              ))}
            </div>
          </Field>

          <div className="rounded-md border border-border bg-bg-alt p-3 text-2xs text-text-muted">
            <div className="mono mb-1 uppercase tracking-wider text-text-dim">
              Prompt template
            </div>
            <code className="mono block whitespace-pre-wrap text-text">
              {`Bạn là copywriter cho ${activePlatform}. Viết mô tả sản phẩm bằng tiếng Việt:\n- Sản phẩm: ${productName || "—"}\n- Đặc điểm: ${features || "—"}`}
            </code>
          </div>

          <Button onClick={generate} disabled={generating} className="w-full">
            {generating ? (
              <>
                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                Generating…
              </>
            ) : (
              <>
                <Wand2 className="h-3.5 w-3.5" />
                Generate 3 phiên bản
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Right: 3 platform variants side-by-side */}
      <div className="lg:col-span-8 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <div className="mono text-2xs uppercase tracking-wider text-text-dim">
              Outputs
            </div>
            <div className="text-sm text-text-muted">
              3 platform · predicted CTR từ historical data
            </div>
          </div>
          <Badge variant="live">
            <span className="live-dot" />
            Gemini 1.5 Pro
          </Badge>
        </div>

        <div className="grid grid-cols-1 gap-3 xl:grid-cols-3">
          {CONTENT_DEMO.map((v) => (
            <ContentCard
              key={v.platform}
              variant={v}
              highlighted={v.platform === activePlatform}
              onCopy={() => copy(`${v.title}\n\n${v.body}`)}
              copied={copied && v.platform === activePlatform}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

function Field({
  label,
  children,
}: {
  label: string;
  children: React.ReactNode;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="mono text-2xs uppercase tracking-wider text-text-dim">
        {label}
      </span>
      {children}
    </label>
  );
}

function ContentCard({
  variant,
  highlighted,
  onCopy,
  copied,
}: {
  variant: ContentVariant;
  highlighted: boolean;
  onCopy: () => void;
  copied: boolean;
}) {
  return (
    <Card
      className={cn(
        "transition-colors",
        highlighted ? "border-accent" : "",
      )}
    >
      <CardHeader>
        <div>
          <Badge variant={PLATFORM_VARIANT[variant.platform]}>
            {variant.platform}
          </Badge>
          <CardTitle className="mt-2 text-sm leading-snug">
            {variant.title}
          </CardTitle>
        </div>
        <Button size="icon" variant="ghost" onClick={onCopy} aria-label="Copy">
          {copied ? (
            <Check className="h-3.5 w-3.5 text-success" />
          ) : (
            <Copy className="h-3.5 w-3.5" />
          )}
        </Button>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-sm leading-relaxed text-text">{variant.body}</p>

        <CtrBar value={variant.predictedCtr} />

        <div className="rounded-md border border-border bg-bg-alt p-2.5 text-2xs text-text-muted">
          <span className="mono uppercase tracking-wider text-text-dim">
            Rationale
          </span>
          <p className="mt-1">{variant.rationale}</p>
        </div>
      </CardContent>
    </Card>
  );
}