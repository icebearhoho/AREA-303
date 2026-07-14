import json
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import config

st.set_page_config(page_title="Social Trend Analyzer", page_icon="📈", layout="wide")

# ============================================================
# Palette + CSS (system fonts, no CDN -> works offline)
# ============================================================
INK, INK_SUB, INK_MUTE = "#e6e8ee", "#9aa3b2", "#6b7280"
BRAND, CARD_BG, BORDER = "#818cf8", "#161a23", "#262c3a"
STATUS = {
    "RESTOCK": {"c": "#22c55e", "icon": "↑", "label": "RESTOCK"},
    "WATCH":   {"c": "#f59e0b", "icon": "→", "label": "MONITOR"},
    "REDUCE":  {"c": "#ef4444", "icon": "↓", "label": "REDUCE STOCK"},
}

st.markdown(f"""
<style>
  [data-testid="stHeader"], #MainMenu, footer {{ display:none; }}
  .block-container {{ max-width:1180px; padding-top:2.2rem; padding-bottom:3rem; }}
  html, body, [class*="css"] {{
    font-family:-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; }}
  .eyebrow {{ color:{BRAND}; font-size:.72rem; font-weight:700; letter-spacing:.14em;
             text-transform:uppercase; margin-bottom:.35rem; }}
  .app-title {{ font-size:1.9rem; font-weight:800; color:{INK}; margin:0; line-height:1.1; }}
  .app-sub {{ color:{INK_SUB}; font-size:.95rem; margin-top:.4rem; }}
  .mode-chip {{ float:right; font-size:.72rem; font-weight:600; color:{INK_SUB};
               border:1px solid {BORDER}; border-radius:999px; padding:.28rem .7rem; }}
  .section {{ font-size:1.05rem; font-weight:700; color:{INK}; margin:1.9rem 0 .8rem; }}
  .kpi-row {{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; }}
  .kpi {{ background:{CARD_BG}; border:1px solid {BORDER}; border-radius:12px; padding:16px 18px; }}
  .kpi-label {{ color:{INK_MUTE}; font-size:.74rem; font-weight:600; letter-spacing:.04em; text-transform:uppercase; }}
  .kpi-value {{ color:{INK}; font-size:1.75rem; font-weight:800; margin-top:.25rem; line-height:1; }}
  .kpi-note {{ color:{INK_MUTE}; font-size:.72rem; margin-top:.35rem; }}
  .alert-row {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; }}
  .card {{ background:{CARD_BG}; border:1px solid {BORDER}; border-radius:12px;
          padding:15px 17px; border-top:3px solid var(--c); }}
  .pill {{ display:inline-block; font-size:.7rem; font-weight:700; letter-spacing:.03em;
          color:var(--c); background:color-mix(in srgb, var(--c) 15%, transparent);
          border-radius:999px; padding:.18rem .55rem; }}
  .card-brand {{ color:{INK}; font-weight:700; font-size:1.02rem; margin:.55rem 0 .4rem; }}
  .card-metrics {{ color:{INK_SUB}; font-size:.83rem; margin-bottom:.5rem; }}
  .card-metrics b {{ color:{INK}; }}
  .card-hint {{ color:{INK_SUB}; font-size:.8rem; line-height:1.35; }}
  .stat-tile {{ background:{CARD_BG}; border:1px solid {BORDER}; border-radius:10px; padding:12px 14px; }}
  .stat-tile .l {{ color:{INK_MUTE}; font-size:.72rem; text-transform:uppercase; }}
  .stat-tile .v {{ color:{INK}; font-size:1.3rem; font-weight:700; margin-top:.2rem; }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load():
    O = config.OUTPUT_DIR
    demo = O / "demo_data.json"
    if demo.exists():                          # ---- DEMO MODE: 1 file JSON tu chua ----
        d = json.loads(demo.read_text(encoding="utf-8"))

        def df(records, datecols=()):
            x = pd.DataFrame(records)
            for c in datecols:
                x[c] = pd.to_datetime(x[c])
            return x

        return (df(d["alerts"]), df(d["brand_monthly"], ["month"]),
                df(d["brand_forecast"], ["month"]), df(d["brand_trends"]),
                df(d["product_monthly"], ["month"]),
                d["meta"], d.get("sentiment_examples", []), "Demo · JSON")

    # ---- LIVE MODE: doc parquet goc ----
    alerts = pd.read_parquet(O / "brand_alerts.parquet")
    bm     = pd.read_parquet(O / "brand_monthly.parquet")
    bf     = pd.read_parquet(O / "brand_forecast.parquet")
    bt     = pd.read_parquet(O / "brand_trends.parquet")
    pm     = pd.read_parquet(O / "product_monthly.parquet")
    meta = {
        "reviews": int(bm["volume"].sum()),
        "brands": int(bm["brand_name"].nunique()),
        "months": int(bm["month"].nunique()),
        "rising": int(bt["rising"].sum()),
        "span": f'{bm["month"].min():%b %Y} - {bm["month"].max():%b %Y}',
    }
    return alerts, bm, bf, bt, pm, meta, [], "Live · parquet"


alerts, bm, bf, bt, pm, meta, examples, mode = load()

# ---------- Header ----------
st.markdown(f"""
<div>
  <span class="mode-chip">{mode}</span>
  <div class="eyebrow">AREA 303 · Track 2 · Feature #08</div>
  <div class="app-title">Social Trend Analyzer</div>
  <div class="app-sub">Spot rising beauty brands from real review activity — restock guidance for sellers.</div>
</div>
""", unsafe_allow_html=True)

# ---------- KPI ----------
st.markdown(f"""
<div class="kpi-row" style="margin-top:1.6rem">
  <div class="kpi"><div class="kpi-label">Reviews analyzed</div>
    <div class="kpi-value">{meta['reviews']:,}</div><div class="kpi-note">real customer reviews</div></div>
  <div class="kpi"><div class="kpi-label">Brands tracked</div>
    <div class="kpi-value">{meta['brands']}</div><div class="kpi-note">across 2,073 products</div></div>
  <div class="kpi"><div class="kpi-label">Time span</div>
    <div class="kpi-value">{meta['months']} mo</div><div class="kpi-note">{meta['span']}</div></div>
  <div class="kpi"><div class="kpi-label">Rising brands</div>
    <div class="kpi-value" style="color:{BRAND}">{meta['rising']}</div><div class="kpi-note">momentum &gt; 20</div></div>
</div>
""", unsafe_allow_html=True)

# ---------- Alert cards ----------
st.markdown('<div class="section">Restock signals</div>', unsafe_allow_html=True)
cards = ""
for _, a in alerts.iterrows():
    s = STATUS[a["alert"]]
    cards += (
        f"<div class='card' style='--c:{s['c']}'>"
        f"<span class='pill'>{s['icon']} {s['label']}</span>"
        f"<div class='card-brand'>{a['brand']}</div>"
        f"<div class='card-metrics'><b>{a['trend']}</b> · ~{a['recent_avg']:.0f} reviews/mo · "
        f"<b>{a['recent_pos']}%</b> positive</div>"
        f"<div class='card-hint'>{a['action']}</div></div>"
    )
st.markdown(f"<div class='alert-row'>{cards}</div>", unsafe_allow_html=True)

# ---------- Brand trend ----------
st.markdown('<div class="section">Brand trend & forecast</div>', unsafe_allow_html=True)
order = bt.sort_values("momentum", ascending=False)
sel = st.selectbox("Brand", order["brand"].tolist(),
                   format_func=lambda b: f"{b} · {order.set_index('brand').loc[b, 'trend']}",
                   label_visibility="collapsed")

hist = bm[bm["brand_name"] == sel].sort_values("month")
fcst = bf[bf["brand"] == sel].sort_values("month")
row = bt.set_index("brand").loc[sel]

col_chart, col_stats = st.columns([3, 1])
with col_chart:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist["month"], y=hist["volume"], mode="lines", name="Reviews / month",
        line=dict(color=BRAND, width=2.5), fill="tozeroy", fillcolor="rgba(129,140,248,0.13)",
        hovertemplate="%{x|%b %Y}<br><b>%{y}</b> reviews<extra></extra>"))
    if len(fcst):
        fx = [hist["month"].iloc[-1]] + list(fcst["month"])
        fy = [hist["volume"].iloc[-1]] + list(fcst["yhat"])
        fig.add_trace(go.Scatter(
            x=fx, y=fy, mode="lines", name="Forecast (Prophet)",
            line=dict(color="#f59e0b", width=2, dash="dot"),
            hovertemplate="%{x|%b %Y}<br>forecast <b>%{y}</b><extra></extra>"))
    fig.update_layout(
        height=330, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified", font=dict(color=INK_SUB, size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0),
        xaxis=dict(showgrid=False, color=INK_MUTE),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False, color=INK_MUTE))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with col_stats:
    st.markdown(f"""
    <div class="stat-tile"><div class="l">Trend</div><div class="v">{row['trend']}</div></div>
    <div style="height:10px"></div>
    <div class="stat-tile"><div class="l">Recent volume</div><div class="v">~{row['recent_avg']:.0f}/mo</div></div>
    <div style="height:10px"></div>
    <div class="stat-tile"><div class="l">Positive</div><div class="v">{row['recent_pos']}%</div></div>
    """, unsafe_allow_html=True)

# ---------- Product drill-down ----------
st.markdown(f'<div class="section">Top products — {sel}</div>', unsafe_allow_html=True)
pmb = pm[pm["brand_name"] == sel]
prod = (pmb.groupby("product_name")
           .apply(lambda d: pd.Series({
               "reviews": int(d["volume"].sum()),
               "pos": round((d["pct_positive"] * d["volume"]).sum() / d["volume"].sum(), 1),
               "rating": round((d["avg_rating"] * d["volume"]).sum() / d["volume"].sum(), 2)}))
           .reset_index()
           .nlargest(8, "reviews")
           .sort_values("reviews"))
labels = [p if len(p) <= 40 else p[:38] + "…" for p in prod["product_name"]]
figp = go.Figure(go.Bar(
    x=prod["reviews"], y=labels, orientation="h", marker_color=BRAND,
    customdata=prod[["pos", "rating"]].values,
    hovertemplate="<b>%{y}</b><br>%{x} reviews · %{customdata[0]}%% positive · ★%{customdata[1]}<extra></extra>"))
figp.update_layout(
    height=max(240, 34 * len(prod)), margin=dict(l=10, r=10, t=6, b=6),
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=INK_SUB, size=12),
    xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", color=INK_MUTE, title="reviews"),
    yaxis=dict(color=INK))
st.plotly_chart(figp, use_container_width=True, config={"displayModeBar": False})

# ---------- Sentiment check ----------
st.markdown('<div class="section">Sentiment check</div>', unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1])
txt = col_in.text_input("s", "This serum completely transformed my skin!", label_visibility="collapsed")
if col_btn.button("Analyze", use_container_width=True):
    r = None
    try:
        from sentiment import predict_sentiment
        r = predict_sentiment(txt)
    except Exception:
        for ex in examples:                      # fallback: cau da phan tich san
            if ex["text"].strip().lower() == txt.strip().lower():
                r = ex
                break
    if r:
        tone = {"positive": "#22c55e", "neutral": "#f59e0b", "negative": "#ef4444"}
        c = tone.get(r["label"], BRAND)
        st.markdown(
            f"<div class='card' style='--c:{c}'>"
            f"<span class='pill' style='--c:{c}'>{r['label'].upper()}</span>"
            f"<span style='color:{INK_SUB};margin-left:.6rem'>confidence "
            f"<b style='color:{INK}'>{r['score']}</b> · engine: {r.get('engine','cache')}</span></div>",
            unsafe_allow_html=True)
    elif examples:
        st.info("Sentiment model not loaded — pre-analyzed examples (demo fallback):")
        for ex in examples:
            st.write(f"- **{ex['label'].upper()}** ({ex['score']}) — {ex['text']}")
    else:
        st.warning("Sentiment model not available.")

st.markdown(
    f"<div style='color:{INK_MUTE};font-size:.75rem;margin-top:2.5rem;"
    f"border-top:1px solid {BORDER};padding-top:1rem'>"
    "Source: Sephora product reviews (2021–2023) with real submission dates · "
    "trends and forecasts computed from actual review volume — no synthetic data.</div>",
    unsafe_allow_html=True)
