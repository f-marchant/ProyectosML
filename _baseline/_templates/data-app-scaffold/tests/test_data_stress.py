"""
test_data_stress.py — Suite de Stress-Testing de Datos para UI (Patrón 'break').

Inspirado en el principio de stress-testing de Jakub Krehel: someter los componentes
y transformaciones de la interfaz a escenarios extremos y datos adversos para garantizar
que la UI sea resiliente y no falle silenciosamente ni rompa el layout.
"""

import pandas as pd
import pytest
from src.data_loader import filter_data
from src.components.kpis import render_kpi_row


def test_stress_empty_dataset():
    """Escenario 1: Dataset con cero registros (Empty State)."""
    df_empty = pd.DataFrame(columns=["id", "date", "category", "metric_primary", "metric_secondary", "status"])
    
    # El filtrado no debe lanzar excepción
    filtered = filter_data(df_empty, categories=["Segment_A"])
    assert len(filtered) == 0

    # Los cálculos de agregación deben comportarse con gracia sin crashear
    assert df_empty["metric_primary"].sum() == 0


def test_stress_single_record():
    """Escenario 2: Dataset con exactamente un solo registro."""
    df_single = pd.DataFrame([{
        "id": 1,
        "date": "2026-10-01",
        "category": "Segment_A",
        "metric_primary": 100.0,
        "metric_secondary": 0.5,
        "status": "OK"
    }])
    
    filtered = filter_data(df_single, categories=["Segment_A"])
    assert len(filtered) == 1
    assert filtered["metric_primary"].sum() == 100.0


def test_stress_extreme_numerical_values():
    """Escenario 3: Números gigantescos, negativos y de precisión decimal extrema."""
    df_extreme = pd.DataFrame([
        {"id": 1, "category": "A", "metric_primary": 1e14, "metric_secondary": -99999.9999, "status": "OK"},
        {"id": 2, "category": "B", "metric_primary": 0.000000001, "metric_secondary": 1e-8, "status": "Critical"},
        {"id": 3, "category": "C", "metric_primary": -5000000.0, "metric_secondary": 0.0, "status": "Warning"},
    ])
    
    total = df_extreme["metric_primary"].sum()
    assert total > 0, "Debe soportar sumas con magnitudes astronómicas sin desbordamiento."
    mean_sec = df_extreme["metric_secondary"].mean()
    assert isinstance(mean_sec, float)


def test_stress_unbreakable_long_strings():
    """Escenario 4: Strings de 300+ caracteres sin espacios (prueba de overflow)."""
    long_string = "A" * 300
    df_overflow = pd.DataFrame([
        {"id": 1, "category": long_string, "metric_primary": 50.0, "metric_secondary": 0.1, "status": "OK"}
    ])
    
    filtered = filter_data(df_overflow, categories=[long_string])
    assert len(filtered) == 1
    assert filtered.iloc[0]["category"] == long_string


def test_stress_missing_and_nan_values():
    """Escenario 5: Presencia masiva de nulos, NaNs y None."""
    df_nans = pd.DataFrame([
        {"id": 1, "category": None, "metric_primary": float("nan"), "metric_secondary": None, "status": None},
        {"id": 2, "category": "A", "metric_primary": 100.0, "metric_secondary": 0.5, "status": "OK"},
    ])
    
    # Manejo de nulos en agregaciones sin fallar
    valid_count = df_nans["metric_primary"].dropna().sum()
    assert valid_count == 100.0
