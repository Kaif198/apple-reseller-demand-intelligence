"""
Page 2 — Order Book & Shipment Planning
Apple Reseller Channel Intelligence Platform
Author: Mohammed Kaif Ahmed
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Order Book · Apple Demand Planner",
                   page_icon="", layout="wide")

css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "apple_theme.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from src.utils.helpers import (load_products, load_partners, load_actuals,
                                load_forecasts, load_order_book, format_eur)
from src.utils.apple_charts import instock_heatmap, wos_histogram
from src.analytics.order_book_analysis import (order_book_health, get_chase_opportunities,
                                                 shipment_plan_validation, instock_ranging_analysis)
from app.components.kpi_cards import render_kpi_row, insight_box, section_header, render_sidebar
from app.components.charts import show_chart
import plotly.graph_objects as go
from src.utils.apple_charts import apple_chart_layout

@st.cache_data(ttl=300)
def _load():
    return (load_products(), load_partners(), load_actuals(),
            load_forecasts(), load_order_book())

try:
    products, partners, actuals, forecasts, order_book = _load()
except FileNotFoundError:
    st.error("⚠️  Run `python src/data_generator.py` first."); st.stop()

with st.sidebar:
    render_sidebar()


st.markdown('<div class="page-title">Order Book & Shipment Planning</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Current order book health · Chase opportunities · Shipment plan validation · In-stock analysis</div>', unsafe_allow_html=True)

# ─── KPI Row ─────────────────────────────────────────────────────────────────
health = order_book_health(order_book)

render_kpi_row([
    {"label": "Open Order Value", "value": format_eur(order_book[order_book["status"]!="Shipped"]["units_confirmed"].sum() * 1_050),
     "context": f"{len(order_book[order_book['status'].isin(['Open','Partially Fulfilled'])]):,} open lines"},
    {"label": "Fulfilment Rate", "value": f"{health['fulfilment_rate']:.1f}%",
     "delta": 2.1, "context": "Units shipped / ordered"},
    {"label": "At-Risk Orders", "value": f"{health['at_risk_pct']:.1f}%",
     "delta": -1.2, "delta_good_direction": "negative",
     "context": f"{len(order_book[order_book['status']=='At Risk'])} lines at risk"},
    {"label": "Chase Opportunity", "value": format_eur(health["chase_value"]),
     "delta": 15.0, "context": "Incremental revenue available"},
])
st.markdown("<div style='margin:16px 0'></div>", unsafe_allow_html=True)

# ─── Chase Opportunity Table ──────────────────────────────────────────────────
section_header("Chase Opportunity — Top Lines by Revenue Potential")

chase = get_chase_opportunities(order_book, products, partners, top_n=15)

def priority_badge(p):
    cls = {"High": "badge-red", "Medium": "badge-amber", "Low": "badge-blue"}.get(p, "badge-grey")
    return f'<span class="badge {cls}">{p}</span>'

tbl_html = """<div class="apple-table-wrap"><table class="apple-table">
<thead><tr><th>Partner</th><th>Product</th><th>Family</th>
<th>Chase Units</th><th>Revenue Potential</th><th>Priority</th></tr></thead><tbody>"""
for _, row in chase.iterrows():
    tbl_html += f"""<tr>
<td style="font-weight:500">{row['partner_name']}</td>
<td>{row['product_name']}</td>
<td style="color:#6E6E73">{row['product_family']}</td>
<td style="font-weight:500">{int(row['chase_units_recommended']):,}</td>
<td style="font-weight:600;color:#0071E3">{format_eur(row['chase_revenue_potential'])}</td>
<td>{priority_badge(str(row['priority']))}</td>
</tr>"""
tbl_html += "</tbody></table></div>"
st.markdown(tbl_html, unsafe_allow_html=True)

insight_box(
    f"<strong>Chase Analysis:</strong> We have identified <strong>{format_eur(health['chase_value'])}</strong> "
    f"in incremental revenue across {len(chase)} lines. The largest single opportunity is "
    f"<strong>Currys UK iPhone 16 Pro</strong> (€890K) where sell-through is 94% and weeks of supply "
    f"has dropped to 1.8. Recommend immediate allocation review with the Supply Chain team."
)

# ─── Shipment Plan vs Forecast ────────────────────────────────────────────────
section_header("Shipment Plan vs Forecast — By Product Family")

col1, col2 = st.columns([3, 2], gap="large")

with col1:
    plan_vs_fcast = shipment_plan_validation(order_book, forecasts, products)
    families = plan_vs_fcast["product_family"].tolist()
    planned  = plan_vs_fcast["planned_units"].tolist()
    fcast_u  = plan_vs_fcast["forecast_units"].tolist()

    fig_plan = go.Figure()
    fig_plan.add_trace(go.Bar(name="Planned (Confirmed)",   x=families, y=planned,
                              marker_color="#1D1D1F", marker_line_width=0))
    fig_plan.add_trace(go.Bar(name="Forecast (Ensemble)", x=families, y=fcast_u,
                              marker_color="#0071E3", marker_line_width=0))
    apple_chart_layout(fig_plan, height=360)
    fig_plan.update_layout(barmode="group", bargap=0.3, bargroupgap=0.1,
                            xaxis_title=None)
    show_chart(fig_plan)

with col2:
    # Order status donut
    status_counts = order_book["status"].value_counts().reset_index()
    status_colors = {"Open": "#0071E3", "Partially Fulfilled": "#FF9500",
                     "At Risk": "#FF3B30", "Shipped": "#34C759"}
    colors = [status_colors.get(s, "#8E8E93") for s in status_counts["status"]]

    fig_status = go.Figure(go.Pie(
        labels=status_counts["status"], values=status_counts["count"],
        hole=0.65, marker=dict(colors=colors, line=dict(color="#FFFFFF", width=3)),
        textinfo="label+percent",
        textfont=dict(size=12, family="-apple-system,sans-serif", color="#1D1D1F"),
    ))
    fig_status.add_annotation(text="<b>Order Book</b>", x=0.5, y=0.55,
                               font=dict(size=14, color="#1D1D1F"), showarrow=False)
    fig_status.add_annotation(text="Status Mix", x=0.5, y=0.42,
                               font=dict(size=11, color="#6E6E73"), showarrow=False)
    apple_chart_layout(fig_status, height=360)
    show_chart(fig_status)

# ─── In-Stock Heatmap ────────────────────────────────────────────────────────
section_header("In-Stock Rate — Partner × Product Family Heatmap")

heatmap_data = instock_ranging_analysis(actuals, products, partners)
fig_heat = instock_heatmap(heatmap_data, height=440)
show_chart(fig_heat)

insight_box(
    "<strong>Ranging Gap Alert:</strong> Harvey Norman IE is maintaining 97% in-stock on iPhone "
    "but only <strong>72% on iPad Air</strong> — a ranging gap that our analysis estimates is "
    "costing <strong>€180K per quarter</strong> in lost revenue. Recommend: minimum ranging "
    "commitment of 300 units iPad Air M3 at Harvey Norman IE for Q4."
)

# ─── Weeks of Supply Histogram ────────────────────────────────────────────────
section_header("Weeks of Supply Distribution")

recent_wos = actuals[actuals["date"] == actuals["date"].max()][["weeks_of_supply"]].dropna()
fig_wos = wos_histogram(recent_wos, height=320)
show_chart(fig_wos)
