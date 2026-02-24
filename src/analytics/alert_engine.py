"""
Alert Engine — Statistical alert detection and business alert feed logic.
Author: Mohammed Kaif Ahmed
"""

import pandas as pd
import numpy as np


def detect_demand_anomalies(actuals: pd.DataFrame,
                             products: pd.DataFrame,
                             partners: pd.DataFrame,
                             z_threshold: float = 2.5,
                             iqr_multiplier: float = 1.5) -> pd.DataFrame:
    """
    Detect demand anomalies using Z-score and IQR methods.
    Returns flagged rows with anomaly type, magnitude, and narrative.
    """
    acts = actuals.copy()
    acts = acts.merge(products[["product_id","product_name","product_family"]], on="product_id", how="left")
    acts = acts.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")

    anomalies = []
    for (pid, partid), group in acts.groupby(["product_id","partner_id"]):
        group = group.sort_values("date")
        if len(group) < 8:
            continue

        # Rolling 8-week stats
        group["roll_mean"] = group["units_sold"].rolling(8, min_periods=4).mean().shift(1)
        group["roll_std"]  = group["units_sold"].rolling(8, min_periods=4).std().shift(1)

        # Z-score anomaly
        group["z_score"] = (group["units_sold"] - group["roll_mean"]) / group["roll_std"].replace(0, np.nan)

        # IQR anomaly
        q1 = group["units_sold"].quantile(0.25)
        q3 = group["units_sold"].quantile(0.75)
        iqr = q3 - q1
        lower_iqr = q1 - iqr_multiplier * iqr
        upper_iqr = q3 + iqr_multiplier * iqr

        # Flag last 4 weeks
        recent = group.tail(4)
        for _, row in recent.iterrows():
            if abs(row.get("z_score", 0) or 0) > z_threshold or \
               not (lower_iqr <= row["units_sold"] <= upper_iqr):
                direction = "spike" if row["units_sold"] > row.get("roll_mean", row["units_sold"]) else "drop"
                pct_change = (row["units_sold"] - row.get("roll_mean", row["units_sold"])) / max(1, row.get("roll_mean", 1)) * 100
                anomalies.append({
                    "date":          row["date"],
                    "product_id":    pid,
                    "partner_id":    partid,
                    "product_name":  row.get("product_name",""),
                    "partner_name":  row.get("partner_name",""),
                    "product_family":row.get("product_family",""),
                    "units_actual":  row["units_sold"],
                    "units_expected":round(row.get("roll_mean", row["units_sold"]), 0),
                    "pct_change":    round(pct_change, 1),
                    "anomaly_type":  direction,
                    "z_score":       round(row.get("z_score", 0) or 0, 2),
                    "narrative": (
                        f"{'↑ Demand spike' if direction == 'spike' else '↓ Demand drop'}: "
                        f"{row.get('product_name',pid)} at {row.get('partner_name',partid)} "
                        f"{'exceeded' if direction == 'spike' else 'fell'} 8-week average by "
                        f"{abs(pct_change):.0f}%. "
                        f"Recommend: verify with Account Manager within 48 hours."
                    )
                })

    if not anomalies:
        return pd.DataFrame()
    return pd.DataFrame(anomalies).sort_values("date", ascending=False)


def build_risk_matrix(actuals: pd.DataFrame,
                      products: pd.DataFrame,
                      partners: pd.DataFrame) -> pd.DataFrame:
    """
    Build risk matrix data: likelihood × revenue impact per SKU-partner.
    Likelihood based on WoS and demand trend; impact based on revenue run-rate.
    """
    recent_cutoff = actuals["date"].max() - pd.Timedelta(weeks=4)
    recent = actuals[actuals["date"] >= recent_cutoff].copy()
    recent = recent.merge(products[["product_id","product_name","product_family","asp"]], on="product_id", how="left")
    recent = recent.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")

    agg = recent.groupby(["product_id","partner_id","product_name","partner_name","product_family"]).agg(
        avg_wos=("weeks_of_supply","mean"),
        avg_in_stock=("in_stock_rate","mean"),
        avg_revenue=("revenue","mean"),
        avg_units_sold=("units_sold","mean"),
    ).reset_index()

    # Likelihood: higher if low WoS or low in-stock
    agg["likelihood"] = (
        np.clip(1 - agg["avg_wos"] / 6, 0, 1) * 0.6 +
        np.clip(1 - agg["avg_in_stock"], 0, 1) * 0.4
    ).round(4)

    # Revenue impact: 4-week potential lost revenue
    agg["revenue_impact"] = (agg["avg_revenue"] * 4 * agg["likelihood"]).round(2)
    agg["label"] = agg["product_name"].str[:25] + " / " + agg["partner_name"].str[:15]

    return agg[["product_id","partner_id","product_name","partner_name",
                "product_family","likelihood","revenue_impact","label"]].dropna()


def get_alert_kpis(alerts: pd.DataFrame) -> dict:
    """Compute alert dashboard KPIs."""
    open_alerts = alerts[alerts["status"] == "Open"]
    return {
        "total_open":     len(open_alerts),
        "critical":       len(open_alerts[open_alerts["severity"] == "Critical"]),
        "warning":        len(open_alerts[open_alerts["severity"] == "Warning"]),
        "info":           len(open_alerts[open_alerts["severity"] == "Info"]),
        "revenue_at_risk":open_alerts["revenue_impact"].sum(),
    }
