"""
test_data_leakage.py — Validación metodológica de prevención de Data Leakage.

Verifica que las transformaciones, escaladores o imputadores se ajusten (fit)
exclusivamente sobre el conjunto de entrenamiento (train) y que los datos
de prueba (test) solo sean transformados (transform).
"""

import numpy as np
import pytest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


def test_pipeline_train_fit_only():
    """
    Verifica que el escalador calcule su media y varianza únicamente con los datos de train.
    """
    np.random.seed(42)
    # Generar datos sintéticos
    X_train = np.random.normal(loc=10.0, scale=2.0, size=(100, 2))
    X_test = np.random.normal(loc=50.0, scale=5.0, size=(20, 2))
    y_train = np.random.randint(0, 2, size=100)

    scaler = StandardScaler()
    pipeline = Pipeline([
        ('scaler', scaler),
        ('model', LogisticRegression(random_state=42))
    ])

    # Entrenar solo en train
    pipeline.fit(X_train, y_train)

    # La media aprendida debe coincidir con la media de train (cercana a 10.0), NO de test
    learned_mean = pipeline.named_steps['scaler'].mean_
    train_mean = np.mean(X_train, axis=0)
    total_mean = np.mean(np.vstack([X_train, X_test]), axis=0)

    # El escalador debe reflejar estrictamente train_mean
    assert np.allclose(learned_mean, train_mean), "El escalador no coincide con la media de train"
    assert not np.allclose(learned_mean, total_mean), "Alerta de Data Leakage: El escalador aprendió de test"

    # Inferencia en test debe ejecutarse sin reajustar (fit)
    preds = pipeline.predict(X_test)
    assert len(preds) == len(X_test)
