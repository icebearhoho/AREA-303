"use client";

import { useState } from "react";
import { Loader2, RotateCcw } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { scoreReturn, type ReturnResult } from "@/lib/features";
import { cn } from "@/lib/utils";

const CATEGORIES = ["Thời trang", "Mỹ phẩm", "Phụ kiện"] as const;

const BAND: Record<string, { label: string; cls: string }> = {
  low: { label: "Thấp", cls: "text-success" },
  medium: { label: "Trung bình", cls: "text-warning" },
  high: { label: "Cao", cls: "text-danger" },
};

export function ReturnPredictionPanel() {
  const [category, setCategory] = useState<(typeof CATEGORIES)[number]>("Thời trang");
  const [price, setPrice] = useState(800000);
  const [newCustomer, setNewCustomer] = useState(true);
  const [sizeRelated, setSizeRelated] = useState(true);
  const [discount, setDiscount] = useState(35);
  const [reviewsRead, setReviewsRead] = useState(0);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<ReturnResult | null>(null);

  async function run() {
    if (busy) return;
    setBusy(true);
    const r = await scoreReturn({
      category, priceVnd: price, isNewCustomer: newCustomer, sizeRelated,
      discountPct: discount, reviewsRead,
    });
    setResult(r);
    setBusy(false);
  }

  const band = result ? BAND[result.risk_band] : null;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <Card className="lg:col-span-7">
        <CardHeader>
          <div>
            <CardTitle>Thông tin đơn hàng</CardTitle>
            <p className="mt-1 text-xs text-text-muted">Ước tính nguy cơ hoàn trả trước khi giao hàng.</p>
          </div>
          <Badge variant="muted">order risk</Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="mono text-2xs uppercase tracking-wider text-text-dim">Danh mục</label>
            <div className="mt-1.5 inline-flex overflow-hidden rounded-md border border-border">
              {CATEGORIES.map((c) => (
                <button key={c} type="button" onClick={() => setCategory(c)}
                  className={cn("px-3 py-2 text-xs font-medium transition-colors",
                    category === c ? "bg-accent/15 text-accent" : "text-text-muted hover:text-text")}>
                  {c}
                </button>
              ))}
            </div>
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Giá trị đơn (₫)</label>
              <span className="mono text-xs text-text">{price.toLocaleString("vi-VN")}</span>
            </div>
            <input type="range" min={0} max={5_000_000} step={50_000} value={price}
              onChange={(e) => setPrice(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Giảm giá (%)</label>
              <span className="mono text-xs text-text">{discount}%</span>
            </div>
            <input type="range" min={0} max={100} value={discount}
              onChange={(e) => setDiscount(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Số review đã đọc trước khi mua</label>
              <span className="mono text-xs text-text">{reviewsRead}</span>
            </div>
            <input type="range" min={0} max={20} value={reviewsRead}
              onChange={(e) => setReviewsRead(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div className="flex flex-wrap gap-4">
            <label className="flex items-center gap-2 text-xs text-text-muted">
              <input type="checkbox" checked={newCustomer} onChange={(e) => setNewCustomer(e.target.checked)} />
              Khách hàng mới
            </label>
            <label className="flex items-center gap-2 text-xs text-text-muted">
              <input type="checkbox" checked={sizeRelated} onChange={(e) => setSizeRelated(e.target.checked)} />
              Sản phẩm liên quan size (áo/giày)
            </label>
          </div>
          <Button onClick={run} disabled={busy} className="w-full">
            {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <RotateCcw className="h-3.5 w-3.5" />}
            Dự đoán nguy cơ hoàn trả
          </Button>
        </CardContent>
      </Card>

      <Card className="lg:col-span-5">
        <CardHeader><CardTitle>Kết quả</CardTitle></CardHeader>
        <CardContent>
          {!result ? (
            <p className="text-sm text-text-muted">Bấm Dự đoán để xem nguy cơ hoàn trả.</p>
          ) : (
            <div className="space-y-4">
              <div className={cn("text-3xl font-semibold tracking-tight", band?.cls)}>
                {Math.round(result.return_risk * 100)}% — {band?.label}
              </div>
              <ul className="space-y-1">
                {result.drivers.map((d, i) => (
                  <li key={i} className="text-xs text-text-muted">• {d}</li>
                ))}
              </ul>
              <div className="rounded-md border border-border bg-bg-alt px-3 py-2 text-xs text-text">
                {result.action}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
