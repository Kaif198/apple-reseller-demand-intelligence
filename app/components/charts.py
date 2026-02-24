"""
Charts Component — thin Streamlit wrappers for src/utils/apple_charts functions.
Author: Mohammed Kaif Ahmed
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.utils.apple_charts import (
    apple_chart_layout, revenue_trend_chart, product_mix_donut,
    partner_ranking_bar, forecast_accuracy_bar, forecast_line_chart,
    instock_heatmap, wos_histogram, npi_velocity_chart, risk_matrix_scatter,
)


def show_chart(fig: go.Figure, use_container_width: bool = True) -> None:
    """Render a plotly figure with consistent config."""
    st.plotly_chart(fig, use_container_width=use_container_width,
                    config={"displayModeBar": False})
