"use client";

import { useState } from "react";
import { Loader2, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { analyzeSentiment, type Sentiment } from "@/lib/features";
import { cn } from "@/lib/utils";

const SAMPLES = [
  "Áo đẹp, vải mát, form chuẩn, giao hàng nhanh, rất hài lòng!",
  "Color is nice but it fades quickly, okay for the price.",
  "Poor quality, looks nothing like the photo, thin material. Disappointed.",
];

const TONE: Record<string, { label: string; cls: string }> = {
  positive: { label: "Positive", cls: "text-success" },
  neutral: { label: "Neutral", cls: "text-warning" },
  negative: { label: "Negative", cls: "text-danger" },
};

export function ReviewSentimentPanel() {
  const [text, setText] = useState(SAMPLES[0]);
  const [rating, setRating] = useState<number>(5);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Sentiment | null>(null);
  const [error, setError] = useState(false);

  async function run() {
    if (!text.trim() || busy) return;
    setBusy(true);
    setError(false);
    const r = await analyzeSentiment(text, rating);
    setError(r === null);
    setResult(r ?? { sentiment: "neutral", confidence: 0, reason: "Backend unavailable." });
    setBusy(false);
  }

  const tone = result ? TONE[result.sentiment] : null;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <Card className="lg:col-span-7">
        <CardHeader>
          <div>
            <CardTitle>Customer review</CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              Dán review của khách — hệ thống phân loại cảm xúc để bạn ưu tiên xử lý.
            </p>
          </div>
          <Badge variant="muted">VN + EN</Badge>
        </CardHeader>
        <CardContent className="space-y-3">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
            className="w-full resize-none rounded-md border border-border bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-accent"
            placeholder="Nhập nội dung review…"
          />
          <div className="flex flex-wrap items-center gap-3">
            <label className="mono text-2xs uppercase tracking-wider text-text-dim">rating</label>
            <div className="inline-flex overflow-hidden rounded-md border border-border">
              {[1, 2, 3, 4, 5].map((r) => (
                <button
                  key={r}
                  type="button"
                  onClick={() => setRating(r)}
                  className={cn(
                    "mono h-8 w-8 text-xs transition-colors",
                    rating === r ? "bg-accent/15 text-accent" : "text-text-muted hover:text-text",
                  )}
                >
                  {r}
                </button>
              ))}
            </div>
            <Button onClick={run} disabled={busy} className="ml-auto">
              {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Sparkles className="h-3.5 w-3.5" />}
              Analyze
            </Button>
          </div>
          <div className="flex flex-wrap gap-1.5 pt-1">
            {SAMPLES.map((s, i) => (
              <button
                key={i}
                type="button"
                onClick={() => setText(s)}
                className="rounded-full border border-border bg-surface px-2.5 py-1 text-2xs text-text-muted hover:border-accent hover:text-text"
              >
                sample {i + 1}
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="lg:col-span-5">
        <CardHeader>
          <CardTitle>Result</CardTitle>
          {result && <Badge variant="muted">conf {Math.round(result.confidence * 100)}%</Badge>}
        </CardHeader>
        <CardContent>
          {error ? (
            <p className="text-sm text-danger">Không lấy được kết quả. Kiểm tra kết nối backend rồi thử lại.</p>
          ) : !result ? (
            <p className="text-sm text-text-muted">Bấm Analyze để phân loại cảm xúc review.</p>
          ) : (
            <div className="space-y-4">
              <div className={cn("text-3xl font-semibold tracking-tight", tone?.cls)}>
                {tone?.label}
              </div>
              <div className="h-2 w-full overflow-hidden rounded-full bg-surface-2">
                <div
                  className="h-full rounded-full bg-accent transition-all"
                  style={{ width: `${Math.round(result.confidence * 100)}%` }}
                />
              </div>
              <p className="text-sm text-text-muted">{result.reason}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
