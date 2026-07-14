import {
  LayoutDashboard,
  Star,
  Tag,
  ShoppingBag,
  UserMinus,
  ShieldAlert,
  TrendingUp,
  Image as ImageIcon,
  MessageSquare,
  PenLine,
  RotateCcw,
  Sparkles,
  ScanFace,
  Heart,
  MessagesSquare,
  BadgePercent,
  Truck,
  GraduationCap,
  type LucideIcon,
} from "lucide-react";

/**
 * Navigation contract — 17 e-commerce AI/ML features for AREA-303.
 *
 * Slug suffix is the canonical id; appears on every nav row right-aligned in mono.
 * Section groups mirror the day-by-day build plan in the project README.
 */
export type NavItem = {
  id: string; // canonical feature id e.g. "01", "17"
  slug: string;
  label: string;
  href: string;
  icon: LucideIcon;
  section: "commerce" | "intelligence" | "creator" | "operations" | "demand";
  category:
    | "NLP"
    | "Time Series"
    | "Computer Vision"
    | "Generative AI"
    | "Behavioral AI";
  owner: "TL" | "DA" | "FS" | "D1" | "D2";
};

export const NAV_ITEMS: NavItem[] = [
  // Commerce — review, pricing, search, try-on
  { id: "01", slug: "review-analyzer",  label: "Review Analyzer",    href: "/features/review-analyzer",  icon: Star,          section: "commerce",     category: "NLP",              owner: "DA" },
  { id: "02", slug: "dynamic-pricing",  label: "Dynamic Pricing",    href: "/features/dynamic-pricing",  icon: Tag,           section: "commerce",     category: "Time Series",     owner: "TL" },
  { id: "03", slug: "personal-shopper", label: "Personal Shopper",   href: "/features/personal-shopper", icon: ShoppingBag,   section: "commerce",     category: "Generative AI",   owner: "FS" },
  { id: "07", slug: "visual-search",    label: "Visual Search",      href: "/features/visual-search",    icon: ImageIcon,     section: "commerce",     category: "Computer Vision", owner: "DA" },
  { id: "12", slug: "virtual-tryon",    label: "Virtual Try-On",     href: "/features/virtual-tryon",    icon: ScanFace,      section: "commerce",     category: "Computer Vision", owner: "DA" },
  { id: "11", slug: "recsys",           label: "Recommend (RecSys)", href: "/features/recsys",           icon: Sparkles,      section: "commerce",     category: "Generative AI",   owner: "FS" },

  // Intelligence — churn, fake review, return, regret, sentiment
  { id: "04", slug: "churn",            label: "Churn Radar",        href: "/features/churn",            icon: UserMinus,     section: "intelligence", category: "Behavioral AI",   owner: "TL" },
  { id: "05", slug: "fake-review",      label: "Fake Review",        href: "/features/fake-review",      icon: ShieldAlert,   section: "intelligence", category: "NLP",              owner: "DA" },
  { id: "06", slug: "demand-forecast",  label: "Demand Forecast",    href: "/features/demand-forecast",  icon: TrendingUp,    section: "intelligence", category: "Time Series",     owner: "DA" },
  { id: "10", slug: "return-predict",   label: "Return Predict",     href: "/features/return-predict",   icon: RotateCcw,     section: "intelligence", category: "Behavioral AI",   owner: "DA" },
  { id: "13", slug: "emotion-sale",     label: "Emotion Sale",       href: "/features/emotion-sale",     icon: Heart,         section: "intelligence", category: "Behavioral AI",   owner: "D1" },
  { id: "15", slug: "regret-predict",   label: "Regret Predict",     href: "/features/regret-predict",   icon: BadgePercent,  section: "intelligence", category: "Behavioral AI",   owner: "D1" },

  // Creator — content, negotiation, seller coach, sentiment alert
  { id: "09", slug: "content-generator",label: "Content Generator",  href: "/features/content-generator",icon: PenLine,       section: "creator",      category: "Generative AI",   owner: "FS" },
  { id: "14", slug: "negotiation",      label: "Negotiation Bot",    href: "/features/negotiation",      icon: MessagesSquare,section: "creator",      category: "Generative AI",   owner: "D1" },
  { id: "17", slug: "seller-coach",     label: "Seller Coach",       href: "/features/seller-coach",     icon: GraduationCap, section: "creator",      category: "Generative AI",   owner: "FS" },
  { id: "08", slug: "sentiment-alert",  label: "Sentiment Alert",    href: "/features/sentiment-alert",  icon: MessageSquare, section: "creator",      category: "NLP",              owner: "D1" },

  // Operations — supply chain
  { id: "16", slug: "supply-chain",     label: "Supply Chain",       href: "/features/supply-chain",     icon: Truck,         section: "operations",   category: "Time Series",     owner: "TL" },
];

export const NAV_SECTIONS: Array<{ id: NavItem["section"]; title: string }> = [
  { id: "commerce",    title: "Commerce" },
  { id: "intelligence",title: "Intelligence" },
  { id: "creator",     title: "Creator" },
  { id: "operations",  title: "Operations" },
];

export const SECTION_TITLES: Record<NavItem["section"], string> = {
  commerce: "Commerce",
  intelligence: "Intelligence",
  creator: "Creator",
  operations: "Operations",
  demand: "Demand",
};

/** Quick lookup by slug for the dynamic page fallback. */
export function findBySlug(slug: string): NavItem | undefined {
  return NAV_ITEMS.find((i) => i.slug === slug);
}