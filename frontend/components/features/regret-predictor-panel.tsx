"use client";

import { useState } from "react";
import { Loader2, BadgePercent } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { scoreRegret, type RegretResult } from "@/lib/features";
import { cn } from "@/lib/utils";

const BAND: Record<string, { label: string; cls: string }> = {
  low: { label: "Thấp", cls: "text-success" },
  medium: { label: "Trung bình", cls: "text-warning" },
  high: { label: "Cao", cls: "text-danger" },
};

export function RegretPredictorPanel() {
  const [decisionTime, setDecisionTime] = useState(30);
  const [revisits, setRevisits] = useState(0);
  const [hour, setHour] = useState(1);
  const [price, setPrice] = useState(1500000);
  const [usedDiscount, setUsedDiscount] = useState(true);
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<RegretResult | null>(null);
  const [error, setError] = useState(false);

  async function run() {
    if (busy) return;
    setBusy(true);
    setError(false);
    const r = await scoreRegret({
      decisionTimeSeconds: decisionTime, revisitCount: revisits, purchaseHour: hour,
      priceVnd: price, usedDiscount,
    });
    setError(r === null);
    setResult(r);
    setBusy(false);
  }

  const band = result ? BAND[result.risk_band] : null;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <Card className="lg:col-span-7">
        <CardHeader>
          <div>
            <CardTitle>Hành vi trước khi mua</CardTitle>
            <p className="mt-1 text-xs text-text-muted">Mô phỏng một giao dịch để dự đoán khả năng khách hối hận sau mua.</p>
          </div>
          <Badge variant="muted">post-purchase</Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Thời gian quyết định (giây)</label>
              <span className="mono text-xs text-text">{decisionTime}s</span>
            </div>
            <input type="range" min={0} max={600} value={decisionTime}
              onChange={(e) => setDecisionTime(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Số lần xem lại trước khi mua</label>
              <span className="mono text-xs text-text">{revisits}</span>
            </div>
            <input type="range" min={0} max={10} value={revisits}
              onChange={(e) => setRevisits(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Giờ mua (0-23h)</label>
              <span className="mono text-xs text-text">{hour}:00</span>
            </div>
            <input type="range" min={0} max={23} value={hour}
              onChange={(e) => setHour(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <div>
            <div className="flex items-center justify-between">
              <label className="mono text-2xs uppercase tracking-wider text-text-dim">Giá trị đơn (₫)</label>
              <span className="mono text-xs text-text">{price.toLocaleString("vi-VN")}</span>
            </div>
            <input type="range" min={0} max={5_000_000} step={50_000} value={price}
              onChange={(e) => setPrice(Number(e.target.value))} className="mt-1.5 w-full accent-accent" />
          </div>
          <label className="flex items-center gap-2 text-xs text-text-muted">
            <input type="checkbox" checked={usedDiscount} onChange={(e) => setUsedDiscount(e.target.checked)} />
            Mua chủ yếu vì có giảm giá
          </label>
          <Button onClick={run} disabled={busy} className="w-full">
            {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <BadgePercent className="h-3.5 w-3.5" />}
            Dự đoán khả năng hối hận
          </Button>
        </CardContent>
      </Card>

      <Card className="lg:col-span-5">
        <CardHeader><CardTitle>Kết quả</CardTitle></CardHeader>
        <CardContent>
          {error ? (
            <p className="text-sm text-danger">Không lấy được kết quả. Kiểm tra kết nối backend rồi thử lại.</p>
          ) : !result ? (
            <p className="text-sm text-text-muted">Bấm Dự đoán để xem kết quả.</p>
          ) : (
            <div className="space-y-4">
              <div className={cn("text-3xl font-semibold tracking-tight", band?.cls)}>
                {Math.round(result.regret_risk * 100)}% — {band?.label}
              </div>
              <ul className="space-y-1">
                {result.drivers.map((d, i) => (
                  <li key={i} className="text-xs text-text-muted">• {d}</li>
                ))}
              </ul>
              <div className="rounded-md border border-border bg-bg-alt px-3 py-2 text-xs text-text">
                <div className="mono mb-1 text-2xs uppercase tracking-wider text-text-dim">Tin nhắn tự động gửi khách</div>
                {result.reassurance_message}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
