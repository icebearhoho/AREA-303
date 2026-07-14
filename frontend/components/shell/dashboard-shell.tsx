import { Sidebar } from "./sidebar";
import { TopBar } from "./topbar";

export function DashboardShell({
  breadcrumb,
  children,
}: {
  breadcrumb: { label: string; href?: string }[];
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-bg">
      <Sidebar />
      <div className="lg:pl-60">
        <TopBar breadcrumb={breadcrumb} />
        <main className="px-4 py-6 lg:px-8 lg:py-8">{children}</main>
      </div>
    </div>
  );
}