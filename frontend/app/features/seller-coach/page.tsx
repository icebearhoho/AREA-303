import { DashboardShell } from "@/components/shell/dashboard-shell";
import { FeatureHeader } from "@/components/genai/feature-header";
import { SellerCoachPanel } from "@/components/features/seller-coach-panel";

export const dynamic = "force-dynamic";

export default function SellerCoachPage() {
  return (
    <DashboardShell
      breadcrumb={[{ label: "Overview", href: "/" }, { label: "Seller Coach" }]}
    >
      <FeatureHeader
        id="17"
        title="Seller Coach"
        subtitle="Đánh giá 5-chiều (listing · pricing · visuals · reviews · inventory) + Gemini sinh roadmap 4 tuần cho seller."
        category="Generative AI"
        owner="FS"
      />
      <SellerCoachPanel />
    </DashboardShell>
  );
}