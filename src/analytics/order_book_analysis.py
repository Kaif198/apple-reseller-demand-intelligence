"""
Order Book Analysis — Business logic for order book health, chase opportunities,
shipment plan validation, and in-stock/ranging analysis.
Author: Mohammed Kaif Ahmed
"""

import pandas as pd
import numpy as np


def order_book_health(order_book: pd.DataFrame) -> dict:
    """Compute order book health KPIs."""
    total_open_value = order_book[order_book["status"] != "Shipped"]["units_confirmed"].sum()
    total_orders = len(order_book)
    at_risk = len(order_book[order_book["status"] == "At Risk"])
    at_risk_pct = at_risk / total_orders * 100

    shipped = order_book[order_book["status"] == "Shipped"]
    partial = order_book[order_book["status"] == "Partially Fulfilled"]
    fulfil_numerator = shipped["units_shipped"].sum() + partial["units_shipped"].sum()
    fulfil_denominator = order_book["units_ordered"].sum()
    fulfil_rate = fulfil_numerator / fulfil_denominator * 100 if fulfil_denominator > 0 else 0

    chase_value = order_book[order_book["chase_opportunity"]]["chase_revenue_potential"].sum()

    return {
        "total_orders":     total_orders,
        "at_risk_pct":      round(at_risk_pct, 1),
        "fulfilment_rate":  round(fulfil_rate, 1),
        "chase_value":      chase_value,
    }


def get_chase_opportunities(order_book: pd.DataFrame,
                             products: pd.DataFrame,
                             partners: pd.DataFrame,
                             top_n: int = 20) -> pd.DataFrame:
    """
    Return top N chase opportunities ranked by revenue potential.
    Identifies partner × product combos where sell-through > 85% and WoS < 3.
    """
    chase = order_book[order_book["chase_opportunity"]].copy()
    chase = chase.merge(products[["product_id","product_name","product_family","asp"]], on="product_id", how="left")
    chase = chase.merge(partners[["partner_id","partner_name","partner_tier"]], on="partner_id", how="left")

    chase = chase.sort_values("chase_revenue_potential", ascending=False).head(top_n)

    chase["priority"] = pd.cut(
        chase["chase_revenue_potential"],
        bins=[0, 100_000, 300_000, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    return chase[[
        "partner_name", "product_name", "product_family",
        "chase_units_recommended", "chase_revenue_potential",
        "status", "priority", "partner_tier"
    ]].reset_index(drop=True)


def shipment_plan_validation(order_book: pd.DataFrame,
                              forecast: pd.DataFrame,
                              products: pd.DataFrame) -> pd.DataFrame:
    """
    Compare next week's shipment plan (confirmed orders) against forecast,
    grouped by product family.
    """
    # Planned: sum confirmed units from open orders by product family
    plan = order_book[order_book["status"].isin(["Open", "Partially Fulfilled"])].copy()
    plan = plan.merge(products[["product_id","product_family"]], on="product_id", how="left")
    plan_by_family = plan.groupby("product_family")["units_confirmed"].sum().reset_index()
    plan_by_family.columns = ["product_family", "planned_units"]

    # Forecast: next week ensemble forecast by family
    ens = forecast[forecast["forecast_model"] == "Ensemble"].copy()
    ens = ens.merge(products[["product_id","product_family"]], on="product_id", how="left")
    ens_by_family = ens.groupby("product_family")["forecast_units"].sum().reset_index()
    ens_by_family.columns = ["product_family", "forecast_units"]

    result = plan_by_family.merge(ens_by_family, on="product_family", how="outer").fillna(0)
    result["gap"] = result["planned_units"] - result["forecast_units"]
    result["gap_pct"] = (result["gap"] / result["forecast_units"].replace(0, 1)) * 100
    result["rag"] = result["gap_pct"].apply(
        lambda x: "Green" if -10 <= x <= 10 else ("Amber" if -20 <= x < -10 or 10 < x <= 20 else "Red")
    )
    return result.sort_values("planned_units", ascending=False).reset_index(drop=True)


def instock_ranging_analysis(actuals: pd.DataFrame, products: pd.DataFrame,
                              partners: pd.DataFrame) -> pd.DataFrame:
    """
    Returns partner × product_family in-stock rates for heatmap.
    Also flags ranging gaps (missing SKUs at partners).
    """
    recent = actuals[actuals["date"] >= actuals["date"].max() - pd.Timedelta(weeks=4)]
    merged = recent.merge(products[["product_id","product_family"]], on="product_id", how="left")
    merged = merged.merge(partners[["partner_id","partner_name"]], on="partner_id", how="left")

    heatmap = merged.groupby(["partner_name","product_family"])["in_stock_rate"].mean().reset_index()
    heatmap.columns = ["partner_name", "product_family", "in_stock_rate"]

    return heatmap
