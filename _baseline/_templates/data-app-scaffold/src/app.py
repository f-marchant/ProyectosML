"""
app.py — Punto de entrada de la Data App / Dashboard MVP.
Metodología ICM + Impeccable Design System.
"""

from pathlib import Path
import streamlit as st

from src.data_loader import load_data, filter_data
from src.components.kpis import render_kpi_row
from src.components.charts import render_timeline_chart, render_category_distribution
from src.components.filters import render_sidebar_filters


def load_custom_css():
    """Inyecta el archivo de estilos custom.css para aplicar la estética Impeccable."""
    css_path = Path(__file__).resolve().parent / "styles" / "custom.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="{{PROJECT_NAME}} — Dashboard MVP",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_custom_css()

    # Encabezado principal
    st.markdown("## {{PROJECT_NAME}}")
    st.caption("{{PROJECT_DESCRIPTION}} | Diseñado bajo Metodología ICM e Impeccable UI")

    # 1. Cargar datos
    df_raw = load_data()

    # 2. Filtros de navegación
    selected_cats, selected_status = render_sidebar_filters(df_raw)
    df_filtered = filter_data(df_raw, categories=selected_cats, status_filter=selected_status)

    if df_filtered.empty:
        st.warning("⚠️ No se encontraron registros para los filtros seleccionados.")
        return

    # 3. Fila superior de KPIs
    render_kpi_row(df_filtered)

    st.markdown("---")

    # 4. Gráficos interactivos en dos columnas
    col_left, col_right = st.columns([6, 4])

    with col_left:
        render_timeline_chart(df_filtered)

    with col_right:
        render_category_distribution(df_filtered)

    st.markdown("---")

    # 5. Tabla de detalle colapsable / accesible
    with st.expander("🔍 Explorar Datos Detallados", expanded=False):
        st.dataframe(df_filtered, use_container_width=True)


if __name__ == "__main__":
    main()
