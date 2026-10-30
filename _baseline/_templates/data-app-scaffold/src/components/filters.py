"""
filters.py — Controles de filtrado interactivo en la barra lateral.
"""

from typing import Tuple
import pandas as pd
import streamlit as st


def render_sidebar_filters(df: pd.DataFrame) -> Tuple[list, list]:
    """
    Renderiza los filtros en el sidebar y retorna las selecciones del usuario.
    """
    st.sidebar.markdown("### Filtros de Exploración")

    categories = sorted(df["category"].dropna().unique().tolist()) if "category" in df.columns else []
    statuses = sorted(df["status"].dropna().unique().tolist()) if "status" in df.columns else []

    selected_categories = st.sidebar.multiselect(
        "Segmentos / Categorías",
        options=categories,
        default=categories
    )

    selected_statuses = st.sidebar.multiselect(
        "Estado del Registro",
        options=statuses,
        default=statuses
    )

    return selected_categories, selected_statuses
