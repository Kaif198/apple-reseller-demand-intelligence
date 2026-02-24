"""
Apple Charts — Plotly Chart Templates with Apple Design System
All chart functions return pre-styled go.Figure objects.
Author: Mohammed Kaif Ahmed
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ─── Apple Design Tokens ───────────────────────────────────────────────────────

APPLE_FONT = (
    "Inter, -apple-system, BlinkMacSystemFont, 'SF Pro Display', "
    "'SF Pro Text', 'Helvetica Neue', Arial, sans-serif"
)

# backward-compat aliases
FONT_STACK = APPLE_FONT
FONT_SIZE_AXIS       = 11
FONT_SIZE_ANNOTATION = 11
FONT_SIZE_LEGEND     = 12
TEXT_PRIMARY   = "#1D1D1F"
TEXT_SECONDARY = "#6E6E73"
TEXT_TERTIARY  = "#86868B"
BG_WHITE       = "#FFFFFF"
GRID_COLOR     = "#F2F2F4"
AXIS_COLOR     = "#E8E8ED"
LINE_WIDTH_PRIMARY   = 2.5
LINE_WIDTH_SECONDARY = 2.0
LINE_WIDTH_GRID      = 1
MARGIN_LEFT   = 16
MARGIN_RIGHT  = 16
MARGIN_TOP    = 24
MARGIN_BOTTOM = 16

APPLE_COLORS = {
    "iPhone":      "#0071E3",
    "iPad":        "#34C759",
    "Mac":         "#FF9500",
    "Apple Watch": "#FF3B30",
    "AirPods":     "#AF52DE",
    "Accessories": "#8E8E93",
}

SERIES_COLORS = {
    "actual":      "#1D1D1F",
    "forecast":    "#0071E3",
    "upper_lower": "#6E6E73",
    "plan":        "#FF9500",
    "ci_fill":     "rgba(0,113,227,0.08)",
}


# ─── Internal base layout ─────────────────────────────────────────────────────

def _apple_layout(fig: go.Figure, title: str = None, subtitle: str = None,
                  height: int = 380, show_legend: bool = True) -> go.Figure:
    """Apply full Apple design system to any Plotly figure."""
    title_text = None
    if title and subtitle:
        title_text = (
            f"<b>{title}</b><br>"
            f"<span style='font-size:13px;color:{TEXT_SECONDARY};font-weight:400'>"
            f"{subtitle}</span>"
        )
    elif title:
        title_text = f"<b>{title}</b>"

    fig.update_layout(
        font=dict(family=APPLE_FONT, color=TEXT_PRIMARY, size=13),
        plot_bgcolor=BG_WHITE,
        paper_bgcolor=BG_WHITE,
        height=height,
        margin=dict(l=MARGIN_LEFT, r=MARGIN_RIGHT,
                    t=72 if title else MARGIN_TOP, b=MARGIN_BOTTOM),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor=AXIS_COLOR,
            font=dict(family=APPLE_FONT, size=13, color=TEXT_PRIMARY),
        ),
        showlegend=show_legend,
        legend=dict(
            title=dict(text=""),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=FONT_SIZE_LEGEND, color=TEXT_SECONDARY),
            bgcolor="rgba(0,0,0,0)", itemsizing="constant",
        ),
        title=dict(
            text=title_text if title_text else "",
            font=dict(size=17, color=TEXT_PRIMARY),
            x=0.01, xanchor="left", y=0.97, yanchor="top",
        ),
    )

    fig.update_xaxes(
        showgrid=False, linecolor=AXIS_COLOR, linewidth=1,
        tickfont=dict(size=FONT_SIZE_AXIS, color=TEXT_TERTIARY, family=APPLE_FONT),
        tickcolor=AXIS_COLOR, zeroline=False,
    )
    fig.update_yaxes(
        showgrid=True, gridcolor=GRID_COLOR, gridwidth=LINE_WIDTH_GRID,
        griddash="dot", linecolor=AXIS_COLOR, linewidth=1,
        tickfont=dict(size=FONT_SIZE_AXIS, color=TEXT_TERTIARY, family=APPLE_FONT),
        zeroline=False,
    )
    return fig


# ─── Public wrapper (backward-compat) ────────────────────────────────────────

def apple_chart_layout(fig: go.Figure, title: str = None,
                       height: int = 380) -> go.Figure:
    """Apply Apple design system to any Plotly figure."""
    return _apple_layout(fig, title=title, height=height)


# ─── Chart Functions ──────────────────────────────────────────────────────────

def revenue_trend_chart(actuals_df: pd.DataFrame,
                        forecast_df: pd.DataFrame = None,
                        title: str = None,
                        height: int = 400) -> go.Figure:
    """Area chart: actuals + forecast + CI + 'Today' marker."""
    try:
        if actuals_df.empty:
            raise ValueError("actuals_df cannot be empty")
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=actuals_df["date"], y=actuals_df["revenue"],
            mode="lines", name="Actual Revenue",
            line=dict(color=SERIES_COLORS["actual"], width=LINE_WIDTH_PRIMARY),
            fill="tozeroy", fillcolor="rgba(29,29,31,0.05)",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>Revenue: €%{y:,.0f}<extra></extra>",
        ))

        if forecast_df is not None and not forecast_df.empty:
            req = ["date", "forecast_revenue", "lower", "upper"]
            if all(c in forecast_df.columns for c in req):
                fig.add_trace(go.Scatter(
                    x=pd.concat([forecast_df["date"], forecast_df["date"][::-1]]),
                    y=pd.concat([forecast_df["upper"], forecast_df["lower"][::-1]]),
                    fill="toself", fillcolor=SERIES_COLORS["ci_fill"],
                    line=dict(color="rgba(0,0,0,0)"),
                    name="80% Confidence Interval", hoverinfo="skip",
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_df["date"], y=forecast_df["forecast_revenue"],
                    mode="lines", name="Forecast",
                    line=dict(color=SERIES_COLORS["forecast"],
                              width=LINE_WIDTH_SECONDARY, dash="dot"),
                    hovertemplate="<b>%{x|%d %b %Y}</b><br>Forecast: €%{y:,.0f}<extra></extra>",
                ))

        _td = pd.Timestamp("2025-09-15")
        fig.add_shape(type="line", x0=_td, x1=_td, y0=0, y1=0.94, yref="paper",
                      line=dict(color="#8E8E93", width=1, dash="dash"))
        fig.add_annotation(x=_td, y=0.93, yref="paper", text="Today", showarrow=False,
                           font=dict(size=FONT_SIZE_ANNOTATION, color=TEXT_SECONDARY),
                           xanchor="left", yanchor="top", xshift=4,
                           bgcolor="rgba(255,255,255,0.85)", borderpad=2)
        return _apple_layout(fig, height=height)

    except Exception as e:
        print(f"Error creating revenue trend chart: {e}")
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)[:100]}", xref="paper",
                           yref="paper", x=0.5, y=0.5, showarrow=False,
                           font=dict(size=14, color=TEXT_SECONDARY))
        return fig


def product_mix_donut(df: pd.DataFrame, value_col: str = "revenue",
                      label_col: str = "product_family",
                      center_text: str = None, height: int = 380) -> go.Figure:
    """Donut chart for product family mix."""
    grouped = df.groupby(label_col)[value_col].sum().reset_index()
    colors = [APPLE_COLORS.get(f, "#8E8E93") for f in grouped[label_col]]
    total = grouped[value_col].sum()
    center = center_text or f"€{total/1e6:.0f}M"

    fig = go.Figure(go.Pie(
        labels=grouped[label_col], values=grouped[value_col],
        hole=0.70,
        marker=dict(colors=colors, line=dict(color=BG_WHITE, width=3)),
        textinfo="percent", textposition="inside",
        textfont=dict(size=10, family=APPLE_FONT, color="white"),
        insidetextorientation="horizontal",
        hovertemplate="<b>%{label}</b><br>Revenue: €%{value:,.0f}<br>Share: %{percent}<extra></extra>",
        pull=[0.02] * len(grouped),
    ))
    fig.add_annotation(text=f"<b>{center}</b>", x=0.5, y=0.55,
                       font=dict(size=22, color=TEXT_PRIMARY, family=APPLE_FONT),
                       showarrow=False)
    fig.add_annotation(text="Total Revenue", x=0.5, y=0.40,
                       font=dict(size=11, color=TEXT_SECONDARY, family=APPLE_FONT),
                       showarrow=False)
    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(margin=dict(l=60, r=60, t=24, b=40))
    return fig


def partner_ranking_bar(df: pd.DataFrame, x_col: str = "revenue",
                        y_col: str = "partner_name",
                        color_col: str = "in_stock_rate",
                        height: int = 400) -> go.Figure:
    """Horizontal bar chart with semantic in-stock colouring."""
    df_sorted = df.sort_values(x_col, ascending=True)
    colors = []
    for rate in df_sorted[color_col]:
        if pd.isna(rate) or rate >= 0.92:
            colors.append("#34C759")
        elif rate >= 0.80:
            colors.append("#FF9500")
        else:
            colors.append("#FF3B30")

    def _fmt(v):
        if v >= 1e9: return f"€{v/1e9:.1f}B"
        return f"€{v/1e6:.0f}M"

    fig = go.Figure(go.Bar(
        x=df_sorted[x_col], y=df_sorted[y_col], orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        text=[_fmt(v) for v in df_sorted[x_col]],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(size=FONT_SIZE_AXIS, color="white", family=APPLE_FONT),
        hovertemplate="<b>%{y}</b><br>Revenue: %{text}<extra></extra>",
    ))
    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(
        xaxis=dict(title=None,
                   tickvals=[0, 1e9, 2e9, 3e9, 4e9, 5e9],
                   ticktext=["€0", "€1B", "€2B", "€3B", "€4B", "€5B"],
                   tickfont=dict(size=FONT_SIZE_AXIS, color=TEXT_TERTIARY)),
        yaxis=dict(title=None),
        bargap=0.25,
        margin=dict(l=110, r=20, t=MARGIN_TOP, b=MARGIN_BOTTOM),
    )
    return fig


def forecast_accuracy_bar(df: pd.DataFrame, x_col: str = "product_family",
                          y_col: str = "accuracy", height: int = 340) -> go.Figure:
    """Bar chart: forecast accuracy by product family with 90% target line."""
    colors = [APPLE_COLORS.get(f, "#8E8E93") for f in df[x_col]]
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col],
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)")),
        text=[f"{v:.1f}%" for v in df[y_col]], textposition="outside",
        textfont=dict(size=FONT_SIZE_AXIS, color=TEXT_PRIMARY, family=APPLE_FONT),
        hovertemplate="<b>%{x}</b><br>Accuracy: %{y:.1f}%<extra></extra>",
    ))
    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(
        yaxis=dict(range=[75, 103], ticksuffix="%"),
        xaxis=dict(title=None, tickangle=0),
        bargap=0.4,
        margin=dict(l=MARGIN_LEFT, r=MARGIN_RIGHT, t=MARGIN_TOP, b=56),
    )
    # Target line — label placed above plot area to avoid overlap with bars
    fig.add_hline(y=90, line_dash="dash", line_color=SERIES_COLORS["plan"],
                  line_width=1.5)
    fig.add_annotation(
        text="Target 90%", x=1, xref="paper", xanchor="right",
        y=90, yref="y", yanchor="bottom",
        showarrow=False,
        font=dict(size=FONT_SIZE_ANNOTATION, color=SERIES_COLORS["plan"],
                  family=APPLE_FONT),
        bgcolor="rgba(255,255,255,0.85)", borderpad=2,
        yshift=4,
    )
    return fig


def forecast_line_chart(actuals_df: pd.DataFrame, forecast_df: pd.DataFrame,
                        title: str = None, height: int = 420) -> go.Figure:
    """Actuals + Forecast + CI + today line. Used by Demand Forecast and Partner Deep Dive."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=actuals_df["date"], y=actuals_df["units_sold"],
        mode="lines", name="Actual",
        line=dict(color=SERIES_COLORS["actual"], width=LINE_WIDTH_PRIMARY),
        hovertemplate="<b>Actual</b>: %{y:,.0f} units<extra></extra>",
    ))
    if not forecast_df.empty:
        x_ci = list(forecast_df["date"]) + list(forecast_df["date"][::-1])
        y_ci = (list(forecast_df["forecast_upper"]) +
                list(forecast_df["forecast_lower"][::-1]))
        fig.add_trace(go.Scatter(
            x=x_ci, y=y_ci, fill="toself",
            fillcolor=SERIES_COLORS["ci_fill"],
            line=dict(color="rgba(0,0,0,0)"),
            name="80% CI", showlegend=True, hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=forecast_df["date"], y=forecast_df["forecast_units"],
            mode="lines", name="Forecast",
            line=dict(color=SERIES_COLORS["forecast"],
                      width=LINE_WIDTH_SECONDARY, dash="dot"),
            hovertemplate="<b>Forecast</b>: %{y:,.0f} units<extra></extra>",
        ))
    _td = pd.Timestamp("2025-09-15")
    fig.add_shape(type="line", x0=_td, x1=_td, y0=0, y1=1, yref="paper",
                  line=dict(color="#8E8E93", width=1, dash="dash"))
    fig.add_annotation(x=_td, y=0.98, yref="paper", text="Today", showarrow=False,
                       font=dict(size=10, color=TEXT_SECONDARY, family=APPLE_FONT),
                       xanchor="left", yanchor="top",
                       bgcolor="rgba(255,255,255,0.9)")
    return _apple_layout(fig, title=title, height=height)


def instock_heatmap(df: pd.DataFrame, height: int = 400) -> go.Figure:
    """Heatmap: in-stock rates by partner × product family."""
    pivot = (df.groupby(["partner_name", "product_family"])["in_stock_rate"]
               .mean().unstack(fill_value=np.nan))
    color_scale = [[0.0, "#FF3B30"], [0.5, "#FF9500"],
                   [0.8, "#34C759"], [1.0, "#1B7D36"]]
    fig = go.Figure(go.Heatmap(
        z=pivot.values * 100, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=color_scale, zmin=60, zmax=100,
        text=[[f"{v:.1f}%" if not np.isnan(v) else "N/A" for v in row]
              for row in pivot.values * 100],
        texttemplate="%{text}",
        textfont=dict(size=FONT_SIZE_ANNOTATION, family=APPLE_FONT, color="#1D1D1F"),
        hovertemplate="<b>%{y}</b> — <b>%{x}</b><br>In-Stock: %{z:.1f}%<extra></extra>",
        colorbar=dict(title="In-Stock %", ticksuffix="%",
                      titlefont=dict(size=FONT_SIZE_AXIS, family=APPLE_FONT),
                      tickfont=dict(size=FONT_SIZE_ANNOTATION, family=APPLE_FONT),
                      thickness=12, outlinewidth=0),
    ))
    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(margin=dict(l=140, r=40, t=20, b=60))
    return fig


def wos_histogram(df: pd.DataFrame, height: int = 340) -> go.Figure:
    """Weeks of supply histogram with zone markers."""
    fig = go.Figure(go.Histogram(
        x=df["weeks_of_supply"], nbinsx=30,
        marker=dict(color="#0071E3", line=dict(color=BG_WHITE, width=0.5)),
        hovertemplate="WoS: %{x:.1f} weeks<br>Count: %{y}<extra></extra>",
        name="SKU-Partner pairs",
    ))
    fig.add_vrect(x0=0, x1=2, fillcolor="rgba(255,59,48,0.06)", opacity=1,
                  line_width=0, annotation_text="Under-stocked",
                  annotation_position="top left",
                  annotation_font=dict(size=10, color="#FF3B30"))
    fig.add_vrect(x0=2, x1=6, fillcolor="rgba(52,199,89,0.06)", opacity=1,
                  line_width=0, annotation_text="Healthy",
                  annotation_position="top left",
                  annotation_font=dict(size=10, color="#34C759"))
    fig.add_vrect(x0=6, x1=12, fillcolor="rgba(255,149,0,0.06)", opacity=1,
                  line_width=0, annotation_text="Over-stocked",
                  annotation_position="top left",
                  annotation_font=dict(size=10, color="#FF9500"))
    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(xaxis=dict(title="Weeks of Supply"),
                      yaxis=dict(title="Count"))
    return fig


def npi_velocity_chart(actual_df: pd.DataFrame, plan_df: pd.DataFrame,
                       prior_df: pd.DataFrame = None, height: int = 400) -> go.Figure:
    """Multi-line NPI velocity: actual vs plan vs prior gen."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plan_df["week_number"], y=plan_df["units_planned"],
        mode="lines", name="Plan",
        line=dict(color=SERIES_COLORS["plan"], width=2, dash="dash"),
        hovertemplate="Week %{x} Plan: %{y:,.0f} units<extra></extra>",
    ))
    if prior_df is not None and not prior_df.empty:
        fig.add_trace(go.Scatter(
            x=prior_df["week_number"], y=prior_df["units_actual"],
            mode="lines", name="Prior Gen (Actual)",
            line=dict(color=SERIES_COLORS["upper_lower"], width=2, dash="dash"),
            hovertemplate="Week %{x} Prior Gen: %{y:,.0f} units<extra></extra>",
        ))
    fig.add_trace(go.Scatter(
        x=actual_df["week_number"], y=actual_df["units_actual"],
        mode="lines+markers", name="Current Gen (Actual)",
        line=dict(color=SERIES_COLORS["actual"], width=LINE_WIDTH_PRIMARY),
        marker=dict(size=6, color=SERIES_COLORS["actual"],
                    line=dict(color=BG_WHITE, width=1.5)),
        hovertemplate="Week %{x} Actual: %{y:,.0f} units<extra></extra>",
    ))
    return _apple_layout(fig, height=height)


def risk_matrix_scatter(df: pd.DataFrame, height: int = 420) -> go.Figure:
    """Risk matrix scatter with quadrant shading."""
    fig = go.Figure()
    # Quadrant backgrounds
    fig.add_shape(type="rect", x0=0, y0=0, x1=50, y1=0.5, yref="paper",
                  fillcolor="rgba(52,199,89,0.05)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=50, y0=0, x1=100, y1=0.5, yref="paper",
                  fillcolor="rgba(255,149,0,0.05)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=0, y0=0.5, x1=50, y1=1, yref="paper",
                  fillcolor="rgba(255,149,0,0.05)", line=dict(width=0), layer="below")
    fig.add_shape(type="rect", x0=50, y0=0.5, x1=100, y1=1, yref="paper",
                  fillcolor="rgba(255,59,48,0.05)", line=dict(width=0), layer="below")

    family_colors = [
        APPLE_COLORS.get(f, "#8E8E93")
        for f in df.get("product_family", ["Accessories"] * len(df))
    ]
    fig.add_trace(go.Scatter(
        x=df["likelihood"] * 100, y=df["revenue_impact"],
        mode="markers",
        marker=dict(size=11, color=family_colors,
                    line=dict(color=BG_WHITE, width=2), opacity=0.85),
        text=df.get("label", df.get("product_id", "")),
        hovertemplate=(
            "<b>%{text}</b><br>Likelihood: %{x:.0f}%<br>"
            "Revenue Impact: €%{y:,.0f}<extra></extra>"
        ),
    ))
    fig.add_hline(y=df["revenue_impact"].median(),
                  line_dash="dot", line_color=AXIS_COLOR, line_width=1)
    fig.add_vline(x=50, line_dash="dot", line_color=AXIS_COLOR, line_width=1)

    q10 = df["revenue_impact"].quantile(0.10)
    q85 = df["revenue_impact"].quantile(0.85)
    for label, x, y in [("Monitor", 15, q10), ("Watch", 75, q10),
                         ("Act", 15, q85), ("Escalate", 75, q85)]:
        fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>",
                           font=dict(size=FONT_SIZE_ANNOTATION, color=TEXT_TERTIARY,
                                     family=APPLE_FONT),
                           showarrow=False, bgcolor="rgba(245,245,247,0.85)",
                           opacity=0.7)

    _apple_layout(fig, height=height, show_legend=False)
    fig.update_layout(
        xaxis=dict(title="Likelihood of Occurrence (%)",
                   ticksuffix="%", range=[0, 100]),
        yaxis=dict(title="Revenue Impact (€)", tickprefix="€"),
    )
    return fig


def alert_resolution_trend(df: pd.DataFrame, height: int = 320) -> go.Figure:
    """Line chart: open vs resolved alerts over time."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["open"], mode="lines", name="Open",
        line=dict(color="#FF3B30", width=2),
        fill="tozeroy", fillcolor="rgba(255,59,48,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["resolved"], mode="lines", name="Resolved",
        line=dict(color="#34C759", width=2),
    ))
    return _apple_layout(fig, height=height)
