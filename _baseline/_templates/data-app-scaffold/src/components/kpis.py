"""
kpis.py — Renderizado de métricas y KPIs clave con jerarquía limpia.
"""

import pandas as pd
import streamlit as st


def render_kpi_row(df: pd.DataFrame):
    """
    Renderiza la fila superior de KPIs sin recargar la página.
    """
    total_records = len(df)
    total_volume = df["metric_primary"].sum() if "metric_primary" in df.columns else 0
    avg_score = df["metric_secondary"].mean() if "metric_secondary" in df.columns else 0
    critical_count = (df["status"] == "Critical").sum() if "status" in df.columns else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Total Registros", value=f"{total_records:,}")

    with col2:
        st.metric(label="Volumen Primario", value=f"${total_volume:,.0f}")

    with col3:
        st.metric(label="Score Promedio", value=f"{avg_score:.2%}")

    with col4:
        st.metric(
            label="Casos Críticos",
            value=f"{critical_count}",
            delta=f"{critical_count} alertas" if critical_count > 0 else "0 alertas",
            delta_color="inverse"
        )
