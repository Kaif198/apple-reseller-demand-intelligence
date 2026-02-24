"""
Page 4 — Risk & Alerts
Apple Reseller Channel Intelligence Platform
Author: Mohammed Kaif Ahmed
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Risk & Alerts · Apple Demand Planner",
                   page_icon="", layout="wide")
css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "apple_theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from src.utils.helpers import (load_products, load_partners, load_actuals,
                                load_alerts, format_eur)
from src.utils.apple_charts import risk_matrix_scatter, apple_chart_layout
from src.analytics.alert_engine import get_alert_kpis, build_risk_matrix
from app.components.kpi_cards import render_kpi_row, insight_box, section_header, render_sidebar
from app.components.alerts import render_alert_feed
from app.components.charts import show_chart
import plotly.graph_objects as go

@st.cache_data(ttl=300)
def _load():
    return load_products(), load_partners(), load_actuals(), load_alerts()

try:
    products, partners, actuals, alerts = _load()
except FileNotFoundError:
    st.error("⚠️  Run `python src/data_generator.py` first."); st.stop()

with st.sidebar:
    render_sidebar()


st.markdown('<div class="page-title">Risk & Alerts</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Early alert feed · Demand anomalies · Inventory risk matrix · Revenue at risk</div>',
            unsafe_allow_html=True)

# ─── KPI Row ─────────────────────────────────────────────────────────────────
kpis = get_alert_kpis(alerts)

render_kpi_row([
    {"label": "Open Alerts",    "value": str(kpis["total_open"]),
     "context": "Require action"},
    {"label": "🔴 Critical",   "value": str(kpis["critical"]),
     "context": "Immediate action required", "delta_good_direction": "negative"},
    {"label": "🟡 Warning",    "value": str(kpis["warning"]),
     "context": "Monitor and plan response"},
    {"label": "ℹ️  Info",      "value": str(kpis["info"]),
     "context": "Awareness items"},
    {"label": "Revenue at Risk","value": format_eur(kpis["revenue_at_risk"]),
     "context": "If open alerts unaddressed", "delta_good_direction": "negative"},
])
st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

# ─── Two-Column: Alert Feed + Risk Matrix ─────────────────────────────────────
col1, col2 = st.columns([2, 3], gap="large")

with col1:
    section_header("Alert Feed")
    # Severity filter
    sev_filter = st.multiselect(
        "Filter by severity",
        options=["Critical", "Warning", "Info"],
        default=["Critical", "Warning", "Info"],
        key="sev_filt"
    )
    filtered_alerts = alerts[alerts["severity"].isin(sev_filter)]
    render_alert_feed(filtered_alerts, max_alerts=15)

with col2:
    section_header("Risk Matrix — Likelihood vs Revenue Impact")

    risk_df = build_risk_matrix(actuals, products, partners)
    if not risk_df.empty:
        fig_risk = risk_matrix_scatter(risk_df, height=480)
        show_chart(fig_risk)

        insight_box(
            f"<strong>Risk Matrix Insight:</strong> The top-right 'Escalate' quadrant contains "
            f"<strong>{len(risk_df[risk_df['likelihood']>0.5])}</strong> high-likelihood, high-impact "
            f"SKU-partner combinations. These should be the first items reviewed in the weekly "
            f"operations call. Combined at-risk revenue: "
            f"<strong>{format_eur(risk_df[risk_df['likelihood']>0.5]['revenue_impact'].sum())}</strong>."
        )

# ─── Top 10 Assignable Actions ────────────────────────────────────────────────
section_header("Top 10 Assignable Actions — Ranked by Revenue Impact")

open_alerts = alerts[alerts["status"] == "Open"].copy()
open_alerts = open_alerts.merge(products[["product_id","product_name","product_family"]], on="product_id", how="left")
open_alerts = open_alerts.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")
top10 = open_alerts.sort_values("revenue_impact", ascending=False).head(10)

sev_cls = {"Critical": "badge-red", "Warning": "badge-amber", "Info": "badge-blue"}

tbl = """<div class="apple-table-wrap"><table class="apple-table">
<thead><tr><th>#</th><th>Severity</th><th>Partner</th><th>Product</th>
<th>Alert Type</th><th>Recommended Action</th><th>Revenue Impact</th></tr></thead><tbody>"""
for rank, (_, row) in enumerate(top10.iterrows(), 1):
    cls = sev_cls.get(row["severity"], "badge-blue")
    tbl += f"""<tr>
<td style="font-weight:700;color:#0071E3">{rank}</td>
<td><span class="badge {cls}">{row['severity']}</span></td>
<td style="font-weight:500">{row.get('partner_name', '—')}</td>
<td style="color:#6E6E73">{str(row.get('product_name','—'))[:30]}</td>
<td>{row['alert_type']}</td>
<td style="font-size:13px;color:#6E6E73">{str(row['recommended_action'])[:80]}…</td>
<td style="font-weight:600;color:#FF3B30">{format_eur(row['revenue_impact'])}</td>
</tr>"""
tbl += "</tbody></table></div>"
st.markdown(tbl, unsafe_allow_html=True)

insight_box(
    f"<strong>Action Summary:</strong> If we action the top 10 alerts this week, we protect "
    f"approximately <strong>{format_eur(top10['revenue_impact'].sum())}</strong> in revenue and "
    f"avoid excess inventory carrying costs. The highest-priority item is the Currys UK iPhone 16 Pro "
    f"low-stock alert (€890K at risk) — allocation increase recommended by EOD."
)

# ─── Alert Resolution Trend ───────────────────────────────────────────────────
section_header("Alert Volume Trend — Last 8 Weeks")

alerts["week"] = pd.to_datetime(alerts["date_generated"]).dt.to_period("W").dt.start_time
trend = alerts.groupby(["week","status"]).size().unstack(fill_value=0).reset_index()

fig_trend = go.Figure()
if "Open" in trend.columns:
    fig_trend.add_trace(go.Scatter(x=trend["week"], y=trend["Open"], mode="lines",
                                   name="Open", line=dict(color="#FF3B30", width=2)))
if "Resolved" in trend.columns:
    fig_trend.add_trace(go.Scatter(x=trend["week"], y=trend["Resolved"], mode="lines",
                                   name="Resolved", line=dict(color="#34C759", width=2)))
if "In Progress" in trend.columns:
    fig_trend.add_trace(go.Scatter(x=trend["week"], y=trend["In Progress"], mode="lines",
                                   name="In Progress", line=dict(color="#FF9500", width=2,
                                                                  dash="dash")))
apple_chart_layout(fig_trend, height=300)
show_chart(fig_trend)
