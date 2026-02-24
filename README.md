# 🍎 Apple Reseller Channel — Demand Planning & Inventory Intelligence Platform

> *End-to-end demand planning and reseller channel intelligence platform for Apple's EMEA operations*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/charts-Plotly-3F4F75)](https://plotly.com)

---

## 🏠 Live Demo

**[→ Launch Dashboard on Streamlit Cloud](https://apple-demand-planner.streamlit.app)** *(deploy after cloning)*

---

## 📸 Dashboard Preview

| Executive Overview | Demand Forecast |
|---|---|
| 6 KPI cards, revenue trend, partner ranking | Cascading filters, forecast vs actuals, model comparison |

| NPI Launch Tracker | Risk & Alerts |
|---|---|
| Velocity vs plan, RAG scorecard, waterfall | Alert feed, risk matrix, top-10 actions |

---

## 🎯 Business Context

Apple's EMEA Reseller Operations team manages hundreds of millions of euros in weekly channel revenue across 13+ reseller partners in 10 countries. This platform simulates the full demand planning cycle:

- **Weekly demand forecasting** with 4-model ensemble (SARIMA, Prophet, Random Forest, Ensemble)
- **Order book management** — identifying chase opportunities, fulfilment gaps, and at-risk orders
- **NPI launch tracking** — velocity vs plan with real-time RAG status across the partner network
- **Early alert system** — statistical anomaly detection with revenue-quantified action priorities
- **Partner deep dive** — full 360° view per reseller across demand, order book, NPI, and alerts

Every insight is quantified in euros. Every recommendation is specific and actionable.

---

## 📊 Key Findings

| Metric | Value | Insight |
|--------|-------|---------|
| **Forecast Accuracy** | **91.3% WMAPE** | Ensemble model across 40 SKUs and 13 EMEA partners |
| **Chase Opportunity** | **€26.1M** | Identified across 8 partners in current order book |
| **NPI Performance** | **107% vs plan** | iPhone 16 overall — Fnac FR flagged at 77%, escalation in progress |
| **Revenue at Risk** | **€16.2M** | From 24 critical + 12 warning open alerts |
| **Ranging Gap** | **€180K/quarter** | Harvey Norman IE: 72% in-stock on iPad Air vs 97% on iPhone |

---

## 🏗️ Key Features

### 📈 Demand Forecasting Engine
4 models built and compared with expanding-window time-series cross-validation:
- **SARIMA** — seasonal ARIMA optimised by AIC (88.5% accuracy)
- **Prophet** — with custom NPI/holiday regressors (90.2%)
- **Random Forest** — with lag features (1,2,4,8,12 weeks), rolling means, seasonality indicators (89.7%)
- **Ensemble** — weighted average by trailing 8-week WMAPE per SKU group (**91.3%**)

### 📦 Order Book & Shipment Planning
- Live order book health with fulfilment rate, at-risk %, and chase opportunity radar
- Chase opportunity identification: sell-through > 85% AND WoS < 3 → quantified in €
- Weekly shipment plan validation vs forecast by product family
- In-stock heatmap (partner × product family) with weeks-of-supply histogram

### 🚀 NPI Launch Intelligence
- Multi-line velocity chart: actual vs plan vs prior generation
- Partner RAG scorecard grid with root cause narratives
- Launch waterfall: plan → partner variances → actual
- Tracks iPhone 16 across 13 partners from Week 1

### ⚠️ Early Alert & Risk System
- Statistical anomaly detection (Z-score + IQR) on weekly demand signals
- Risk matrix: likelihood × revenue impact scatter per SKU-partner
- 55 auto-generated alerts with severity, revenue impact, and recommended action
- Top-10 actions table sorted by revenue impact

### 🤝 Partner Deep Dive
- 360° partner view across 5 tabs: Overview, Demand, Order Book, NPI, Alerts
- Auto-generated 3-bullet business insights per partner
- Revenue trend (2 years), product mix donut, alert feed

---

## 🔬 Technical Architecture

### Data Pipeline
```
src/data_generator.py
    → data/raw/products.csv          (40 SKUs, realistic ASPs)
    → data/raw/reseller_partners.csv (13 EMEA partners)
    → data/raw/demand_actuals.csv    (104 weeks × product × partner = 53,259 rows)
    → data/raw/forecasts.csv         (12 weeks × 4 models = 24,960 rows)
    → data/raw/order_book.csv        (348 active orders)
    → data/raw/npi_tracker.csv       (316 rows, 14 NPI products)
    → data/raw/alerts.csv            (55 alerts, €16.2M at risk)
```

### Stack
| Layer | Technology |
|-------|-----------|
| Data Generation | `pandas`, `numpy`, custom seasonality engine |
| Forecasting | `statsmodels` (SARIMA), `prophet`, `scikit-learn` (RF) |
| Dashboard | `streamlit 1.32`, Apple CSS design system |
| Charts | `plotly 5.22` — all styled to Apple design spec |
| Deployment | Streamlit Cloud (free tier) |

### Data Realism
- **Seasonality**: iPhone launch spike W37-W42 (+340%), holiday W47-W52 (+180%), BTS W33-W37 (+60%)
- **NPI curves**: Log-decay normalisation from launch peak over 12 weeks
- **Supply constraints**: 12% of weeks have `units_shipped < units_ordered`
- **Partner distribution**: Pareto — MediaMarkt DE is 20× Harvey Norman IE by revenue
- **Accessory correlation**: 0.6-0.8 with iPhone demand, 1-2 week lag

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/MohammedKaifAhmed/apple-demand-planner
cd apple-demand-planner

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate all synthetic data
python src/data_generator.py

# 4. Launch the dashboard
streamlit run app/streamlit_app.py
```

Open **http://localhost:8501** in your browser.

### Notebook Order
```
00_data_generation.ipynb    → Data validation
01_demand_forecasting.ipynb → 4-model build + evaluation
02_order_book_management.ipynb
03_npi_launch_tracker.ipynb
04_early_alerts_risk.ipynb
```

---

## 📁 Project Structure

```
apple-demand-planner/
├── data/raw/              ← Generated CSVs (gitignored)
├── src/
│   ├── data_generator.py  ← Full synthetic dataset generator
│   ├── utils/
│   │   ├── apple_charts.py   ← Plotly Apple design templates
│   │   └── helpers.py        ← Data loaders, KPI calcs, formatters
│   ├── forecasting/       ← ARIMA, Prophet, RF, Ensemble modules
│   └── analytics/         ← Order book, NPI, alerts, partner logic
├── app/
│   ├── streamlit_app.py   ← Executive Overview (Page 1)
│   ├── pages/             ← 5 sub-pages
│   ├── components/        ← KPI cards, charts, alert feed
│   └── styles/apple_theme.css ← Full Apple design system
└── notebooks/             ← 5 analytical notebooks
```

---

## 👤 Author

**Mohammed Kaif Ahmed**  
MSc Strategy & Innovation Management, DCU Business School  
[LinkedIn](www.linkedin.com/in/kaif-ahmed-bb972421a) · [GitHub](https://github.com/Kaif198)

*Built as a portfolio demonstration for the Apple Demand Planner role, EMEA Reseller Operations, Cork.*

---

*"Designed by Apple in California" — this platform emulates the aesthetic and analytical rigour of internal Apple operational tooling.*
