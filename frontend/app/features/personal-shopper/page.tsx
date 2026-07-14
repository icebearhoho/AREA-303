import { DashboardShell } from "@/components/shell/dashboard-shell";
import { FeatureHeader } from "@/components/genai/feature-header";
import { PersonalShopperPanel } from "@/components/features/personal-shopper-panel";

export const dynamic = "force-dynamic";

export default function PersonalShopperPage() {
  return (
    <DashboardShell
      breadcrumb={[{ label: "Overview", href: "/" }, { label: "Personal Shopper" }]}
    >
      <FeatureHeader
        id="03"
        title="Personal Shopper"
        subtitle="RAG retrieval trên Tiki catalog + preference signal từ Sephora reviews, sinh gợi ý tiếng Việt qua Gemini 1.5 Pro với SSE streaming."
        category="Generative AI"
        owner="FS"
      />
      <PersonalShopperPanel />
    </DashboardShell>
  );
}