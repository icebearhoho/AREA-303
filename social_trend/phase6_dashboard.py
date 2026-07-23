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
    "RESTOCK": {"c": "#22c55e", "icon": "↑", "label": "STOCK UP"},
    "WATCH":   {"c": "#f59e0b", "icon": "→", "label": "MONITOR"},
    "REDUCE":  {"c": "#ef4444", "icon": "↓", "label": "REDUCE"},
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
  .card-kw {{ color:{INK}; font-weight:700; font-size:1.05rem; margin:.55rem 0 .35rem; }}
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

        rows = [{"keyword": k, "date": pd.Timestamp(p["date"]), "interest": p["interest"]}
                for k, ser in d["series"].items() for p in ser]
        return (df(d["alerts"]), df(d["keyword_trends"]), pd.DataFrame(rows),
                d["meta"], d.get("sentiment_examples", []), "Demo · JSON")

    # ---- LIVE MODE: doc parquet goc ----
    alerts = pd.read_parquet(O / "keyword_alerts.parquet")
    trends = pd.read_parquet(O / "keyword_trends.parquet")
    series = pd.read_parquet(config.GOOGLE_TRENDS_PARQUET)[["keyword", "date", "interest"]]
    meta = {
        "keywords": int(trends.shape[0]),
        "weeks": int(series["date"].nunique()),
        "span": f'{series["date"].min():%b %Y} - {series["date"].max():%b %Y}',
        "rising": int(trends["rising"].sum()),
        "sentiment_f1": 0.69,
    }
    return alerts, trends, series, meta, [], "Live · parquet"


alerts, trends, series, meta, examples, mode = load()

# ---------- Header ----------
st.markdown(f"""
<div>
  <span class="mode-chip">{mode}</span>
  <div class="eyebrow">AREA 303 · Track 2 · Feature #08</div>
  <div class="app-title">Social Trend Analyzer</div>
  <div class="app-sub">Spot rising product searches from Google Trends — restock guidance for sellers.</div>
</div>
""", unsafe_allow_html=True)

# ---------- KPI ----------
st.markdown(f"""
<div class="kpi-row" style="margin-top:1.6rem">
  <div class="kpi"><div class="kpi-label">Keywords tracked</div>
    <div class="kpi-value">{meta['keywords']}</div><div class="kpi-note">beauty + fashion</div></div>
  <div class="kpi"><div class="kpi-label">Weeks of data</div>
    <div class="kpi-value">{meta['weeks']}</div><div class="kpi-note">{meta['span']}</div></div>
  <div class="kpi"><div class="kpi-label">Rising now</div>
    <div class="kpi-value" style="color:{BRAND}">{meta['rising']}</div><div class="kpi-note">momentum &ge; 5</div></div>
  <div class="kpi"><div class="kpi-label">Sentiment engine</div>
    <div class="kpi-value">F1 {meta.get('sentiment_f1','-')}</div><div class="kpi-note">XLM-RoBERTa</div></div>
</div>
""", unsafe_allow_html=True)

# ---------- Alert cards ----------
st.markdown('<div class="section">Search-trend signals</div>', unsafe_allow_html=True)
cards = ""
for _, a in alerts.iterrows():
    s = STATUS[a["alert"]]
    cards += (
        f"<div class='card' style='--c:{s['c']}'>"
        f"<span class='pill'>{s['icon']} {s['label']}</span>"
        f"<div class='card-kw'>{a['keyword']} <span style='color:{INK_MUTE};font-weight:400;font-size:.8rem'>· {a['group']}</span></div>"
        f"<div class='card-metrics'><b>{a['trend']}</b> · momentum {a['momentum']:+.0f} · "
        f"interest <b>{a['recent_interest']:.0f}</b></div>"
        f"<div class='card-hint'>{a['action']}</div></div>"
    )
st.markdown(f"<div class='alert-row'>{cards}</div>", unsafe_allow_html=True)

# ---------- Search-interest chart ----------
st.markdown('<div class="section">Search interest over time</div>', unsafe_allow_html=True)
order = trends.sort_values("momentum", ascending=False)
sel = st.selectbox("Keyword", order["keyword"].tolist(),
                   format_func=lambda k: f"{k} · {order.set_index('keyword').loc[k, 'trend']}",
                   label_visibility="collapsed")
d = series[series["keyword"] == sel].sort_values("date")
row = trends.set_index("keyword").loc[sel]

col_chart, col_stats = st.columns([3, 1])
with col_chart:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=d["date"], y=d["interest"], mode="lines",
        line=dict(color=BRAND, width=2.5), fill="tozeroy", fillcolor="rgba(129,140,248,0.13)",
        hovertemplate="%{x|%d %b %Y}<br>interest <b>%{y}</b><extra></extra>"))
    fig.update_layout(
        height=330, margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified", font=dict(color=INK_SUB, size=12),
        xaxis=dict(showgrid=False, color=INK_MUTE),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                   color=INK_MUTE, range=[0, 105], title="Google Trends interest"))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
with col_stats:
    st.markdown(f"""
    <div class="stat-tile"><div class="l">Trend</div><div class="v">{row['trend']}</div></div>
    <div style="height:10px"></div>
    <div class="stat-tile"><div class="l">Momentum</div><div class="v">{row['momentum']:+.0f}</div></div>
    <div style="height:10px"></div>
    <div class="stat-tile"><div class="l">Recent interest</div><div class="v">{row['recent_interest']:.0f}</div></div>
    """, unsafe_allow_html=True)

# ---------- Sentiment check (separate tool) ----------
st.markdown('<div class="section">Sentiment check <span style="color:#6b7280;font-weight:400;font-size:.8rem">— standalone tool</span></div>', unsafe_allow_html=True)
col_in, col_btn = st.columns([5, 1])
txt = col_in.text_input("s", "This lipstick is amazing, best purchase ever!", label_visibility="collapsed")
if col_btn.button("Analyze", use_container_width=True):
    r = None
    try:
        from sentiment import predict_sentiment
        r = predict_sentiment(txt)
    except Exception:
        for ex in examples:
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
    "Source: Google Trends weekly search interest (beauty + fashion keywords) — real demand signal, "
    "no forecasting model. Sentiment engine (XLM-RoBERTa) offered as a standalone tool.</div>",
    unsafe_allow_html=True)
