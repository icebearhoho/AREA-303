import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { NavItem } from "@/lib/nav";

const OWNER_LABEL: Record<string, string> = {
  TL: "Team Lead", DA: "Data / ML", FS: "Fullstack", D1: "Developer 1", D2: "Developer 2",
};

export function ComingSoon({ item }: { item: NavItem }) {
  return (
    <Card>
      <CardHeader>
        <div>
          <CardTitle>Coming soon</CardTitle>
          <p className="mt-1 text-xs text-text-muted">
            Feature này thuộc phần việc của{" "}
            <span className="text-text">{OWNER_LABEL[item.owner] ?? item.owner}</span>. Sẽ được
            wire vào {item.app === "seller" ? "Seller Portal" : "Shop"} khi owner merge.
          </p>
        </div>
        <Badge variant="muted">{item.category}</Badge>
      </CardHeader>
      <CardContent>
        <pre className="mono overflow-x-auto rounded-md border border-border bg-bg-alt p-4 text-xs text-text-muted">
{`app:      ${item.app}
route:    ${item.href}
id:       #${item.id}
owner:    ${item.owner} (${OWNER_LABEL[item.owner]})
category: ${item.category}`}
        </pre>
      </CardContent>
    </Card>
  );
}
