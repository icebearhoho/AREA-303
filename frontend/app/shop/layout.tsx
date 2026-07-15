import { Nunito } from "next/font/google";
import { ShopShell } from "@/components/shell/shop-shell";

const nunito = Nunito({
  subsets: ["latin", "vietnamese"],
  variable: "--font-shop",
  display: "swap",
  weight: ["400", "600", "700", "800"],
});

export default function ShopLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className={`${nunito.variable} theme-shop`}>
      <ShopShell>{children}</ShopShell>
    </div>
  );
}
