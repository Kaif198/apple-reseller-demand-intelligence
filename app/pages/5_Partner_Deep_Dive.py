"""
Page 5 — Partner Deep Dive
Apple Reseller Channel Intelligence Platform
Author: Mohammed Kaif Ahmed
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Partner Deep Dive · Apple Demand Planner",
                   page_icon="", layout="wide")
st.write(
    '<style>@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap");</style>',
    unsafe_allow_html=True
)

css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "apple_theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from src.utils.helpers import (load_products, load_partners, load_actuals,
                                load_forecasts, load_order_book, load_npi_tracker,
                                load_alerts, format_eur, format_pct)
from src.utils.apple_charts import (product_mix_donut, apple_chart_layout,
                                     forecast_line_chart)
from src.analytics.partner_analytics import (partner_overview, partner_revenue_trend,
                                               partner_product_mix, generate_partner_insights)
from app.components.kpi_cards import render_kpi_row, insight_box, section_header, render_sidebar
from app.components.alerts import render_alert_feed
from app.components.charts import show_chart
import plotly.graph_objects as go

@st.cache_data(ttl=300)
def _load():
    return (load_products(), load_partners(), load_actuals(), load_forecasts(),
            load_order_book(), load_npi_tracker(), load_alerts())

try:
    products, partners, actuals, forecasts, order_book, npi, alerts = _load()
except FileNotFoundError:
    st.error("⚠️  Run `python src/data_generator.py` first."); st.stop()

with st.sidebar:
    render_sidebar()


st.markdown('<div class="page-title">Partner Deep Dive</div>', unsafe_allow_html=True)

# ─── Partner Selector ─────────────────────────────────────────────────────────
partner_names = sorted(partners["partner_name"].tolist())
sel_partner = st.selectbox("Select Partner", partner_names, key="partner_sel")
sel_pid = partners[partners["partner_name"] == sel_partner]["partner_id"].values[0]
tier    = partners[partners["partner_name"] == sel_partner]["partner_tier"].values[0]
country = partners[partners["partner_name"] == sel_partner]["country"].values[0]

tier_badge_cls = {"Platinum": "badge-blue", "Gold": "badge-amber", "Silver": "badge-grey"}
tier_html = f'<span class="badge {tier_badge_cls.get(tier,"badge-grey")}">{tier}</span>'
st.markdown(
    f'<div style="margin:8px 0 20px 0">'
    f'{tier_html}&nbsp;&nbsp;'
    f'<span style="color:#6E6E73;font-size:14px">Country: {country}</span>'
    f'</div>',
    unsafe_allow_html=True
)

# ─── KPI Row ─────────────────────────────────────────────────────────────────
kpis = partner_overview(actuals, alerts, sel_pid)
product_mix = partner_product_mix(actuals, products, sel_pid)

render_kpi_row([
    {"label": "Revenue YTD",    "value": format_eur(kpis.get("ytd_revenue", 0)),
     "delta": kpis.get("revenue_delta", 0)},
    {"label": "In-Stock Rate",  "value": f"{kpis.get('in_stock_rate', 0):.1f}%",
     "delta": None, "context": f"Avg {kpis.get('avg_wos', 0):.1f} wks of supply"},
    {"label": "Fulfilment Rate","value": f"{kpis.get('fulfil_rate', 0):.1f}%",
     "delta": None},
    {"label": "Open Alerts",    "value": str(kpis.get("open_alerts", 0)),
     "context": f"{kpis.get('critical_alerts', 0)} critical",
     "delta_good_direction": "negative"},
])
st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

# ─── Tab Navigation ───────────────────────────────────────────────────────────
tabs = st.tabs(["📊 Overview", "📈 Demand", "📦 Order Book", "🚀 NPI", "⚠️ Alerts"])

# ═══════════ TAB 1: OVERVIEW ═══════════
with tabs[0]:
    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        section_header("Revenue Trend — Last 2 Years")
        rev_trend = partner_revenue_trend(actuals, sel_pid, weeks=104)
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=rev_trend["date"], y=rev_trend["revenue"],
            mode="lines", name="Revenue",
            line=dict(color="#1D1D1F", width=2),
            fill="tozeroy", fillcolor="rgba(29,29,31,0.05)",
        ))
        apple_chart_layout(fig_rev, height=340)
        fig_rev.update_layout(yaxis=dict(tickprefix="€"))
        show_chart(fig_rev)

    with col2:
        section_header("Product Family Mix")
        fig_mix = product_mix_donut(product_mix,
                                     center_text=format_eur(kpis.get("ytd_revenue", 0)),
                                     height=340)
        show_chart(fig_mix)

    section_header("Key Insights")
    insights = generate_partner_insights(sel_partner, kpis, product_mix)
    for bullet in insights:
        insight_box(bullet, icon="")

# ═══════════ TAB 2: DEMAND ═══════════
with tabs[1]:
    section_header(f"Demand Actuals & Forecast — {sel_partner}")

    p_acts = actuals[actuals["partner_id"] == sel_pid]
    weekly = p_acts.groupby("date").agg(units_sold=("units_sold","sum")).reset_index().sort_values("date").tail(52)

    p_fcast = forecasts[(forecasts["partner_id"] == sel_pid) &
                          (forecasts["forecast_model"] == "Ensemble")]
    weekly_fc = p_fcast.groupby("date").agg(
        forecast_units=("forecast_units","sum"),
        forecast_lower=("forecast_lower","sum"),
        forecast_upper=("forecast_upper","sum"),
    ).reset_index().sort_values("date")

    fig_dem = forecast_line_chart(weekly, weekly_fc, height=420)
    show_chart(fig_dem)

    # Accuracy by product family
    section_header("Demand by Product Family")
    p_acts_fam = p_acts.merge(products[["product_id","product_family"]], on="product_id", how="left")
    fam_weekly = p_acts_fam.groupby(["date","product_family"]).agg(
        units_sold=("units_sold","sum")).reset_index()

    from src.utils.apple_charts import APPLE_COLORS
    fig_fam = go.Figure()
    for fam, color in APPLE_COLORS.items():
        fam_data = fam_weekly[fam_weekly["product_family"] == fam].sort_values("date").tail(26)
        if fam_data.empty: continue
        fig_fam.add_trace(go.Scatter(
            x=fam_data["date"], y=fam_data["units_sold"],
            name=fam, line=dict(color=color, width=2), mode="lines"
        ))
    apple_chart_layout(fig_fam, height=360)
    show_chart(fig_fam)

# ═══════════ TAB 3: ORDER BOOK ═══════════
with tabs[2]:
    section_header(f"Order Book — {sel_partner}")
    p_orders = order_book[order_book["partner_id"] == sel_pid].copy()
    p_orders = p_orders.merge(products[["product_id","product_name","product_family"]], on="product_id", how="left")

    if p_orders.empty:
        st.info("No open orders for this partner.")
    else:
        chase_val = p_orders[p_orders["chase_opportunity"]]["chase_revenue_potential"].sum()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Open Lines", len(p_orders[p_orders["status"].isin(["Open","Partially Fulfilled"])]))
        with c2:
            st.metric("Chase Opportunity", format_eur(chase_val))
        with c3:
            at_risk = len(p_orders[p_orders["status"] == "At Risk"])
            st.metric("At Risk Lines", at_risk)

        st.markdown("<div style='margin:12px 0'></div>", unsafe_allow_html=True)

        tbl = """<div class="apple-table-wrap"><table class="apple-table">
<thead><tr><th>Order ID</th><th>Product</th><th>Ordered</th>
<th>Confirmed</th><th>Shipped</th><th>Status</th><th>Chase</th></tr></thead><tbody>"""
        status_cls = {"Open":"badge-blue","Partially Fulfilled":"badge-amber",
                      "At Risk":"badge-red","Shipped":"badge-green"}
        for _, r in p_orders.head(20).iterrows():
            chase_str = format_eur(r["chase_revenue_potential"]) if r["chase_opportunity"] else "—"
            cls = status_cls.get(r["status"], "badge-grey")
            tbl += f"""<tr>
<td style="color:#6E6E73;font-size:12px">{r['order_id']}</td>
<td style="font-size:13px">{str(r.get('product_name',''))[:30]}</td>
<td>{int(r['units_ordered']):,}</td>
<td>{int(r['units_confirmed']):,}</td>
<td>{int(r['units_shipped']):,}</td>
<td><span class="badge {cls}">{r['status']}</span></td>
<td style="color:#0071E3;font-weight:600">{chase_str}</td>
</tr>"""
        tbl += "</tbody></table></div>"
        st.markdown(tbl, unsafe_allow_html=True)

# ═══════════ TAB 4: NPI ═══════════
with tabs[3]:
    section_header(f"NPI Performance — {sel_partner}")
    p_npi = npi[npi["partner_id"] == sel_pid].copy()
    p_npi = p_npi.merge(products[["product_id","product_name"]], on="product_id", how="left")

    if p_npi.empty:
        st.info("No NPI data for this partner.")
    else:
        tbl = """<div class="apple-table-wrap"><table class="apple-table">
<thead><tr><th>Product</th><th>Week</th><th>Plan</th><th>Actual</th>
<th>Velocity vs Plan</th><th>Sell-Through</th><th>Status</th></tr></thead><tbody>"""
        for _, r in p_npi.sort_values(["product_id","week_number"]).head(30).iterrows():
            vel_color = "#34C759" if r["velocity_vs_plan"]>=0.9 else ("#FF9500" if r["velocity_vs_plan"]>=0.7 else "#FF3B30")
            rag_cls = {"Green":"badge-green","Amber":"badge-amber","Red":"badge-red"}.get(r["risk_flag"],"badge-grey")
            tbl += f"""<tr>
<td style="font-size:13px">{str(r.get('product_name',''))[:30]}</td>
<td style="color:#6E6E73">Wk {int(r['week_number'])}</td>
<td>{int(r['units_planned']):,}</td>
<td style="font-weight:600">{int(r['units_actual']):,}</td>
<td style="font-weight:600;color:{vel_color}">{r['velocity_vs_plan']*100:.1f}%</td>
<td>{r['sell_through_rate']*100:.1f}%</td>
<td><span class="badge {rag_cls}">{r['risk_flag']}</span></td>
</tr>"""
        tbl += "</tbody></table></div>"
        st.markdown(tbl, unsafe_allow_html=True)

# ═══════════ TAB 5: ALERTS ═══════════
with tabs[4]:
    section_header(f"Open Alerts — {sel_partner}")
    p_alerts = alerts[(alerts["partner_id"] == sel_pid) & (alerts["status"] == "Open")]
    if p_alerts.empty:
        insight_box(f"✅ No open alerts for {sel_partner} — operations are on track.", icon="")
    else:
        render_alert_feed(p_alerts)
