"use client";

import type { ComponentType } from "react";
import { PersonalShopperPanel } from "./personal-shopper-panel";
import { RecsysPanel } from "./recsys-panel";
import { ContentGeneratorPanel } from "./content-generator-panel";
import { SellerCoachPanel } from "./seller-coach-panel";
import { ReviewSentimentPanel } from "./review-sentiment-panel";
import { FakeReviewPanel } from "./fake-review-panel";
import { DynamicPricingPanel } from "./dynamic-pricing-panel";
import { ChurnPanel } from "./churn-panel";
import { CustomerJourneyPanel } from "./customer-journey-panel";

/** Maps a feature slug to its live panel. Keep in sync with IMPLEMENTED in lib/nav. */
const PANELS: Record<string, ComponentType> = {
  "personal-shopper": PersonalShopperPanel,
  recsys: RecsysPanel,
  "content-generator": ContentGeneratorPanel,
  "seller-coach": SellerCoachPanel,
  "review-analyzer": ReviewSentimentPanel,
  "fake-review": FakeReviewPanel,
  "dynamic-pricing": DynamicPricingPanel,
  churn: ChurnPanel,
  "customer-journey": CustomerJourneyPanel,
};

export function FeaturePanel({ slug }: { slug: string }) {
  const Panel = PANELS[slug];
  return Panel ? <Panel /> : null;
}
