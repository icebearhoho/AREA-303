# AREA-303 — Operations Dashboard

Reference DESIGN.md for the Next.js 14 App Router dashboard: shadcn/ui primitives, Tailwind tokens, sidebar shell with 17 feature links, KPI cards on the home surface, Recharts + react-leaflet wired as the analytics + map engine. The product reads like an SRE console — dark canvas, terminal-derived type for data, restrained chromatic accents, edges sharp enough to feel like cells.

## 1. Visual Theme & Atmosphere

Dark operations console. Deep neutral canvas, layered surfaces for elevation, a single chromatic accent for primary action and live data. Headlines lean sans for legibility; numbers and identifiers lean mono — the same separation an engineer draws between labels and values in a Grafana panel. Charts and maps sit inside bordered cards; chrome never bleeds into the data layer. Density first, decoration last.

Mood: technical, calm, instrument-grade.

## 2. Color Palette & Roles

```
/* canvas */
--bg:              #0a0a0f        /* deep neutral, page background */
--bg-alt:          #11121a        /* sidebar, table header rows */
--surface:         #161823        /* default card */
--surface-2:       #1d2030        /* hover, nested card */
--surface-3:       #252839        /* active row, selected KPI */

/* type */
--text:            #e8e9ef        /* primary text */
--text-muted:      #9ea1b3        /* secondary text, axis labels */
--text-dim:        #5f6378        /* placeholder, disabled */

/* lines */
--border:          #232636        /* default 1px divider */
--border-strong:   #2f3349        /* input border, emphasized rule */

/* chromatic — ONE accent carries action + live data */
--accent:          #5eead4        /* teal — primary CTA, active nav, live dot */
--accent-hover:    #7df0dd
--accent-deep:     #2cb5a0

/* semantic — used sparingly, never as decoration */
--success:         #4ade80
--warning:         #fbbf24
--danger:          #f87171
--info:            #60a5fa

/* data viz palette — Recharts series */
--series-1:        #5eead4
--series-2:        #a78bfa
--series-3:        #fbbf24
--series-4:        #f472b6
--series-5:        #60a5fa
```

Rule: teal `--accent` owns primary action, the active sidebar item, and the "live" indicator dot on realtime widgets. The data-viz series palette rotates for multi-series charts only — never for chrome or copy. Semantic colors appear only on status pills, alert banners, and chart deltas.

## 3. Typography Rules

- **UI / headlines / body:** `Inter`, fallback system sans. Weight 400 / 500 / 600 / 700.
- **Numerals, code, IDs, monospace blocks:** `JetBrains Mono`, fallback `ui-monospace`. Weight 400 / 500 / 700.
- Mixed face is the look — labels in Inter, every metric value, timestamp, hash, and command in JetBrains Mono. Never the other way.
- Letter-spacing: -0.01em on display headlines, 0 elsewhere.
- Line-height: 1.5 body, 1.2 headings, 1.4 code blocks.

Scale (px): 11 / 12 / 13 / 14 / 16 / 18 / 22 / 28 / 36 / 48.

Numerals: tabular (`font-feature-settings: "tnum"`) on every metric, KPI, table cell, and axis tick.

## 4. Component Stylings

**Sidebar (persistent shell)**
- 240px fixed width on desktop, 64px icon-rail at ≥1024px, full overlay drawer below 768px.
- `--bg-alt` fill, 1px right `--border`.
- Brand mark at top (16px mono wordmark, accent dot).
- 17 nav items: 36px row height, 14px Inter label, 14px mono ID slug on the right in `--text-dim`. Active row: `--surface-3` fill + 2px left `--accent` border. Hover: `--surface-2` fill.
- Section headers: 11px uppercase Inter, +4% tracking, `--text-dim`.

**Top bar (per route)**
- 56px height, `--bg` fill, 1px bottom `--border`.
- Breadcrumb left (Inter 13px). Search input center (`⌘K` kbd hint right). User menu right.

**KPI cards**
- `--surface` fill, 1px `--border`, radius 10. Padding 20.
- Header: 12px uppercase Inter muted, +4% tracking.
- Value: JetBrains Mono 36px / weight 500, tabular.
- Delta: 12px mono, `--success` for up / `--danger` for down, optional arrow glyph.
- Sparkline (Recharts `<Line>`) under the value, 40px tall, accent stroke, no axes.
- Hover: 1px `--border-strong` border, no lift.

**Buttons**
- Primary: `--accent` fill, `#0a0a0f` text, radius 8, padding 8/14, weight 500.
- Secondary: transparent fill, 1px `--border-strong`, `--text` color. Hover: 1px `--accent` border.
- Ghost: `--text-muted` text, hover `--text`.
- Destructive: `--danger` fill, `#0a0a0f` text — only on confirm dialogs.
- Icon button: 32px square, `--surface` fill, `--border`, radius 8.

**Inputs**
- `--bg-alt` fill, 1px `--border-strong`, radius 8, padding 8/12.
- Focus: 2px `--accent` ring, no offset.
- Placeholder in `--text-dim`.

**Tables**
- Header row: `--bg-alt` fill, 11px uppercase Inter +4%, `--text-muted`.
- Body rows: 48px height, 1px bottom `--border`.
- Hover: `--surface-2` fill. Selected: `--surface-3` fill + 2px left `--accent`.
- Monospace for IDs, timestamps, numeric columns. Inter for label columns.

**Cards / panels**
- `--surface` fill, 1px `--border`, radius 10. Padding 20.
- Header: 14px Inter weight 600 left, optional action right.
- Nested code block: `--bg-alt` fill, 1px `--border`, radius 6.

**Charts (Recharts)**
- Grid: 1px `--border`, dashed on Y axis only.
- Axis labels: 11px mono `--text-dim`.
- Tooltip: `--surface-2` fill, 1px `--border-strong`, radius 8, 12px mono values.
- Legend: 12px Inter, square swatches, top-right placement.
- Animations: 200ms ease-out, disabled when `prefers-reduced-motion`.

**Map (react-leaflet)**
- Custom dark tile layer (CARTO `dark_all`).
- Markers: 8px circle, `--accent` fill, 1px `#0a0a0f` stroke for legibility on dark tiles.
- Clusters: `--surface-2` fill, `--accent` border, mono count.
- Popup: `--surface-2` fill, 1px `--border-strong`, radius 8.

**Command palette (`⌘K`)**
- Centered modal, 560px wide, `--surface-2` fill, 1px `--accent` border, radius 12.
- Input row at top, 56px, 1px bottom `--border`. Result rows 44px, hover `--surface-3`.
- Mono for IDs and shortcuts, Inter for descriptions.

**Status pills**
- 11px Inter weight 500, uppercase, +4% tracking.
- Live: `--accent` text, `--accent` 12% background fill, 2px accent dot.
- Warning: `--warning` text, 12% warning fill.
- Danger: `--danger` text, 12% danger fill.

## 5. Layout Principles

- 1440px app-shell max. Sidebar 240px + main fluid. Main content max-width 1280px, centered.
- 4px base unit. 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.
- Page padding: 32px desktop, 16px mobile.
- KPI strip: 4-column grid on desktop (1fr × 4, 16px gap), 2-column on tablet, 1-column on mobile.
- Chart grids: 12-column CSS grid. Primary chart spans 8 cols, secondary spans 4 cols. 24px gap.
- Density: 48px table rows, 36px nav rows, 32px button height. This is an operations surface — tight beats spacious.
- Sections separated by 1px `--border` rules, not whitespace gaps.
- shadcn/ui primitives sit on Tailwind tokens via `tailwind.config.ts` CSS variables — never hardcode hex.

## 6. Depth & Elevation

Flat with surface layering. `bg → bg-alt → surface → surface-2 → surface-3` is the entire elevation language. No drop shadows on cards or KPIs. Modals and the command palette add a single backdrop layer (`rgba(0,0,0,0.6)`) and a 1px `--border-strong` or `--accent` rule on the panel itself. Hover changes the border, not the shadow.

## 7. Do's and Don'ts

**Do**
- Mix Inter (labels) and JetBrains Mono (values) in every KPI row and table.
- Reserve teal `--accent` for primary CTA, active sidebar item, and the live indicator dot.
- Use the 5-color series palette only inside Recharts and the map legend.
- Wire every chromatic use to a semantic role — if a color has no job, remove it.
- Reach for shadcn/ui primitives (`Card`, `Button`, `Input`, `Dialog`, `Command`, `Table`) before rolling custom.
- Treat the sidebar as the navigation contract — 17 links, fixed order, slug suffix per route.

**Don't**
- Use teal as type color. Teal is action + active state, never body copy.
- Add gradients, glows, or scale-on-hover lifts to cards or buttons.
- Soften corners past 12px. Cards 10, buttons 8, inputs 8, modals 12.
- Introduce a second accent color outside the semantic set.
- Use sans for numeric values. If a number appears, it must be mono + tabular.
- Stack more than 5 series in a single chart — break the panel.
- Add illustrations, mascots, or decorative photography to the dashboard shell.

## 8. Responsive Behavior

- Sidebar collapses to 64px icon-rail at <1024px, full overlay drawer at <768px.
- KPI strip: 4 → 2 columns at <1024px, 1 column at <640px.
- Chart grid: 8/4 split → stacked single column at <768px.
- Tables become horizontally scrollable below 768px, sticky first column for ID.
- Command palette goes full-screen below 640px.
- Type scale steps down one tier at <768px (36 → 28 for KPI values).
- Map: full-width, controls bottom-right, popup auto-anchored above marker on mobile.

## 9. Agent Prompt Guide

Bias: dark `#0a0a0f` canvas with 5-tier surface elevation (`bg → bg-alt → surface → surface-2 → surface-3`), single teal `#5eead4` accent for primary CTA + active sidebar + live dot, Inter for UI/headlines + JetBrains Mono for every numeric and identifier value (mixed in the same row), shadcn/ui primitives wired to Tailwind CSS variables, 240px persistent sidebar shell with 17 feature links, 4 KPI cards on the home surface using Recharts sparklines, react-leaflet with a dark CARTO tile layer, 10px card radius / 8px button radius / 12px modal radius, tabular numerals on every metric, semantic colors only on status pills and chart deltas, Recharts and react-leaflet as the only chart/map engines.

Reject: light themes, gradient fills, drop shadows on cards or KPIs, scale-on-hover lifts, multi-typeface mixing inside a single value cell (sans for the number, mono for the unit), more than one chromatic accent in chrome, decorative illustration in the dashboard shell, sans-only numerals on KPI cards, corner radii past 12px, hex colors hardcoded outside `tailwind.config.ts` CSS variables, stacked series beyond 5 in a single chart.