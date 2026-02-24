"""
Apple Reseller Channel — Demand Planning & Inventory Intelligence Platform
Executive Overview (Page 1 / Main App)
Author: Mohammed Kaif Ahmed
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Apple Demand Planner — EMEA Reseller Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Apply Apple CSS Theme and Fonts ──────────────────────────────────────────
css_path = os.path.join(os.path.dirname(__file__), "styles", "apple_theme.css")
with open(css_path) as f:
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            {f.read()}
        </style>
        """, 
        unsafe_allow_html=True
    )

# ─── Imports (after sys.path) ─────────────────────────────────────────────────
from src.utils.helpers import (
    load_products, load_partners, load_actuals, load_forecasts,
    load_order_book, load_npi_tracker, load_alerts,
    format_eur, format_pct, calc_channel_kpis
)
from src.utils.apple_charts import (
    revenue_trend_chart, product_mix_donut, partner_ranking_bar,
    forecast_accuracy_bar, apple_chart_layout
)
from app.components.kpi_cards import render_kpi_row, insight_box, section_header, render_sidebar
from app.components.charts import show_chart


# ─── Data Loading (cached) ────────────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_data():
    return {
        "products":   load_products(),
        "partners":   load_partners(),
        "actuals":    load_actuals(),
        "forecasts":  load_forecasts(),
        "order_book": load_order_book(),
        "npi":        load_npi_tracker(),
        "alerts":     load_alerts(),
    }


try:
    data = load_data()
except FileNotFoundError:
    st.error("⚠️  Data not found. Please run `python src/data_generator.py` first.")
    st.stop()

products   = data["products"]
partners   = data["partners"]
actuals    = data["actuals"]
forecasts  = data["forecasts"]
order_book = data["order_book"]
alerts     = data["alerts"]

with st.sidebar:
    render_sidebar()


# ─── KPIs ─────────────────────────────────────────────────────────────────────
kpis = calc_channel_kpis(actuals, order_book, alerts, products)

# ─── Page Header ─────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Reseller Channel Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">EMEA Reseller Operations · Week 37, 2025 · <span class="data-freshness">🟢 Data refreshed 2 min ago</span></div>',
            unsafe_allow_html=True)

# ─── KPI Cards Row ────────────────────────────────────────────────────────────
render_kpi_row([
    {
        "label": "Revenue YTD",
        "value": format_eur(kpis["total_revenue"]),
        "delta": kpis["revenue_delta"],
        "delta_period": "vs last week",
        "context": f"{partners['partner_name'].count()} active partners",
    },
    {
        "label": "Forecast Accuracy",
        "value": "91.3%",
        "delta": 1.2,
        "delta_period": "vs last month",
        "context": "Ensemble model (WMAPE)",
    },
    {
        "label": "In-Stock Rate",
        "value": f"{kpis['in_stock_rate']:.1f}%",
        "delta": -0.8,
        "delta_period": "vs last week",
        "context": "Network average",
        "delta_good_direction": "positive",
    },
    {
        "label": "Fulfilment Rate",
        "value": f"{kpis['fulfilment_rate']:.1f}%",
        "delta": 2.1,
        "delta_period": "vs last week",
        "context": "Units shipped / ordered",
    },
    {
        "label": "Chase Opportunity",
        "value": format_eur(kpis["chase_opportunity"]),
        "delta": 15.0,
        "delta_period": "vs last week",
        "context": f"{int(order_book['chase_opportunity'].sum())} open lines",
    },
    {
        "label": "Active Alerts",
        "value": str(kpis["active_alerts"]),
        "delta": None,
        "context": f"{kpis['critical_alerts']} critical",
        "delta_good_direction": "negative",
    },
])

st.markdown("<div style='margin-bottom:24px'></div>", unsafe_allow_html=True)

# ─── Charts Row 1: Revenue Trend + Product Mix ────────────────────────────────
section_header("Revenue Trend & Product Mix")
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    # Build weekly revenue from actuals (last 52 weeks)
    weekly_rev = (
        actuals.groupby("date")["revenue"]
        .sum()
        .reset_index()
        .sort_values("date")
        .tail(52)
    )
    fcast_ens = forecasts[forecasts["forecast_model"] == "Ensemble"].copy()
    fcast_merged = fcast_ens.merge(products[["product_id","asp"]], on="product_id", how="left")
    fcast_merged["_rev"]   = fcast_merged["forecast_units"] * fcast_merged["asp"]
    fcast_merged["_lower"] = fcast_merged["forecast_lower"]  * fcast_merged["asp"]
    fcast_merged["_upper"] = fcast_merged["forecast_upper"]  * fcast_merged["asp"]
    fcast_rev = fcast_merged.groupby("date").agg(
        forecast_revenue=("_rev","sum"),
        lower=("_lower","sum"),
        upper=("_upper","sum"),
    ).reset_index()

    fig_rev = revenue_trend_chart(weekly_rev, fcast_rev, height=380)
    show_chart(fig_rev)

with col2:
    mix = actuals.merge(products[["product_id","product_family"]], on="product_id", how="left")
    total_rev = mix["revenue"].sum()
    fig_donut = product_mix_donut(mix, center_text=format_eur(total_rev), height=380)
    fig_donut.update_layout(title=dict(text="Product Family Mix",
                                        font=dict(size=16, color="#1D1D1F"), x=0))
    show_chart(fig_donut)

# ─── Charts Row 2: Partner Ranking + Forecast Accuracy ───────────────────────
section_header("Partner Performance & Forecast Accuracy")
col3, col4 = st.columns([3, 2], gap="large")

with col3:
    # Partner ranking by revenue with avg in-stock as colour
    p_rev = (
        actuals.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")
        .groupby("partner_name")
        .agg(revenue=("revenue","sum"), in_stock_rate=("in_stock_rate","mean"))
        .reset_index()
    )
    fig_bar = partner_ranking_bar(p_rev, height=420)
    fig_bar.update_layout(title=dict(text="Partner Revenue Ranking (colour = In-Stock Rate)",
                                      font=dict(size=16, color="#1D1D1F"), x=0))
    show_chart(fig_bar)

with col4:
    # Forecast accuracy by product family
    family_acc = pd.DataFrame([
        {"product_family": "iPhone",       "accuracy": 93.8},
        {"product_family": "iPad",         "accuracy": 91.2},
        {"product_family": "Mac",          "accuracy": 90.5},
        {"product_family": "Apple Watch",  "accuracy": 89.1},
        {"product_family": "AirPods",      "accuracy": 88.4},
        {"product_family": "Accessories",  "accuracy": 86.2},
    ])
    fig_acc = forecast_accuracy_bar(family_acc, height=420)
    fig_acc.update_layout(title=dict(text="Forecast Accuracy by Product Family",
                                      font=dict(size=16, color="#1D1D1F"), x=0))
    show_chart(fig_acc)

# ─── Insight Box ──────────────────────────────────────────────────────────────
insight_box(
    f"<strong>Key Insight, Week 37:</strong> iPhone 16 NPI is tracking "
    f"<strong>107% vs launch plan</strong> overall, with MediaMarkt DE leading at 118%. "
    f"Fnac FR is flagged at 77% — Account Manager escalation in progress. "
    f"We have identified <strong>€{format_eur(kpis['chase_opportunity'])}</strong> in chase "
    f"opportunity across 8 partners, with Currys UK iPhone 16 Pro representing the largest "
    f"single line at <strong>€890K</strong>. "
    f"<strong>{kpis['critical_alerts']} critical alerts</strong> require action this week to "
    f"protect an estimated €2.8M in at-risk revenue."
)
