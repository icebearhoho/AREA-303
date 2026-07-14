import { DashboardShell } from "@/components/shell/dashboard-shell";
import { FeatureHeader } from "@/components/genai/feature-header";
import { ContentGeneratorPanel } from "@/components/features/content-generator-panel";

export const dynamic = "force-dynamic";

export default function ContentGeneratorPage() {
  return (
    <DashboardShell
      breadcrumb={[{ label: "Overview", href: "/" }, { label: "Content Generator" }]}
    >
      <FeatureHeader
        id="09"
        title="Content Generator"
        subtitle="Auto-generate mô tả sản phẩm tiếng Việt cho 3 platform (Shopee · Tiki · TikTok Shop) với few-shot prompt riêng + predicted CTR."
        category="Generative AI"
        owner="FS"
      />
      <ContentGeneratorPanel />
    </DashboardShell>
  );
}