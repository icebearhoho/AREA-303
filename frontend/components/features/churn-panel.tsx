"use client";

import { useState } from "react";
import { Loader2, UserMinus } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { scoreChurn, type ChurnResult } from "@/lib/features";
import { cn } from "@/lib/utils";

const TRENDS = [
  { value: "declining", label: "Giảm dần" },
  { value: "stable", label: "Ổn định" },
  { value: "growing", label: "Tăng dần" },
] as const;

const BAND: Record<string, { label: string; cls: string }> = {
  low: { label: "Thấp", cls: "text-success" },
  medium: { label: "Trung bình", cls: "text-warning" },
  high: { label: "Cao", cls: "text-danger" },
};

function NumberField({ label, value, onChange, max }: { label: string; value: number; onChange: (v: number) => void; max: number }) {
  return (
    <div>
      <div className="flex items-center justify-between">
        <label className="mono text-2xs uppercase tracking-wider text-text-dim">{label}</label>
        <span className="mono text-xs text-text">{value}</span>
      </div>
      <input
        type="range"
        min={0}
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="mt-1.5 w-full accent-accent"
      />
    </div>
  );
}

export function ChurnPanel() {
  const [recency, setRecency] = useState(45);
  const [frequency, setFrequency] = useState(3);
  const [sessions, setSessions] = useState(2);
  const [abandon, setAbandon] = useState(30);
  const [trend, setTrend] = useState<(typeof TRENDS)[number]["value"]>("stable");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<ChurnResult | null>(null);
  const [error, setError] = useState(false);

  async function run() {
    if (busy) return;
    setBusy(true);
    setError(false);
    const r = await scoreChurn({
      recencyDays: recency, frequencyOrders: frequency, sessionsLastMonth: sessions,
      cartAbandonRate: abandon / 100, trend,
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
            <CardTitle>Hành vi khách hàng</CardTitle>
            <p className="mt-1 text-xs text-text-muted">Chỉnh các chỉ số để mô phỏng một khách hàng cụ thể.</p>
          </div>
          <Badge variant="muted">RFM heuristic</Badge>
        </CardHeader>
        <CardContent className="space-y-4">
          <NumberField label="Ngày chưa mua lại" value={recency} onChange={setRecency} max={200} />
          <NumberField label="Số đơn đã mua" value={frequency} onChange={setFrequency} max={30} />
          <NumberField label="Số phiên truy cập / tháng" value={sessions} onChange={setSessions} max={30} />
          <NumberField label="Tỉ lệ bỏ giỏ hàng (%)" value={abandon} onChange={setAbandon} max={100} />
          <div>
            <label className="mono text-2xs uppercase tracking-wider text-text-dim">Xu hướng hoạt động</label>
            <div className="mt-1.5 inline-flex overflow-hidden rounded-md border border-border">
              {TRENDS.map((t) => (
                <button
                  key={t.value}
                  type="button"
                  onClick={() => setTrend(t.value)}
                  className={cn(
                    "px-3 py-2 text-xs font-medium transition-colors",
                    trend === t.value ? "bg-accent/15 text-accent" : "text-text-muted hover:text-text",
                  )}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>
          <Button onClick={run} disabled={busy} className="w-full">
            {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <UserMinus className="h-3.5 w-3.5" />}
            Dự đoán churn
          </Button>
        </CardContent>
      </Card>

      <Card className="lg:col-span-5">
        <CardHeader>
          <CardTitle>Kết quả</CardTitle>
        </CardHeader>
        <CardContent>
          {error ? (
            <p className="text-sm text-danger">Không lấy được kết quả. Kiểm tra kết nối backend rồi thử lại.</p>
          ) : !result ? (
            <p className="text-sm text-text-muted">Bấm Dự đoán churn để xem nguy cơ rời bỏ.</p>
          ) : (
            <div className="space-y-4">
              <div>
                <div className={cn("text-3xl font-semibold tracking-tight", band?.cls)}>
                  {Math.round(result.churn_risk * 100)}% — {band?.label}
                </div>
                <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-surface-2">
                  <div
                    className={cn("h-full rounded-full transition-all",
                      result.risk_band === "high" ? "bg-danger" : result.risk_band === "medium" ? "bg-warning" : "bg-success")}
                    style={{ width: `${Math.round(result.churn_risk * 100)}%` }}
                  />
                </div>
              </div>
              <div>
                <div className="mono text-2xs uppercase tracking-wider text-text-dim">Yếu tố chính</div>
                <ul className="mt-2 space-y-1">
                  {result.drivers.map((d, i) => (
                    <li key={i} className="text-xs text-text-muted">• {d}</li>
                  ))}
                </ul>
              </div>
              <div className="rounded-md border border-border bg-bg-alt px-3 py-2 text-xs text-text">
                {result.retention_action}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
