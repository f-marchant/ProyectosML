"""
test_data_loader.py — Pruebas unitarias de carga y filtrado de datos.
"""

from pathlib import Path
import pandas as pd
from src.data_loader import load_data, filter_data


def test_load_sample_data():
    """Verifica que el dataset de muestra cargue correctamente y contenga las columnas requeridas."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample" / "sample_data.csv"
    assert sample_path.exists(), "El archivo sample_data.csv debe existir."

    df = load_data(str(sample_path))
    assert not df.empty, "El dataframe no debe estar vacío."
    assert "date" in df.columns
    assert "metric_primary" in df.columns
    assert "category" in df.columns
    assert "status" in df.columns


def test_filter_data_by_category():
    """Verifica el filtrado correcto por categoría."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample" / "sample_data.csv"
    df = load_data(str(sample_path))

    filtered = filter_data(df, categories=["Segment_A"])
    assert len(filtered) > 0
    assert set(filtered["category"].unique()) == {"Segment_A"}


def test_filter_data_empty():
    """Verifica que un filtro inexistente devuelva un dataframe vacío sin lanzar excepción."""
    sample_path = Path(__file__).resolve().parent.parent / "data" / "sample" / "sample_data.csv"
    df = load_data(str(sample_path))

    filtered = filter_data(df, categories=["NonExistent"])
    assert filtered.empty
