import { DashboardShell } from "@/components/shell/dashboard-shell";
import { FeatureHeader } from "@/components/genai/feature-header";
import { RecsysPanel } from "@/components/features/recsys-panel";

export const dynamic = "force-dynamic";

export default function RecsysPage() {
  return (
    <DashboardShell
      breadcrumb={[{ label: "Overview", href: "/" }, { label: "RecSys" }]}
    >
      <FeatureHeader
        id="11"
        title="Recommend (RecSys)"
        subtitle="Hybrid collaborative filtering (LightFM / BERT4Rec) kết hợp LLM reasoning giải thích 'vì sao' sản phẩm phù hợp với user."
        category="Generative AI"
        owner="FS"
      />
      <RecsysPanel />
    </DashboardShell>
  );
}