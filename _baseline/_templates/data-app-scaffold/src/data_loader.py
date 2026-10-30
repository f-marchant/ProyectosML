"""
data_loader.py — Módulo desacoplado de ingesta y transformación de datos para la UI.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Carga el dataset de la aplicación con caché en memoria.
    Si no se provee ruta, carga el dataset de muestra local.
    """
    if file_path is None:
        base_dir = Path(__file__).resolve().parent.parent
        file_path = str(base_dir / "data" / "sample" / "sample_data.csv")

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de datos en: {file_path}")

    df = pd.read_csv(path)

    # Validaciones y conversiones mínimas
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])

    return df


def filter_data(
    df: pd.DataFrame,
    categories: Optional[list] = None,
    status_filter: Optional[list] = None
) -> pd.DataFrame:
    """
    Aplica filtros declarativos sobre el dataframe en memoria.
    """
    filtered = df.copy()

    if categories:
        filtered = filtered[filtered["category"].isin(categories)]

    if status_filter:
        filtered = filtered[filtered["status"].isin(status_filter)]

    return filtered
