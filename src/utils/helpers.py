"""
Helpers — Shared utility functions for the Apple Demand Planner platform.
Author: Mohammed Kaif Ahmed
"""

import pandas as pd
import numpy as np
import os
import sys

# ─── Path helpers ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR  = os.path.join(BASE_DIR, "data", "raw")
PROC_DIR = os.path.join(BASE_DIR, "data", "processed")


def get_data_path(filename: str, processed: bool = False) -> str:
    """Return absolute path to a data file."""
    folder = PROC_DIR if processed else RAW_DIR
    return os.path.join(folder, filename)


# ─── Formatters ───────────────────────────────────────────────────────────────
def format_eur(value: float, decimals: int = 1) -> str:
    """Format a value as euros, e.g. €4.2M or €890K."""
    if abs(value) >= 1_000_000_000:
        return f"€{value/1e9:.{decimals}f}B"
    elif abs(value) >= 1_000_000:
        return f"€{value/1e6:.{decimals}f}M"
    elif abs(value) >= 1_000:
        return f"€{value/1e3:.{decimals}f}K"
    else:
        return f"€{value:,.0f}"


def format_pct(value: float, decimals: int = 1) -> str:
    """Format a decimal (0-1) or percentage value as a string."""
    if value <= 1.5:
        return f"{value*100:.{decimals}f}%"
    return f"{value:.{decimals}f}%"


def format_units(value: float) -> str:
    """Format unit count with K suffix."""
    if abs(value) >= 1_000:
        return f"{value/1e3:.1f}K"
    return f"{int(round(value)):,}"


def format_delta(delta_pct: float) -> tuple:
    """Return (symbol, colour_class) for a percentage delta."""
    if delta_pct > 0:
        return f"↑ {abs(delta_pct):.1f}%", "positive"
    elif delta_pct < 0:
        return f"↓ {abs(delta_pct):.1f}%", "negative"
    else:
        return "— 0.0%", "neutral"


# ─── RAG utilities ────────────────────────────────────────────────────────────
def rag_color(flag: str) -> str:
    """Return hex colour for a RAG flag string."""
    mapping = {"Green": "#34C759", "Amber": "#FF9500", "Red": "#FF3B30"}
    return mapping.get(flag, "#8E8E93")


def severity_badge_class(severity: str) -> str:
    """Return CSS class for alert severity."""
    mapping = {
        "Critical": "badge-red",
        "Warning":  "badge-amber",
        "Info":     "badge-blue",
        "Success":  "badge-green",
    }
    return mapping.get(severity, "badge-blue")


# ─── Data loaders ─────────────────────────────────────────────────────────────
def load_products() -> pd.DataFrame:
    return pd.read_csv(get_data_path("products.csv"), parse_dates=["launch_date"])


def load_partners() -> pd.DataFrame:
    return pd.read_csv(get_data_path("reseller_partners.csv"))


def load_actuals() -> pd.DataFrame:
    return pd.read_csv(get_data_path("demand_actuals.csv"), parse_dates=["date"])


def load_forecasts() -> pd.DataFrame:
    return pd.read_csv(get_data_path("forecasts.csv"), parse_dates=["date"])


def load_order_book() -> pd.DataFrame:
    return pd.read_csv(get_data_path("order_book.csv"), parse_dates=["date_placed","date_requested"])


def load_npi_tracker() -> pd.DataFrame:
    return pd.read_csv(get_data_path("npi_tracker.csv"))


def load_alerts() -> pd.DataFrame:
    return pd.read_csv(get_data_path("alerts.csv"), parse_dates=["date_generated"])


def load_all() -> dict:
    """Load all datasets and return them keyed by name."""
    return {
        "products": load_products(),
        "partners": load_partners(),
        "actuals":  load_actuals(),
        "forecasts":load_forecasts(),
        "order_book": load_order_book(),
        "npi":      load_npi_tracker(),
        "alerts":   load_alerts(),
    }


# ─── KPI calculations ─────────────────────────────────────────────────────────
def calc_forecast_accuracy(actuals: pd.DataFrame, forecasts: pd.DataFrame,
                            model: str = "Ensemble") -> dict:
    """
    Calculate MAPE, WMAPE, Bias across product families for one model.
    Uses matching on date + product_id + partner_id.
    """
    fcast = forecasts[forecasts["forecast_model"] == model].copy()
    merged = actuals.merge(
        fcast[["date","product_id","partner_id","forecast_units"]],
        on=["date","product_id","partner_id"], how="inner"
    )
    if merged.empty:
        return {"mape": 0, "wmape": 0, "bias": 0, "accuracy": 0}

    merged["error"] = merged["forecast_units"] - merged["units_sold"]
    merged["abs_error"] = merged["error"].abs()
    merged["abs_pct_error"] = merged["abs_error"] / merged["units_sold"].replace(0, np.nan)

    mape  = merged["abs_pct_error"].mean() * 100
    wmape = merged["abs_error"].sum() / merged["units_sold"].sum() * 100
    bias  = merged["error"].mean() / merged["units_sold"].mean() * 100
    acc   = 100 - wmape

    return {"mape": round(mape, 2), "wmape": round(wmape, 2),
            "bias": round(bias, 2), "accuracy": round(acc, 1)}


def calc_channel_kpis(actuals: pd.DataFrame, order_book: pd.DataFrame,
                       alerts: pd.DataFrame, products: pd.DataFrame) -> dict:
    """Compute the 6 Executive Overview KPIs."""
    total_rev = actuals["revenue"].sum()

    # WoW delta
    last_week = actuals["date"].max()
    prev_week = last_week - pd.Timedelta(weeks=1)
    rev_lw = actuals[actuals["date"] == last_week]["revenue"].sum()
    rev_pw = actuals[actuals["date"] == prev_week]["revenue"].sum()
    rev_delta = (rev_lw - rev_pw) / rev_pw * 100 if rev_pw > 0 else 0

    avg_in_stock = actuals["in_stock_rate"].mean() * 100

    fulfil = actuals["units_shipped"].sum() / actuals["units_ordered"].sum() * 100

    chase_rev = order_book[order_book["chase_opportunity"]]["chase_revenue_potential"].sum()

    active_alerts = len(alerts[alerts["status"] == "Open"])
    critical_alerts = len(alerts[(alerts["status"] == "Open") &
                                  (alerts["severity"] == "Critical")])

    return {
        "total_revenue":    total_rev,
        "revenue_delta":    round(rev_delta, 1),
        "in_stock_rate":    round(avg_in_stock, 1),
        "fulfilment_rate":  round(fulfil, 1),
        "chase_opportunity":chase_rev,
        "active_alerts":    active_alerts,
        "critical_alerts":  critical_alerts,
    }


# ─── Week utilities ────────────────────────────────────────────────────────────
def iso_week_label(d: pd.Timestamp) -> str:
    """Return 'W12, 2025' style label."""
    return f"W{d.isocalendar()[1]}, {d.year}"


def current_week_label() -> str:
    return "W37, 2025"  # Simulation "today"
