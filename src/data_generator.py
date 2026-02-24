"""
Apple Reseller Channel — Synthetic Data Generator
Generates all 7 CSV datasets for the Demand Planning & Inventory Intelligence Platform.
Author: Mohammed Kaif Ahmed
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import warnings
warnings.filterwarnings("ignore")

# ─── Reproducibility ───────────────────────────────────────────────────────────
np.random.seed(42)

# ─── Output paths ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 1. PRODUCTS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_products() -> pd.DataFrame:
    """Generate 40 realistic Apple SKUs with correct ASPs and lifecycle attributes."""
    today = date(2025, 9, 15)  # Simulation "today"

    products = [
        # ── iPhone 16 Series (NPI — launched Aug 2025) ─────────────────────────
        ("IPHONE-16-PRO-MAX-256",  "iPhone 16 Pro Max 256GB",   "iPhone", "iPhone Pro Max",  date(2025,9,1),  1_299, "Launch", "Tier 1"),
        ("IPHONE-16-PRO-MAX-512",  "iPhone 16 Pro Max 512GB",   "iPhone", "iPhone Pro Max",  date(2025,9,1),  1_499, "Launch", "Tier 1"),
        ("IPHONE-16-PRO-MAX-1TB",  "iPhone 16 Pro Max 1TB",     "iPhone", "iPhone Pro Max",  date(2025,9,1),  1_749, "Launch", "Tier 1"),
        ("IPHONE-16-PRO-128",      "iPhone 16 Pro 128GB",       "iPhone", "iPhone Pro",      date(2025,9,1),  1_099, "Launch", "Tier 1"),
        ("IPHONE-16-PRO-256",      "iPhone 16 Pro 256GB",       "iPhone", "iPhone Pro",      date(2025,9,1),  1_199, "Launch", "Tier 1"),
        ("IPHONE-16-PRO-512",      "iPhone 16 Pro 512GB",       "iPhone", "iPhone Pro",      date(2025,9,1),  1_399, "Launch", "Tier 1"),
        ("IPHONE-16-128",          "iPhone 16 128GB",           "iPhone", "iPhone",          date(2025,9,1),    929, "Launch", "Tier 1"),
        ("IPHONE-16-256",          "iPhone 16 256GB",           "iPhone", "iPhone",          date(2025,9,1),  1_029, "Launch", "Tier 1"),
        ("IPHONE-16-PLUS-128",     "iPhone 16 Plus 128GB",      "iPhone", "iPhone Plus",     date(2025,9,1),  1_079, "Launch", "Tier 1"),
        ("IPHONE-16-PLUS-256",     "iPhone 16 Plus 256GB",      "iPhone", "iPhone Plus",     date(2025,9,1),  1_179, "Launch", "Tier 1"),
        # ── iPhone 15 Series (Maturity/Decline) ────────────────────────────────
        ("IPHONE-15-PRO-128",      "iPhone 15 Pro 128GB",       "iPhone", "iPhone Pro",      date(2024,9,15),   849, "Maturity", "Tier 1"),
        ("IPHONE-15-PRO-256",      "iPhone 15 Pro 256GB",       "iPhone", "iPhone Pro",      date(2024,9,15),   949, "Maturity", "Tier 1"),
        ("IPHONE-15-128",          "iPhone 15 128GB",           "iPhone", "iPhone",          date(2024,9,15),   729, "Decline",  "Tier 1"),
        ("IPHONE-15-256",          "iPhone 15 256GB",           "iPhone", "iPhone",          date(2024,9,15),   829, "Decline",  "Tier 1"),
        # ── iPad ───────────────────────────────────────────────────────────────
        ("IPAD-AIR-M3-11-128",     "iPad Air 11\" M3 128GB WiFi","iPad",  "iPad Air",        date(2025,3,1),    699, "Growth",  "Tier 2"),
        ("IPAD-AIR-M3-13-256",     "iPad Air 13\" M3 256GB WiFi","iPad",  "iPad Air",        date(2025,3,1),    999, "Growth",  "Tier 2"),
        ("IPAD-PRO-M4-11-256",     "iPad Pro 11\" M4 256GB WiFi","iPad",  "iPad Pro",        date(2024,5,15),  1_099, "Maturity","Tier 2"),
        ("IPAD-PRO-M4-13-256",     "iPad Pro 13\" M4 256GB WiFi","iPad",  "iPad Pro",        date(2024,5,15),  1_399, "Maturity","Tier 2"),
        ("IPAD-10-64",             "iPad 10th Gen 64GB WiFi",   "iPad",   "iPad",            date(2023,10,1),   449, "Decline", "Tier 2"),
        ("IPAD-MINI-7-128",        "iPad mini 7 128GB WiFi",    "iPad",   "iPad mini",       date(2024,10,1),   599, "Maturity","Tier 2"),
        # ── Mac ────────────────────────────────────────────────────────────────
        ("MBP-14-M4-16GB",         "MacBook Pro 14\" M4 16GB",  "Mac",   "MacBook Pro",     date(2024,11,1),  2_399, "Growth",  "Tier 2"),
        ("MBP-14-M4PRO-24GB",      "MacBook Pro 14\" M4 Pro 24GB","Mac",  "MacBook Pro",     date(2024,11,1),  2_999, "Growth",  "Tier 2"),
        ("MBP-16-M4PRO-24GB",      "MacBook Pro 16\" M4 Pro 24GB","Mac",  "MacBook Pro",     date(2024,11,1),  3_499, "Growth",  "Tier 2"),
        ("MBA-M3-8GB-256",         "MacBook Air 13\" M3 8GB",   "Mac",   "MacBook Air",     date(2024,3,1),   1_299, "Maturity","Tier 2"),
        ("MBA-M3-16GB-512",        "MacBook Air 13\" M3 16GB",  "Mac",   "MacBook Air",     date(2024,3,1),   1_699, "Maturity","Tier 2"),
        # ── Apple Watch ────────────────────────────────────────────────────────
        ("AW-ULTRA-2-49",          "Apple Watch Ultra 2 49mm",  "Apple Watch","Watch Ultra", date(2024,9,15),   899, "Maturity","Tier 2"),
        ("AW-S10-42-AL",           "Apple Watch Series 10 42mm Aluminium","Apple Watch","Watch Series",date(2024,9,15),449,"Maturity","Tier 2"),
        ("AW-S10-46-AL",           "Apple Watch Series 10 46mm Aluminium","Apple Watch","Watch Series",date(2024,9,15),479,"Maturity","Tier 2"),
        ("AW-SE-40-AL",            "Apple Watch SE 40mm Aluminium","Apple Watch","Watch SE", date(2024,9,15),   279, "Maturity","Tier 2"),
        ("AW-SE-44-AL",            "Apple Watch SE 44mm Aluminium","Apple Watch","Watch SE", date(2024,9,15),   299, "Maturity","Tier 2"),
        # ── AirPods ────────────────────────────────────────────────────────────
        ("AIRPODS-4-ANC",          "AirPods 4 with ANC",        "AirPods","AirPods",         date(2024,9,15),   179, "Growth",  "Tier 2"),
        ("AIRPODS-4",              "AirPods 4",                 "AirPods","AirPods",          date(2024,9,15),   149, "Growth",  "Tier 2"),
        ("AIRPODS-PRO-2",          "AirPods Pro 2nd Gen",       "AirPods","AirPods Pro",      date(2023,9,15),   279, "Maturity","Tier 2"),
        ("AIRPODS-MAX-USB-C",      "AirPods Max USB-C",         "AirPods","AirPods Max",      date(2024,9,15),   549, "Growth",  "Tier 2"),
        # ── Accessories ────────────────────────────────────────────────────────
        ("ACC-MCASE-16PRO-CLEAR",  "iPhone 16 Pro Clear Case",  "Accessories","Cases",       date(2025,9,1),     59,  "Launch", "Tier 3"),
        ("ACC-MCASE-16-SILICON",   "iPhone 16 Silicone Case",   "Accessories","Cases",       date(2025,9,1),     59,  "Launch", "Tier 3"),
        ("ACC-MCASE-16PRO-FINE",   "iPhone 16 Pro FineWoven Case","Accessories","Cases",     date(2025,9,1),     79,  "Launch", "Tier 3"),
        ("ACC-MSTAND",             "MagSafe Duo Charger",       "Accessories","Chargers",    date(2021,11,1),   149,  "Maturity","Tier 3"),
        ("ACC-APPLECARE-IPHONE",   "AppleCare+ for iPhone 16",  "Accessories","AppleCare",  date(2025,9,1),    199,  "Launch", "Tier 3"),
        ("ACC-LIGHTNING-USBC",     "USB-C to MagSafe 3 Cable",  "Accessories","Cables",     date(2023,6,1),     49,  "Maturity","Tier 3"),
    ]

    rows = []
    for pid, name, family, category, launch, asp, lifecycle, priority in products:
        is_npi = (today - launch).days <= 90
        rows.append({
            "product_id":       pid,
            "product_name":     name,
            "product_family":   family,
            "product_category": category,
            "launch_date":      launch,
            "is_npi":           is_npi,
            "asp":              asp,
            "lifecycle_stage":  lifecycle,
            "priority_tier":    priority,
        })

    df = pd.DataFrame(rows)
    print(f"  ✓ Products: {len(df)} SKUs, {df['is_npi'].sum()} NPIs")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 2. RESELLER PARTNERS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_partners() -> pd.DataFrame:
    """Generate 13 EMEA reseller partners with Pareto-distributed revenue."""
    partners = [
        # name, country, region, tier, avg_monthly_rev_M, stores, digital_maturity
        ("MediaMarkt DE",     "DE", "DACH",    "Platinum", 28.5, 417, 9),
        ("Currys UK",         "GB", "UK&I",    "Platinum", 22.1, 305, 8),
        ("Fnac FR",           "FR", "France",  "Gold",     11.4, 102, 7),
        ("Euronics IT",       "IT", "South EU","Gold",      8.9, 258, 6),
        ("El Corte Inglés ES","ES", "South EU","Gold",      7.2,  88, 6),
        ("Elkjøp NO",         "NO", "Nordic",  "Gold",      6.8, 197, 7),
        ("Saturn DE",         "DE", "DACH",    "Gold",     10.3, 158, 8),
        ("Coolblue NL",       "NL", "Benelux", "Gold",      5.5,  24, 10),
        ("Expert SE",         "SE", "Nordic",  "Silver",    3.1, 152, 6),
        ("Darty FR",          "FR", "France",  "Silver",    3.8, 213, 5),
        ("Power DK",          "DK", "Nordic",  "Silver",    2.4,  54, 6),
        ("Komplett NO",       "NO", "Nordic",  "Silver",    1.8,   0, 10),  # online-only
        ("Harvey Norman IE",  "IE", "UK&I",    "Silver",    1.4,  33, 5),
    ]

    rows = []
    for i, (name, country, region, tier, rev, stores, digital) in enumerate(partners):
        rows.append({
            "partner_id":           f"PARTNER-{i+1:03d}",
            "partner_name":         name,
            "country":              country,
            "region":               region,
            "partner_tier":         tier,
            "avg_monthly_revenue":  rev * 1_000_000,
            "store_count":          stores,
            "digital_maturity_score": digital,
        })

    df = pd.DataFrame(rows)
    print(f"  ✓ Partners: {len(df)} resellers across {df['country'].nunique()} countries")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 3. DEMAND ACTUALS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_demand_actuals(products: pd.DataFrame, partners: pd.DataFrame) -> pd.DataFrame:
    """
    Generate 104 weeks of weekly demand per product × partner.
    Simulates seasonality, NPI curves, supply constraints, Pareto partner sizes,
    accessory correlation, YoY growth, and noise.
    """
    print("  Generating demand actuals (this may take 30-60 seconds)...")

    # Date spine: 104 weeks ending ~ today (Sep 15 2025), starting Oct 2023
    end_date   = date(2025, 8, 25)  # Last full week before "today"
    start_date = end_date - timedelta(weeks=103)
    weeks = [start_date + timedelta(weeks=i) for i in range(104)]

    # Partner revenue weights (Pareto) — must sum to 1
    partner_weights = np.array([28.5, 22.1, 11.4, 8.9, 7.2, 6.8, 10.3, 5.5,
                                  3.1, 3.8, 2.4, 1.8, 1.4])
    partner_weights = partner_weights / partner_weights.sum()

    # Product family baseline weekly channel units (total network)
    family_base = {
        "iPhone":       6_500,
        "iPad":         1_800,
        "Mac":            900,
        "Apple Watch":    800,
        "AirPods":      1_400,
        "Accessories":  3_500,
    }

    rows = []
    iphone_demand_by_week = {}  # track for accessory lag correlation

    product_list = products.to_dict("records")
    partner_list = partners.to_dict("records")

    for week_idx, week_start in enumerate(weeks):
        week_num = week_start.isocalendar()[1]   # ISO week number
        year     = week_start.year
        yoy_factor = 1.0 + 0.06 * ((year - 2023) + (week_idx / 104))

        # ── Seasonality multipliers (applied to all iPhone/tech) ────────────
        # iPhone launch: W37-W42
        iphone_launch_mult = 1.0
        if 37 <= week_num <= 41:
            iphone_launch_mult = 1.0 + 3.4 * np.exp(-0.5 * ((week_num - 39) / 1.5) ** 2)
        elif 42 <= week_num <= 46:
            iphone_launch_mult = 1.0 + 0.3 * np.exp(-0.4 * (week_num - 42))

        # Holiday season: W47-W52
        holiday_mult = 1.0
        if 47 <= week_num <= 52:
            holiday_mult = 1.0 + 1.8 * np.exp(-0.3 * abs(week_num - 50))

        # Back-to-school: W33-W37
        bts_mult = 1.0
        if 33 <= week_num <= 37:
            bts_mult = 1.0 + 0.6 * np.exp(-0.5 * abs(week_num - 35))

        # Feb dip (CNY supply effect)
        feb_mult = 0.85 if week_num in [6, 7, 8] else 1.0

        total_iphone_demand_this_week = 0

        for prod in product_list:
            family    = prod["product_family"]
            pid       = prod["product_id"]
            asp       = prod["asp"]
            lifecycle = prod["lifecycle_stage"]
            launch    = prod["launch_date"] if isinstance(prod["launch_date"], date) else pd.to_datetime(prod["launch_date"]).date()
            weeks_since_launch = max(0, (week_start - launch).days // 7)

            # ── Lifecycle factor ─────────────────────────────────────────────
            if lifecycle == "Launch":
                if weeks_since_launch < 0:
                    lc_factor = 0.0  # product not yet launched
                else:
                    lc_factor = max(0.3, 1.0 * np.exp(-0.08 * weeks_since_launch)) + 0.3
            elif lifecycle == "Growth":
                lc_factor = min(1.0, 0.5 + 0.04 * weeks_since_launch)
            elif lifecycle == "Maturity":
                lc_factor = 1.0
            elif lifecycle == "Decline":
                lc_factor = max(0.2, 1.0 - 0.004 * weeks_since_launch)
            else:
                lc_factor = 1.0

            # ── Family seasonal mult ─────────────────────────────────────────
            if family == "iPhone":
                season_mult = iphone_launch_mult * holiday_mult * bts_mult * feb_mult
            elif family in ["iPad", "Mac"]:
                season_mult = (0.4 * iphone_launch_mult + 0.6) * holiday_mult * bts_mult
            elif family == "Apple Watch":
                season_mult = (0.3 * iphone_launch_mult + 0.7) * holiday_mult
            elif family == "AirPods":
                # 1-week lag on iPhone launch
                prev_week_num = (week_num - 1) if week_num > 1 else 52
                lag_iphone = 1.0
                if 38 <= prev_week_num <= 43:
                    lag_iphone = 1.0 + 2.0 * np.exp(-0.6 * abs(prev_week_num - 40))
                season_mult = lag_iphone * holiday_mult
            elif family == "Accessories":
                # 1-2 week lag on iPhone launch
                lag_iphone = 1.0
                if 39 <= week_num <= 45:
                    lag_iphone = 1.0 + 2.5 * np.exp(-0.5 * abs(week_num - 41))
                season_mult = lag_iphone * holiday_mult
            else:
                season_mult = 1.0

            base_family_units = family_base.get(family, 500)

            # Distribute family units across SKUs in that family
            family_skus = [p for p in product_list if p["product_family"] == family]
            sku_count   = len(family_skus)
            # Weight by ASP inverse (cheaper sells more) and lifecycle
            sku_rank    = sorted(family_skus, key=lambda x: x["asp"])
            sku_unit_weight = 1.0 / (1.0 + 0.5 * sku_rank.index(prod)) if prod in sku_rank else 1.0
            total_sku_weight = sum(1.0 / (1.0 + 0.5 * i) for i in range(sku_count))
            sku_fraction = sku_unit_weight / total_sku_weight if total_sku_weight > 0 else 1.0 / sku_count

            base_units = base_family_units * sku_fraction * season_mult * lc_factor * yoy_factor

            # Track for accessory correlation
            if family == "iPhone":
                total_iphone_demand_this_week += base_units

            for p_idx, partner in enumerate(partner_list):
                partner_weight = partner_weights[p_idx]
                partner_id     = partner["partner_id"]

                # Partner × product eligibility (smaller partners don't carry every SKU)
                tier = partner["partner_tier"]
                if tier == "Silver" and prod["priority_tier"] == "Tier 3" and np.random.random() < 0.25:
                    continue  # Silver partners sometimes skip accessories

                partner_units = base_units * partner_weight * 13  # scale to partner level
                noise = np.random.normal(1.0, 0.10)
                noise = np.clip(noise, 0.7, 1.4)
                units_ordered = max(0, int(round(partner_units * noise)))

                if units_ordered == 0:
                    continue

                # ── Supply constraint (~12% of rows) ─────────────────────────
                is_constrained = np.random.random() < 0.12
                if is_constrained:
                    fill_rate = np.random.uniform(0.55, 0.85)
                else:
                    fill_rate = np.random.uniform(0.92, 1.0)
                units_shipped = max(0, int(round(units_ordered * fill_rate)))

                # Sell-through: slightly less than shipped (some stay on shelf)
                st_rate = np.random.uniform(0.78, 0.97)
                units_sold = max(0, int(round(units_shipped * st_rate)))

                asp_variance = np.random.uniform(0.97, 1.03)
                asp_actual   = prod["asp"] * asp_variance
                revenue      = units_sold * asp_actual

                # In-stock rate — worse if constrained
                if is_constrained:
                    in_stock_rate = np.random.uniform(0.60, 0.85)
                else:
                    in_stock_rate = np.random.uniform(0.88, 0.99)

                # Inject ~1.5% data quality NaN in in_stock_rate
                if np.random.random() < 0.015:
                    in_stock_rate = np.nan

                # Weeks of supply (rough: inventory / weekly_run_rate)
                inventory = max(0, (units_shipped - units_sold) + np.random.randint(0, int(units_sold * 0.5) + 1))
                run_rate  = max(1, units_sold)
                wos = round(inventory / run_rate, 2) if run_rate > 0 else 0.0
                wos = min(wos, 12.0)

                rows.append({
                    "date":          week_start,
                    "product_id":    pid,
                    "partner_id":    partner_id,
                    "units_ordered": units_ordered,
                    "units_shipped": units_shipped,
                    "units_sold":    units_sold,
                    "revenue":       round(revenue, 2),
                    "asp_actual":    round(asp_actual, 2),
                    "in_stock_rate": round(in_stock_rate, 4) if not (isinstance(in_stock_rate, float) and np.isnan(in_stock_rate)) else np.nan,
                    "weeks_of_supply": wos,
                })

        iphone_demand_by_week[week_start] = total_iphone_demand_this_week

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    print(f"  ✓ Demand actuals: {len(df):,} rows | {df['date'].nunique()} weeks | Total revenue €{df['revenue'].sum()/1e9:.2f}B")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 4. FORECASTS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_forecasts(products: pd.DataFrame, partners: pd.DataFrame,
                       actuals: pd.DataFrame) -> pd.DataFrame:
    """Generate 12-week forward forecasts per product × partner with 4 models."""
    today = date(2025, 9, 15)
    forecast_weeks = [today + timedelta(weeks=i) for i in range(1, 13)]
    models = ["ARIMA", "Prophet", "RF", "Ensemble"]
    model_accuracy = {"ARIMA": 0.885, "Prophet": 0.902, "RF": 0.897, "Ensemble": 0.913}

    # Get trailing 8-week avg as base forecast signal
    recent_cutoff = pd.Timestamp(today - timedelta(weeks=8))
    recent = actuals[actuals["date"] >= recent_cutoff].groupby(
        ["product_id", "partner_id"]
    ).agg(weekly_avg_units=("units_sold", "mean")).reset_index()

    rows = []
    for _, row in recent.iterrows():
        pid    = row["product_id"]
        partid = row["partner_id"]
        base   = row["weekly_avg_units"]

        prod_info = products[products["product_id"] == pid]
        if prod_info.empty:
            continue
        lifecycle = prod_info.iloc[0]["lifecycle_stage"]

        for wk_idx, fw in enumerate(forecast_weeks):
            week_num = fw.isocalendar()[1]
            trend = 1.0 + 0.005 * wk_idx  # slight upward trend in forecast

            # iphone launch bump for W37-W43
            if pid.startswith("IPHONE-16") and 37 <= week_num <= 43:
                trend *= (1.5 + 0.5 * np.exp(-0.4 * abs(week_num - 39)))
            elif pid.startswith("IPHONE-16") and week_num > 43:
                trend *= max(0.8, 1.0 - 0.03 * (week_num - 43))

            # Holiday uplift
            if 47 <= week_num <= 52:
                trend *= 1.4

            forecast_base = max(0, base * trend)

            for model in models:
                mape = 1.0 - model_accuracy[model]
                noise_factor = np.random.normal(1.0, mape * 0.5)
                forecast_units = max(0, int(round(forecast_base * noise_factor)))

                # Confidence intervals (80%)
                ci_half = forecast_units * (mape * 2.0)
                lower = max(0, int(round(forecast_units - ci_half)))
                upper = int(round(forecast_units + ci_half))

                # Trailing MAPE metric (per model)
                trailing_mape = round(mape + np.random.uniform(-0.01, 0.01), 4)

                rows.append({
                    "date":                fw,
                    "product_id":          pid,
                    "partner_id":          partid,
                    "forecast_units":      forecast_units,
                    "forecast_lower":      lower,
                    "forecast_upper":      upper,
                    "forecast_model":      model,
                    "forecast_accuracy_mape": trailing_mape,
                })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    print(f"  ✓ Forecasts: {len(df):,} rows | {df['forecast_model'].nunique()} models | "
          f"12 weeks forward")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 5. ORDER BOOK
# ═══════════════════════════════════════════════════════════════════════════════
def generate_order_book(products: pd.DataFrame, partners: pd.DataFrame,
                        actuals: pd.DataFrame) -> pd.DataFrame:
    """Generate current open order book. ~200-300 active orders."""
    today = pd.Timestamp("2025-09-15")
    statuses = ["Open", "Partially Fulfilled", "At Risk", "Shipped"]
    status_weights = [0.40, 0.25, 0.15, 0.20]

    # Base on recent actuals for realistic sizing
    recent = actuals[actuals["date"] >= today - pd.Timedelta(weeks=4)].groupby(
        ["product_id", "partner_id"]
    ).agg(avg_weekly=("units_ordered", "mean")).reset_index()

    rows = []
    order_id = 1

    for _, base_row in recent.iterrows():
        pid    = base_row["product_id"]
        partid = base_row["partner_id"]
        avg_wk = base_row["avg_weekly"]

        if avg_wk < 1:
            continue
        if np.random.random() < 0.35:
            continue  # Not every product-partner combo has an open order

        prod_info = products[products["product_id"] == pid].iloc[0]

        placed_days_ago = np.random.randint(1, 28)
        date_placed = today - pd.Timedelta(days=placed_days_ago)
        lead_time   = np.random.randint(5, 21)
        date_req    = date_placed + pd.Timedelta(days=lead_time)

        units_ordered   = max(1, int(round(avg_wk * 2 * np.random.uniform(0.8, 1.3))))
        status          = np.random.choice(statuses, p=status_weights)

        if status == "Shipped":
            units_confirmed = units_ordered
            units_shipped   = units_confirmed
        elif status == "Partially Fulfilled":
            units_confirmed = units_ordered
            units_shipped   = int(units_ordered * np.random.uniform(0.4, 0.8))
        elif status == "At Risk":
            units_confirmed = int(units_ordered * np.random.uniform(0.5, 0.9))
            units_shipped   = 0
        else:  # Open
            units_confirmed = int(units_ordered * np.random.uniform(0.7, 1.0))
            units_shipped   = 0

        # Chase opportunity: sell-through high, WoS low
        chase = status in ["Open", "Partially Fulfilled"] and np.random.random() < 0.35
        chase_units = int(units_ordered * np.random.uniform(0.15, 0.40)) if chase else 0
        chase_rev   = chase_units * prod_info["asp"] if chase else 0.0

        rows.append({
            "order_id":                f"ORD-{order_id:05d}",
            "date_placed":             date_placed,
            "date_requested":          date_req,
            "product_id":              pid,
            "partner_id":              partid,
            "units_ordered":           units_ordered,
            "units_confirmed":         units_confirmed,
            "units_shipped":           units_shipped,
            "status":                  status,
            "chase_opportunity":       chase,
            "chase_units_recommended": chase_units,
            "chase_revenue_potential": round(chase_rev, 2),
        })
        order_id += 1

    df = pd.DataFrame(rows)
    print(f"  ✓ Order book: {len(df):,} orders | "
          f"Chase opportunity: €{df['chase_revenue_potential'].sum()/1e6:.1f}M")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 6. NPI TRACKER
# ═══════════════════════════════════════════════════════════════════════════════
def generate_npi_tracker(products: pd.DataFrame, partners: pd.DataFrame) -> pd.DataFrame:
    """Track NPI launch performance weeks 1-12 per NPI product × partner."""
    npi_products = products[products["is_npi"]].copy()
    rows = []

    # Risk scenario: Fnac FR underperforming on iPhone 16 Pro
    for _, prod in npi_products.iterrows():
        pid = prod["product_id"]
        asp = prod["asp"]

        for _, partner in partners.iterrows():
            partid = partner["partner_id"]
            pname  = partner["partner_name"]
            weight = {
                "Platinum": 1.0, "Gold": 0.55, "Silver": 0.25
            }.get(partner["partner_tier"], 0.5)

            # Not all partners carry every NPI
            if partner["partner_tier"] == "Silver" and np.random.random() < 0.3:
                continue

            # Weeks available since launch
            launch = prod["launch_date"]
            if isinstance(launch, str):
                launch = pd.to_datetime(launch).date()
            today = date(2025, 9, 15)
            weeks_live = min(12, max(0, (today - launch).days // 7))
            if weeks_live == 0:
                continue

            # Planned allocation (based on partner tier)
            base_plan = int(400 * weight * (1 / (1 + 0.1 * asp / 500)))
            base_plan = max(10, base_plan)

            for wk in range(1, weeks_live + 1):
                units_planned = int(base_plan * max(0.3, 1.0 - 0.07 * (wk - 1)))

                # Velocity factor — decays after launch
                velocity_base = max(0.4, 1.0 - 0.05 * (wk - 1)) + np.random.normal(0, 0.08)

                # Fnac FR underperforming iPhone 16 Pro
                if pname == "Fnac FR" and "IPHONE-16-PRO" in pid:
                    velocity_base *= 0.72

                # MediaMarkt DE outperforming
                if pname == "MediaMarkt DE" and pid.startswith("IPHONE-16"):
                    velocity_base *= 1.15

                velocity_base = np.clip(velocity_base, 0.2, 1.4)
                units_actual = max(0, int(round(units_planned * velocity_base)))
                velocity_vs_plan = round(units_actual / max(1, units_planned), 4)

                sell_through = np.clip(velocity_base * 0.92, 0.15, 0.99)
                st_pct = round(sell_through, 4)

                # RAG
                if velocity_vs_plan >= 0.90:
                    risk_flag   = "Green"
                    risk_reason = None
                elif velocity_vs_plan >= 0.70:
                    risk_flag   = "Amber"
                    risk_reason = f"Tracking {round((1-velocity_vs_plan)*100)}% below launch plan — monitor closely"
                else:
                    risk_flag   = "Red"
                    if pname == "Fnac FR" and "IPHONE-16-PRO" in pid:
                        risk_reason = "Delayed marketing campaign; lower web traffic vs UK/DE launch"
                    else:
                        risk_reason = "Significantly below plan — escalate to Account Manager"

                rows.append({
                    "week_number":      wk,
                    "product_id":       pid,
                    "partner_id":       partner["partner_id"],
                    "units_planned":    units_planned,
                    "units_actual":     units_actual,
                    "velocity_vs_plan": velocity_vs_plan,
                    "sell_through_rate":st_pct,
                    "risk_flag":        risk_flag,
                    "risk_reason":      risk_reason,
                })

    df = pd.DataFrame(rows)
    print(f"  ✓ NPI tracker: {len(df):,} rows | {df['product_id'].nunique()} NPI products")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 7. ALERTS
# ═══════════════════════════════════════════════════════════════════════════════
def generate_alerts(products: pd.DataFrame, partners: pd.DataFrame,
                    actuals: pd.DataFrame) -> pd.DataFrame:
    """Generate business alert feed from demand signals."""
    import uuid
    from datetime import datetime

    alert_templates = [
        # (type, severity, metric, threshold, action_template, rev_impact_range)
        ("Low Stock",         "Critical", "weeks_of_supply",  2.0,
         "Increase allocation by {units} units to {partner}",           (200_000, 900_000)),
        ("Low Stock",         "Warning",  "weeks_of_supply",  3.0,
         "Monitor closely — request expedited shipment from supply chain",(50_000, 250_000)),
        ("Excess Inventory",  "Warning",  "weeks_of_supply",  8.0,
         "Reduce next week order by {units} units; consider sell-through promo", (30_000, 150_000)),
        ("Demand Spike",      "Info",     "demand_vs_avg",    1.25,
         "Pre-position additional {units} units to capture demand upside", (100_000, 500_000)),
        ("Demand Drop",       "Critical", "demand_vs_avg",    0.70,
         "Engage Account Manager — verify with {partner} within 48hrs",  (80_000, 400_000)),
        ("NPI Underperformance","Warning","velocity_vs_plan", 0.80,
         "Escalate to RM — review marketing execution with partner",     (60_000, 300_000)),
        ("Delivery Delay",    "Critical", "on_time_delivery", 0.85,
         "Escalate to logistics team — re-route {units} units",         (100_000, 600_000)),
    ]

    statuses = ["Open", "In Progress", "Resolved"]
    status_weights = [0.55, 0.25, 0.20]

    rows = []
    # Get recent actuals for context
    recent = actuals[actuals["date"] >= pd.Timestamp("2025-07-01")]

    # Generate 40-60 alerts
    n_alerts = 52
    selected_prods   = np.random.choice(products["product_id"].values, n_alerts)
    selected_partners = np.random.choice(partners["partner_id"].values, n_alerts)

    for i in range(n_alerts):
        template = alert_templates[i % len(alert_templates)]
        atype, severity, metric, threshold, action_tmpl, rev_range = template

        pid    = selected_prods[i]
        partid = selected_partners[i]
        pname  = partners[partners["partner_id"] == partid]["partner_name"].values
        pname  = pname[0] if len(pname) > 0 else "Unknown Partner"

        prod_info = products[products["product_id"] == pid]
        asp = prod_info["asp"].values[0] if not prod_info.empty else 999

        # Random metric value that breaches threshold
        if metric in ["weeks_of_supply", "on_time_delivery", "velocity_vs_plan"]:
            metric_val = round(threshold * np.random.uniform(0.4, 0.95), 2)
        else:
            metric_val = round(threshold * np.random.uniform(1.1, 1.5), 2)

        chase_units = np.random.randint(50, 500)
        action = action_tmpl.replace("{partner}", pname).replace("{units}", str(chase_units))
        rev_impact = round(np.random.uniform(*rev_range), 2)

        hours_ago = np.random.randint(1, 96)
        gen_time  = datetime(2025, 9, 15, 9, 0) - timedelta(hours=hours_ago)

        rows.append({
            "alert_id":           f"ALT-{str(uuid.uuid4())[:8].upper()}",
            "date_generated":     gen_time,
            "alert_type":         atype,
            "severity":           severity,
            "product_id":         pid,
            "partner_id":         partid,
            "metric_name":        metric,
            "metric_value":       metric_val,
            "threshold":          threshold,
            "recommended_action": action,
            "revenue_impact":     rev_impact,
            "status":             np.random.choice(statuses, p=status_weights),
        })

    # Force a few specific critical alerts
    critical_scenarios = [
        {
            "alert_id": "ALT-FNAC-001",
            "date_generated": datetime(2025, 9, 12, 8, 30),
            "alert_type": "NPI Underperformance",
            "severity": "Critical",
            "product_id": "IPHONE-16-PRO-256",
            "partner_id": "PARTNER-003",
            "metric_name": "velocity_vs_plan",
            "metric_value": 0.77,
            "threshold": 0.90,
            "recommended_action": "Escalate to Fnac FR Account Manager — joint marketing intervention required. Delayed campaign execution identified.",
            "revenue_impact": 420_000.00,
            "status": "Open",
        },
        {
            "alert_id": "ALT-CURRYS-001",
            "date_generated": datetime(2025, 9, 14, 7, 15),
            "alert_type": "Low Stock",
            "severity": "Critical",
            "product_id": "IPHONE-16-PRO-256",
            "partner_id": "PARTNER-002",
            "metric_name": "weeks_of_supply",
            "metric_value": 1.8,
            "threshold": 2.0,
            "recommended_action": "Increase allocation by 2,400 units (€2.4M) to Currys UK immediately — spring promo window closes W14.",
            "revenue_impact": 890_000.00,
            "status": "Open",
        },
        {
            "alert_id": "ALT-HNI-001",
            "date_generated": datetime(2025, 9, 13, 10, 0),
            "alert_type": "Low Stock",
            "severity": "Warning",
            "product_id": "IPAD-AIR-M3-11-128",
            "partner_id": "PARTNER-013",
            "metric_name": "in_stock_rate",
            "metric_value": 0.72,
            "threshold": 0.90,
            "recommended_action": "Harvey Norman IE: Ranging gap on iPad Air — allocate minimum 300 units to restore in-stock rate to >90%.",
            "revenue_impact": 180_000.00,
            "status": "Open",
        },
    ]
    rows.extend(critical_scenarios)

    df = pd.DataFrame(rows)
    df["date_generated"] = pd.to_datetime(df["date_generated"])
    df = df.sort_values("date_generated", ascending=False).reset_index(drop=True)
    print(f"  ✓ Alerts: {len(df)} total | {(df['severity']=='Critical').sum()} Critical | "
          f"€{df['revenue_impact'].sum()/1e6:.1f}M total revenue at risk")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    print("\n🍎  Apple Demand Planner — Synthetic Data Generator")
    print("=" * 55)

    print("\n[1/7] Generating Products...")
    products = generate_products()
    products.to_csv(os.path.join(RAW_DIR, "products.csv"), index=False)

    print("\n[2/7] Generating Reseller Partners...")
    partners = generate_partners()
    partners.to_csv(os.path.join(RAW_DIR, "reseller_partners.csv"), index=False)

    print("\n[3/7] Generating Demand Actuals (104 weeks)...")
    actuals = generate_demand_actuals(products, partners)
    actuals.to_csv(os.path.join(RAW_DIR, "demand_actuals.csv"), index=False)

    print("\n[4/7] Generating Forecasts (12 weeks forward)...")
    forecasts = generate_forecasts(products, partners, actuals)
    forecasts.to_csv(os.path.join(RAW_DIR, "forecasts.csv"), index=False)

    print("\n[5/7] Generating Order Book...")
    order_book = generate_order_book(products, partners, actuals)
    order_book.to_csv(os.path.join(RAW_DIR, "order_book.csv"), index=False)

    print("\n[6/7] Generating NPI Tracker...")
    npi = generate_npi_tracker(products, partners)
    npi.to_csv(os.path.join(RAW_DIR, "npi_tracker.csv"), index=False)

    print("\n[7/7] Generating Alerts...")
    alerts = generate_alerts(products, partners, actuals)
    alerts.to_csv(os.path.join(RAW_DIR, "alerts.csv"), index=False)

    # ── Processed summaries ────────────────────────────────────────────────────
    print("\n📊  Generating processed summaries...")

    # Demand features
    feat = actuals.merge(products[["product_id","product_family","lifecycle_stage","priority_tier","asp"]], on="product_id")
    feat = feat.merge(partners[["partner_id","partner_name","partner_tier","country"]], on="partner_id")
    feat.to_csv(os.path.join(PROCESSED_DIR, "demand_features.csv"), index=False)

    # Forecast results (Ensemble only)
    ens = forecasts[forecasts["forecast_model"] == "Ensemble"].copy()
    ens.to_csv(os.path.join(PROCESSED_DIR, "forecast_results.csv"), index=False)

    # Alert summary
    alert_summary = alerts.groupby(["severity","alert_type"]).agg(
        count=("alert_id","count"),
        total_revenue_impact=("revenue_impact","sum"),
        open_count=("status", lambda x: (x=="Open").sum())
    ).reset_index()
    alert_summary.to_csv(os.path.join(PROCESSED_DIR, "alert_summary.csv"), index=False)

    print("\n✅  All datasets generated successfully!")
    print(f"    Raw data: {RAW_DIR}")
    print(f"    Processed: {PROCESSED_DIR}")
    print("\n" + "=" * 55)
    print(f"    Total rows generated: {len(products)+len(partners)+len(actuals)+len(forecasts)+len(order_book)+len(npi)+len(alerts):,}")


if __name__ == "__main__":
    main()
