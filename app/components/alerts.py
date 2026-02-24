"""
Alert Feed Component — renders the styled alert feed for Risk & Alerts page.
Author: Mohammed Kaif Ahmed
"""

import streamlit as st
import pandas as pd
from datetime import datetime


def _severity_class(severity: str) -> str:
    """Map severity string to CSS class."""
    return {
        "Critical": "alert-critical",
        "Warning":  "alert-warning",
        "Info":     "alert-info",
        "Success":  "alert-success",
    }.get(severity, "alert-info")


def alert_card_html(row: pd.Series) -> str:
    """Build HTML for a single Apple-style alert card."""
    ts = row["date_generated"]
    ts_str = (
        ts.strftime("%a %d %b · %H:%M")
        if isinstance(ts, (pd.Timestamp, datetime))
        else str(ts)
    )

    severity_class = _severity_class(row["severity"])
    severity = row["severity"]
    alert_type = row.get("alert_type", "")
    product_id = row.get("product_id", "")
    action = str(row.get("recommended_action", "Review"))[:120]

    impact = row.get("revenue_impact", 0)
    impact_html = (
        f'<span class="alert-rev-impact">€{impact/1e3:.0f}K at risk</span>'
        if impact and impact > 0 else ""
    )

    return f"""
<div class="alert-card {severity_class}">
    <div class="alert-header">
        <span class="alert-title">{product_id}</span>
        <span class="alert-timestamp">{ts_str} · <b>{severity}</b> · {alert_type}</span>
    </div>
    <div class="alert-description">{action}</div>
    <div class="alert-meta">
        <span class="alert-action">Review →</span>
        {impact_html}
    </div>
</div>
"""


def render_alert_feed(alerts_df: pd.DataFrame, max_alerts: int = 20) -> None:
    """Render the full Apple-styled alert feed, sorted by severity then date."""
    severity_order = {"Critical": 0, "Warning": 1, "Info": 2}
    df = alerts_df.copy()
    df["_sev_order"] = df["severity"].map(severity_order).fillna(3)
    df = (
        df[df["status"] == "Open"]
        .sort_values(["_sev_order", "date_generated"], ascending=[True, False])
        .head(max_alerts)
    )

    if df.empty:
        st.markdown(
            '<div class="insight-box">✅ No open alerts — channel is operating normally.</div>',
            unsafe_allow_html=True,
        )
        return

    html = '<div class="alert-feed">'
    for _, row in df.iterrows():
        html += alert_card_html(row)
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
