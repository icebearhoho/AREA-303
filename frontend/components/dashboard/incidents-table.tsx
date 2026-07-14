import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Alert, ALERTS } from "@/lib/mock-data";

type AlertRow = (typeof ALERTS)[number];

const severityVariant: Record<
  Alert["severity"],
  "danger" | "warning" | "info"
> = {
  critical: "danger",
  warning: "warning",
  info: "info",
};

const statusVariant: Record<
  Alert["status"],
  "danger" | "warning" | "muted"
> = {
  open: "danger",
  monitoring: "warning",
  resolved: "muted",
};

export function AlertsTable({ data }: { data: AlertRow[] }) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Alerts feed</CardTitle>
          <p className="mt-1 text-xs text-text-muted">
            5 sự kiện gần nhất trên toàn bộ 17 features.
          </p>
        </div>
        <Badge variant="muted">{data.length} hiển thị</Badge>
      </CardHeader>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Feature</TableHead>
            <TableHead>Vùng</TableHead>
            <TableHead>Severity</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Bắt đầu</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((a) => (
            <TableRow key={a.id}>
              <TableCell className="mono text-text">{a.id}</TableCell>
              <TableCell>
                <div className="flex flex-col">
                  <span>{a.featureLabel}</span>
                  <span className="text-xs text-text-muted">{a.message}</span>
                </div>
              </TableCell>
              <TableCell className="mono text-xs text-text-muted">{a.region}</TableCell>
              <TableCell>
                <Badge variant={severityVariant[a.severity]}>{a.severity}</Badge>
              </TableCell>
              <TableCell>
                <Badge variant={statusVariant[a.status]}>{a.status}</Badge>
              </TableCell>
              <TableCell className="mono text-xs text-text-muted text-right">
                {a.startedAt}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Card>
  );
}