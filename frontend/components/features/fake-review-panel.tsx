"use client";

import { useState } from "react";
import { Loader2, ShieldAlert, ShieldCheck } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { detectFake, type FakeVerdict } from "@/lib/features";
import { cn } from "@/lib/utils";

const SAMPLES = [
  "Amazing! Love it! Best product ever! Highly recommend to everyone!",
  "Fits true to size, the linen is breathable and the stitching held up after three washes.",
  "Shop bán hàng uy tín, giao nhanh, đóng gói đẹp",
];

export function FakeReviewPanel() {
  const [text, setText] = useState(SAMPLES[0]);
  const [rating, setRating] = useState<number>(5);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<FakeVerdict | null>(null);
  const [error, setError] = useState(false);

  async function run() {
    if (!text.trim() || busy) return;
    setBusy(true);
    setError(false);
    const r = await detectFake(text, rating);
    setError(r === null);
    setResult(r ?? { is_fake: false, confidence: 0, signals: [], reason: "Backend unavailable." });
    setBusy(false);
  }

  const fake = result?.is_fake;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <Card className="lg:col-span-7">
        <CardHeader>
          <div>
            <CardTitle>Review to verify</CardTitle>
            <p className="mt-1 text-xs text-text-muted">
              Phát hiện review giả / seeding trước khi tin vào rating của sản phẩm.
            </p>
          </div>
          <Badge variant="muted">moderation</Badge>
        </CardHeader>
        <CardContent className="space-y-3">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={5}
            className="w-full resize-none rounded-md border border-border bg-bg-alt px-3 py-2 text-sm text-text outline-none focus:border-accent"
            placeholder="Nhập review cần kiểm tra…"
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
              {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <ShieldAlert className="h-3.5 w-3.5" />}
              Check
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
          <CardTitle>Verdict</CardTitle>
          {result && <Badge variant="muted">conf {Math.round(result.confidence * 100)}%</Badge>}
        </CardHeader>
        <CardContent>
          {error ? (
            <p className="text-sm text-danger">Không lấy được kết quả. Kiểm tra kết nối backend rồi thử lại.</p>
          ) : !result ? (
            <p className="text-sm text-text-muted">Bấm Check để kiểm tra review.</p>
          ) : (
            <div className="space-y-4">
              <div className={cn("flex items-center gap-2 text-2xl font-semibold tracking-tight",
                fake ? "text-danger" : "text-success")}>
                {fake ? <ShieldAlert className="h-6 w-6" /> : <ShieldCheck className="h-6 w-6" />}
                {fake ? "Likely FAKE" : "Likely genuine"}
              </div>
              <p className="text-sm text-text-muted">{result.reason}</p>
              <div>
                <div className="mono text-2xs uppercase tracking-wider text-text-dim">signals</div>
                <ul className="mt-2 space-y-1">
                  {result.signals.map((s, i) => (
                    <li key={i} className="flex items-start gap-2 text-xs text-text-muted">
                      <span className={cn("mt-1 h-1.5 w-1.5 shrink-0 rounded-full",
                        fake ? "bg-danger" : "bg-text-dim")} />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
