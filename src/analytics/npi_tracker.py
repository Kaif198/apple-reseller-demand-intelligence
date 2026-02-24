"""
NPI Tracker Analytics — Launch readiness, velocity tracking, and risk identification.
Author: Mohammed Kaif Ahmed
"""

import pandas as pd
import numpy as np


def npi_launch_kpis(npi_df: pd.DataFrame, products: pd.DataFrame) -> dict:
    """Summary KPIs for the NPI tracker page."""
    npi_prods = products[products["is_npi"]]["product_id"].tolist()
    npi_filt  = npi_df[npi_df["product_id"].isin(npi_prods)]

    overall_velocity = npi_filt["velocity_vs_plan"].mean()
    red_count   = (npi_filt["risk_flag"] == "Red").sum()
    amber_count = (npi_filt["risk_flag"] == "Amber").sum()
    green_count = (npi_filt["risk_flag"] == "Green").sum()

    return {
        "overall_velocity":  round(overall_velocity * 100, 1),
        "red_flags":   red_count,
        "amber_flags": amber_count,
        "green_flags": green_count,
    }


def partner_npi_scorecard(npi_df: pd.DataFrame,
                           partners: pd.DataFrame,
                           product_id: str) -> pd.DataFrame:
    """
    Returns per-partner NPI scorecard for a given product.
    Latest week per partner, with velocity, sell-through, and RAG.
    """
    filt = npi_df[npi_df["product_id"] == product_id].copy()
    latest = filt.groupby("partner_id").apply(
        lambda g: g.nlargest(1, "week_number")
    ).reset_index(drop=True)

    latest = latest.merge(partners[["partner_id","partner_name","partner_tier","country"]], on="partner_id", how="left")

    latest["velocity_pct"] = (latest["velocity_vs_plan"] * 100).round(1)
    latest["st_pct"] = (latest["sell_through_rate"] * 100).round(1)

    return latest[[
        "partner_name","partner_tier","country","week_number",
        "units_planned","units_actual","velocity_pct","st_pct","risk_flag","risk_reason"
    ]].sort_values("velocity_pct", ascending=False).reset_index(drop=True)


def npi_waterfall_data(npi_df: pd.DataFrame, partners: pd.DataFrame,
                       product_id: str) -> pd.DataFrame:
    """
    Build waterfall chart data: Plan → Variance by partner → Actual.
    """
    filt = npi_df[npi_df["product_id"] == product_id].copy()
    filt = filt.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")

    summary = filt.groupby("partner_name").agg(
        plan=("units_planned","sum"),
        actual=("units_actual","sum"),
    ).reset_index()
    summary["variance"] = summary["actual"] - summary["plan"]

    return summary.sort_values("variance")
