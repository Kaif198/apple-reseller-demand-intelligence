"""
KPI Cards — HTML/CSS components for metric display.
Author: Mohammed Kaif Ahmed
"""

import streamlit as st
from typing import Optional


def kpi_card(
    label: str,
    value: str,
    delta: Optional[float] = None,
    delta_period: str = "vs last week",
    context: Optional[str] = None,
    delta_good_direction: str = "positive",
) -> str:
    """Generate an Apple-style KPI card HTML string."""
    # Build delta pill
    delta_html = ""
    if delta is not None:
        if delta > 0:
            symbol = "↑"
            cls = "positive" if delta_good_direction == "positive" else "negative"
        elif delta < 0:
            symbol = "↓"
            cls = "negative" if delta_good_direction == "positive" else "positive"
        else:
            symbol = "—"
            cls = "neutral"
        delta_html = (
            f'<span class="kpi-delta {cls}">'
            f'{symbol} {abs(delta):.1f}% {delta_period}</span>'
        )

    context_html = (
        f'<span class="kpi-context">{context}</span>' if context else ""
    )

    return (
        f'<div class="kpi-card">'
        f'<span class="kpi-label">{label}</span>'
        f'<span class="kpi-value">{value}</span>'
        f'{delta_html}'
        f'{context_html}'
        f'</div>'
    )


def render_kpi_row(cards: list) -> None:
    """
    Render a row of KPI cards inside a flex .kpi-row container.
    Each dict: {label, value, delta?, delta_period?, context?, delta_good_direction?}
    """
    cards_html = "".join(
        kpi_card(
            label=c.get("label", ""),
            value=c.get("value", "—"),
            delta=c.get("delta"),
            delta_period=c.get("delta_period", "vs last week"),
            context=c.get("context"),
            delta_good_direction=c.get("delta_good_direction", "positive"),
        )
        for c in cards
    )
    st.markdown(f'<div class="kpi-row">{cards_html}</div>', unsafe_allow_html=True)


def insight_box(text: str, icon: str = "💡") -> None:
    """Render an Apple-style insight callout box."""
    label_html = (
        f'<div class="insight-label"><span>{icon}</span> Key Insight</div>'
        if icon else ""
    )
    st.markdown(
        f'<div class="insight-box">{label_html}{text}</div>',
        unsafe_allow_html=True,
    )


def section_header(title: str) -> None:
    """Render a section divider header."""
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def page_header(title: str, subtitle: str = None, updated: str = None) -> None:
    """Render Apple-style page header with optional subtitle and freshness indicator."""
    subtitle_html = (
        f'<p class="page-header-subtitle">{subtitle}</p>' if subtitle else ""
    )
    meta_html = (
        f'<div class="page-header-meta">'
        f'<span class="meta-dot"></span>Data updated: {updated}</div>'
    ) if updated else ""

    st.markdown(
        f'<div class="page-header">'
        f'<h1 class="page-header-title">{title}</h1>'
        f'{subtitle_html}{meta_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def chart_container(title: str, subtitle: str = None) -> None:
    """Render chart section title (call before st.plotly_chart)."""
    subtitle_html = (
        f'<span class="chart-subtitle">{subtitle}</span>' if subtitle else ""
    )
    st.markdown(
        f'<span class="chart-title">{title}</span>{subtitle_html}',
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """
    Render the shared app sidebar:  logo + clean nav links (no emojis).
    Call this inside `with st.sidebar:` at the top of every page.
    """
    import base64, os

    # ── Apple logo ──────────────────────────────────────────────────────────
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "static", "apple_logo.svg"
    )
    try:
        svg_bytes = open(logo_path, "rb").read()
        b64 = base64.b64encode(svg_bytes).decode()
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:10px;padding:4px 0 20px 0;
                        border-bottom:1px solid #E8E8ED;margin-bottom:16px;">
              <img src="data:image/svg+xml;base64,{b64}"
                   style="width:22px;height:22px;opacity:0.85;"/>
              <span style="font-family:-apple-system,BlinkMacSystemFont,'Inter',sans-serif;
                           font-size:15px;font-weight:600;color:#1D1D1F;letter-spacing:-0.2px;">
                Reseller Intelligence
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.markdown(
            '<div class="sidebar-brand">Reseller Intelligence</div>',
            unsafe_allow_html=True,
        )

    # ── Navigation links ─────────────────────────────────────────────────────
    st.page_link("streamlit_app.py",               label="Executive Overview")
    st.page_link("pages/1_Demand_Forecast.py",     label="Demand Forecast")
    st.page_link("pages/2_Order_Book.py",          label="Order Book & Shipments")
    st.page_link("pages/3_NPI_Tracker.py",         label="NPI Launch Tracker")
    st.page_link("pages/4_Risk_Alerts.py",         label="Risk & Alerts")
    st.page_link("pages/5_Partner_Deep_Dive.py",   label="Partner Deep Dive")

    # ── Footer meta ──────────────────────────────────────────────────────────
    st.markdown(
        '<div class="sidebar-week">Week 37, 2025&nbsp;&nbsp;'
        '<span style="color:#8E8E93">·</span>&nbsp;&nbsp;EMEA Reseller Ops'
        '<br><span style="color:#8E8E93;font-size:11px">Data refreshed 2 min ago</span>'
        '</div>'
        '<div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #E8E8ED; '
        'font-family: -apple-system, BlinkMacSystemFont, \'Inter\', sans-serif; '
        'font-size: 11px; color: #8E8E93; line-height: 1.6;">'
        'Created by - Mohammed Kaif Ahmed<br>'
        'Email - kaifahmed6864@gmail.com'
        '</div>',
        unsafe_allow_html=True,
    )
