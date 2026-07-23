"use client";

import { useState } from "react";
import { Loader2, Send, CheckCircle2, XCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { negotiate } from "@/lib/features";
import { cn } from "@/lib/utils";

type Turn = { role: "buyer" | "bot"; text: string; decision?: "accept" | "counter" | "reject" };

const VND = new Intl.NumberFormat("vi-VN");

export function NegotiationPanel() {
  const [productName] = useState("Lô 500 áo thun cotton B2B");
  const [listPrice] = useState(1_200_000);
  const [minPrice] = useState(850_000);
  const [offer, setOffer] = useState("900000");
  const [round, setRound] = useState(1);
  const [done, setDone] = useState<"accept" | "reject" | null>(null);
  const [busy, setBusy] = useState(false);
  const [turns, setTurns] = useState<Turn[]>([]);
  const [error, setError] = useState(false);

  async function send() {
    if (busy || done || !offer.trim()) return;
    const offerNum = Number(offer.replace(/\D/g, ""));
    setBusy(true);
    setError(false);
    setTurns((prev) => [...prev, { role: "buyer", text: `Mình đề nghị ${VND.format(offerNum)}₫` }]);

    const r = await negotiate({
      productName, listPriceVnd: listPrice, minPriceVnd: minPrice, buyerOfferVnd: offerNum, round,
    });
    setError(r === null);
    if (r) {
      setTurns((prev) => [...prev, { role: "bot", text: r.message, decision: r.decision }]);
      if (r.decision === "accept") setDone("accept");
      else if (r.decision === "reject") setDone("reject");
      else if (r.counter_price_vnd) setOffer(String(r.counter_price_vnd));
      setRound((r) => r + 1);
    }
    setBusy(false);
  }

  function reset() {
    setTurns([]); setRound(1); setDone(null); setOffer("900000"); setError(false);
  }

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <Card className="lg:col-span-5">
        <CardHeader>
          <div>
            <CardTitle>Lô hàng B2B</CardTitle>
            <p className="mt-1 text-xs text-text-muted">{productName}</p>
          </div>
          <Badge variant="muted">round {round}</Badge>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <div className="flex justify-between"><span className="text-text-muted">Giá niêm yết</span><span className="mono text-text">{VND.format(listPrice)}₫</span></div>
          <div className="flex justify-between"><span className="text-text-muted">Giá sàn (ẩn với buyer)</span><span className="mono text-text">{VND.format(minPrice)}₫</span></div>
          {done && (
            <Button variant="secondary" size="sm" onClick={reset} className="mt-3 w-full">Bắt đầu lại</Button>
          )}
        </CardContent>
      </Card>

      <Card className="lg:col-span-7">
        <CardHeader><CardTitle>Đàm phán</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div className="max-h-72 space-y-2 overflow-y-auto rounded-md border border-border bg-bg-alt p-3">
            {turns.length === 0 && <p className="text-xs text-text-dim">Nhập mức giá đề nghị và bấm Gửi để bắt đầu.</p>}
            {turns.map((t, i) => (
              <div key={i} className={cn("flex", t.role === "buyer" ? "justify-end" : "justify-start")}>
                <div className={cn(
                  "max-w-[80%] rounded-lg px-3 py-2 text-xs",
                  t.role === "buyer" ? "bg-accent/15 text-text" : "bg-surface text-text",
                )}>
                  {t.decision === "accept" && <CheckCircle2 className="mb-1 h-4 w-4 text-success" />}
                  {t.decision === "reject" && <XCircle className="mb-1 h-4 w-4 text-danger" />}
                  {t.text}
                </div>
              </div>
            ))}
            {error && (
              <p className="text-sm text-danger">Không lấy được phản hồi. Kiểm tra kết nối backend rồi thử lại.</p>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Input
              value={offer}
              onChange={(e) => setOffer(e.target.value)}
              disabled={busy || !!done}
              placeholder="Mức giá đề nghị (₫)"
              className="h-10"
            />
            <Button onClick={send} disabled={busy || !!done}>
              {busy ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : <Send className="h-3.5 w-3.5" />}
              Gửi
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
