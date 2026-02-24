"""
Partner Analytics — Deep dive analytics per reseller partner.
Author: Mohammed Kaif Ahmed
"""

import pandas as pd
import numpy as np


def partner_overview(actuals: pd.DataFrame,
                     alerts: pd.DataFrame,
                     partner_id: str) -> dict:
    """Compute partner-level KPI snapshot."""
    p_acts = actuals[actuals["partner_id"] == partner_id]
    if p_acts.empty:
        return {}

    ytd_rev = p_acts["revenue"].sum()

    last_wk  = p_acts["date"].max()
    prev_wk  = last_wk - pd.Timedelta(weeks=1)
    rev_lw   = p_acts[p_acts["date"] == last_wk]["revenue"].sum()
    rev_pw   = p_acts[p_acts["date"] == prev_wk]["revenue"].sum()
    rev_delta = (rev_lw - rev_pw) / max(1, rev_pw) * 100

    avg_in_stock = p_acts["in_stock_rate"].mean() * 100
    avg_wos      = p_acts["weeks_of_supply"].mean()

    fulfil = p_acts["units_shipped"].sum() / max(1, p_acts["units_ordered"].sum()) * 100

    p_alerts = alerts[(alerts["partner_id"] == partner_id) &
                       (alerts["status"] == "Open")]

    return {
        "ytd_revenue":   ytd_rev,
        "revenue_delta": round(rev_delta, 1),
        "in_stock_rate": round(avg_in_stock, 1),
        "avg_wos":       round(avg_wos, 1),
        "fulfil_rate":   round(fulfil, 1),
        "open_alerts":   len(p_alerts),
        "critical_alerts": len(p_alerts[p_alerts["severity"] == "Critical"]),
    }


def partner_revenue_trend(actuals: pd.DataFrame, partner_id: str,
                           weeks: int = 52) -> pd.DataFrame:
    """Return weekly revenue trend for one partner."""
    p = actuals[actuals["partner_id"] == partner_id].copy()
    weekly = p.groupby("date").agg(revenue=("revenue","sum")).reset_index()
    weekly = weekly.sort_values("date").tail(weeks)
    return weekly


def partner_product_mix(actuals: pd.DataFrame, products: pd.DataFrame,
                         partner_id: str) -> pd.DataFrame:
    """Revenue breakdown by product family for one partner."""
    p = actuals[actuals["partner_id"] == partner_id].copy()
    p = p.merge(products[["product_id","product_family"]], on="product_id", how="left")
    mix = p.groupby("product_family").agg(revenue=("revenue","sum")).reset_index()
    return mix.sort_values("revenue", ascending=False)


def generate_partner_insights(partner_name: str,
                               kpis: dict,
                               product_mix: pd.DataFrame) -> list:
    """Auto-generate 3 bullet insights for a partner."""
    top_family = product_mix.iloc[0]["product_family"] if not product_mix.empty else "iPhone"
    top_rev    = product_mix.iloc[0]["revenue"] if not product_mix.empty else 0

    insights = [
        f"**Revenue Performance:** {partner_name} has generated €{kpis.get('ytd_revenue',0)/1e6:.1f}M YTD, "
        f"{'up' if kpis.get('revenue_delta',0) > 0 else 'down'} "
        f"{abs(kpis.get('revenue_delta',0)):.1f}% week-over-week. {top_family} drives "
        f"€{top_rev/1e6:.1f}M ({top_rev/max(1,kpis.get('ytd_revenue',1))*100:.0f}% of total).",

        f"**In-Stock & Fulfilment:** Average in-stock rate of {kpis.get('in_stock_rate',0):.1f}% with "
        f"{kpis.get('avg_wos',0):.1f} weeks of supply on hand. Fulfilment rate of "
        f"{kpis.get('fulfil_rate',0):.1f}% — "
        f"{'above' if kpis.get('fulfil_rate',0) >= 95 else 'below'} the 95% network target.",

        f"**Risk Posture:** {kpis.get('open_alerts',0)} open alerts, "
        f"{kpis.get('critical_alerts',0)} critical. "
        f"{'No immediate escalation required.' if kpis.get('critical_alerts',0) == 0 else 'Immediate Account Manager review recommended for critical items.'}",
    ]
    return insights
