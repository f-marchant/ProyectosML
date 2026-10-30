"""
charts.py — Visualizaciones interactivas Plotly respetando DESIGN.md.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

COLOR_SKY = "#38BDF8"
COLOR_EMERALD = "#34D399"
COLOR_RED = "#F87171"
COLOR_MUTED = "#94A3B8"
COLOR_GRID = "rgba(148, 163, 184, 0.12)"


def _apply_theme(fig: go.Figure):
    """Aplica tokens visuales de DESIGN.md a cualquier figura Plotly."""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
            color="#F1F5F9",
            size=12
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLOR_GRID,
            linecolor=COLOR_GRID,
            tickfont=dict(color=COLOR_MUTED)
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLOR_GRID,
            linecolor=COLOR_GRID,
            tickfont=dict(color=COLOR_MUTED)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=COLOR_MUTED)
        )
    )
    return fig


def render_timeline_chart(df: pd.DataFrame):
    """Renderiza evolución temporal de la métrica principal."""
    if "date" not in df.columns or "metric_primary" not in df.columns:
        st.info("Sin datos temporales para visualizar.")
        return

    df_sorted = df.sort_values("date")
    fig = px.line(
        df_sorted,
        x="date",
        y="metric_primary",
        color="category" if "category" in df.columns else None,
        markers=True,
        title="Tendencia Temporal de Métrica Principal",
        color_discrete_sequence=[COLOR_SKY, COLOR_EMERALD, "#A78BFA"]
    )
    _apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)


def render_category_distribution(df: pd.DataFrame):
    """Renderiza distribución por categoría."""
    if "category" not in df.columns or "metric_primary" not in df.columns:
        return

    cat_agg = df.groupby("category", as_index=False)["metric_primary"].sum()

    fig = px.bar(
        cat_agg,
        x="category",
        y="metric_primary",
        title="Distribución por Categoría",
        color="category",
        color_discrete_sequence=[COLOR_SKY, COLOR_EMERALD, "#A78BFA"]
    )
    _apply_theme(fig)
    fig.update_traces(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
