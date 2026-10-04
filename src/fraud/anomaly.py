"""Anomaly scores for the laboratory.

An outlier is a point that is unusual under a reference distribution or a
distance rule. Fraud is a business label. The two sets overlap and neither
contains the other. A large legitimate purchase is often an outlier. A
low-and-slow fraud pattern may never look like an outlier.
"""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM


def zscore_flags(values: np.ndarray, threshold: float = 3.0) -> tuple[np.ndarray, np.ndarray]:
    values = np.asarray(values, dtype=float)
    std = float(values.std(ddof=0))
    if std == 0 or len(values) == 0:
        return np.zeros(len(values), dtype=bool), np.zeros(len(values), dtype=float)
    z = (values - float(values.mean())) / std
    return np.abs(z) >= threshold, z


def iqr_flags(values: np.ndarray, k: float = 1.5) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    q1, q3 = np.percentile(values, [25, 75])
    iqr = q3 - q1
    low = q1 - k * iqr
    high = q3 + k * iqr
    return (values < low) | (values > high)


def isolation_forest_flags(features: np.ndarray, contamination: float = 0.01, seed: int = 42) -> np.ndarray:
    model = IsolationForest(contamination=contamination, random_state=seed, n_estimators=100)
    labels = model.fit_predict(np.asarray(features, dtype=float))
    return labels == -1


def one_class_svm_flags(features: np.ndarray, nu: float = 0.05) -> np.ndarray:
    """One-class SVM. Keep this on small samples; it scales poorly."""
    model = OneClassSVM(kernel="rbf", gamma="scale", nu=nu)
    labels = model.fit_predict(np.asarray(features, dtype=float))
    return labels == -1


def local_outlier_factor_flags(features: np.ndarray, n_neighbors: int = 20) -> np.ndarray:
    features = np.asarray(features, dtype=float)
    neighbors = min(n_neighbors, max(len(features) - 1, 1))
    model = LocalOutlierFactor(n_neighbors=neighbors, novelty=False)
    labels = model.fit_predict(features)
    return labels == -1


def pca_reconstruction_error(features: np.ndarray, n_components: int = 2) -> np.ndarray:
    """Squared error of a linear autoencoder, which is PCA reconstruction.

    A nonlinear autoencoder is the PyTorch example under machine-learning/pytorch.
    The decision rule is the same idea: high reconstruction error is unusual, not
    automatically fraudulent.
    """
    x = np.asarray(features, dtype=float)
    if x.ndim != 2:
        raise ValueError("Features must be a 2-D array.")
    mean = x.mean(axis=0)
    centered = x - mean
    components = min(n_components, x.shape[0], x.shape[1])
    if components < 1:
        return np.zeros(len(x), dtype=float)
    _, _, vt = np.linalg.svd(centered, full_matrices=False)
    basis = vt[:components].T
    reconstructed = centered @ basis @ basis.T
    return np.sum((centered - reconstructed) ** 2, axis=1)
