"""Core laboratory tests. They use small synthetic samples and do not need data/raw."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from data.generate import GenerateConfig, generate_dataset
from data.quality import clean_transactions, quality_report, validate_transactions
from evaluation.fairness import demographic_parity_difference, equal_opportunity_difference
from evaluation.inference import bootstrap_mean_interval, normal_confidence_interval, two_proportion_ztest
from evaluation.metrics import ks_statistic, precision_at_recall, recall_at_precision
from evaluation.thresholds import select_threshold, threshold_cost_curve
from evaluation.validation import (
    LeakageError,
    assert_point_in_time,
    find_leaky_columns,
    quantile_time_split,
)
from features.credit_features import attach_credit_transaction_features
from features.store import OnlineFeatureCache, ParquetFeatureStore, training_serving_skew
from features.transactions import engineer_fraud_features
from features.windows import prior_mean_and_std, window_count_and_sum
from forecasting.backtest import (
    apply_transaction_cost,
    assert_causal_splits,
    expanding_window_indices,
    rolling_window_indices,
)
from forecasting.series import fit_ar1, log_returns
from fraud.anomaly import iqr_flags, pca_reconstruction_error, zscore_flags
from fraud.decisions import decide
from models.clv import horizon_revenue_frame, rfm_table, simple_clv
from monitoring.drift import population_stability_index
from risk.expected_loss import expected_loss


def test_window_counts_are_point_in_time():
    hour = 3_600_000_000_000
    entities = np.array([1, 1, 1])
    stamps = np.array([0, int(0.5 * hour), 2 * hour], dtype=np.int64)
    amounts = np.array([10.0, 5.0, 7.0])
    counts, sums = window_count_and_sum(entities, stamps, amounts, hour)
    assert list(counts) == [1, 2, 1]
    assert sums.tolist() == pytest.approx([10.0, 15.0, 7.0])


def test_prior_mean_excludes_current_row():
    entities = np.array([1, 1, 1])
    amounts = np.array([10.0, 30.0, 50.0])
    means, _stds = prior_mean_and_std(entities, amounts)
    assert np.isnan(means[0])
    assert means[1] == pytest.approx(10.0)
    assert means[2] == pytest.approx(20.0)


def test_expected_loss_identity():
    assert expected_loss(0.02, 0.45, 10_000) == pytest.approx(90.0)


def test_ks_on_separated_scores():
    ks = ks_statistic(np.array([0, 0, 1, 1]), np.array([0.1, 0.2, 0.8, 0.9]))
    assert ks == pytest.approx(1.0)


def test_recall_at_precision():
    recall = recall_at_precision(np.array([1, 1, 0, 0]), np.array([0.9, 0.8, 0.7, 0.1]), 0.9)
    assert recall == pytest.approx(1.0)
    assert precision_at_recall(np.array([1, 0, 0, 0]), np.array([0.9, 0.2, 0.1, 0.05]), 1.0) == pytest.approx(1.0)


def test_high_false_negative_cost_lowers_threshold():
    # The legitimate event scores above the fraud, so a low threshold is the only
    # way to catch the fraud, and it also flags the legitimate event.
    y = np.array([1, 0])
    scores = np.array([0.40, 0.70])
    expensive_miss = select_threshold(threshold_cost_curve(y, scores, fn_cost=10_000, fp_cost=1))
    cheap_miss = select_threshold(threshold_cost_curve(y, scores, fn_cost=1, fp_cost=10_000))
    assert expensive_miss["threshold"] <= 0.40
    assert cheap_miss["threshold"] > 0.70


def test_decisions_and_leakage_names():
    assert list(decide(np.array([0.1, 0.5, 0.9]), 0.4, 0.8)) == ["approve", "review", "block"]
    assert "is_fraud" in find_leaky_columns(["amount", "is_fraud"])
    assert find_leaky_columns(["prior_delinquency_count", "amount_zscore"]) == []
    with pytest.raises(LeakageError):
        assert_point_in_time(
            np.array(["2024-02-01"], dtype="datetime64[ns]"),
            np.array(["2024-01-01"], dtype="datetime64[ns]"),
        )


def test_time_split_is_ordered():
    frame = pd.DataFrame({"timestamp": pd.date_range("2024-01-01", periods=10, freq="D"), "y": 1})
    train, valid, test = quantile_time_split(frame, "timestamp")
    assert train["timestamp"].max() <= valid["timestamp"].min()
    assert valid["timestamp"].max() <= test["timestamp"].min()


def test_statistics_and_fairness():
    result = two_proportion_ztest(3500, 1_000_000, 1500, 1_000_000)
    assert result["p_value"] < 0.01
    low, high = normal_confidence_interval(np.array([1.0, 2.0, 3.0, 4.0, 5.0]))
    assert low < 3 < high
    boot_low, boot_high = bootstrap_mean_interval(np.array([1.0, 2.0, 3.0, 4.0]), n_resamples=200)
    assert boot_low <= boot_high
    groups = np.array(["a", "a", "b", "b"])
    assert demographic_parity_difference(np.array([1, 1, 0, 0]), groups) == pytest.approx(1.0)
    assert equal_opportunity_difference(np.array([1, 1, 1, 1]), np.array([1, 0, 1, 0]), groups) == pytest.approx(0.0)


def test_backtest_is_causal_and_costs_reduce_return():
    splits = expanding_window_indices(20, min_train=8, test_size=4)
    rolling = rolling_window_indices(20, train_size=8, test_size=4)
    assert_causal_splits(splits)
    assert_causal_splits(rolling)
    assert apply_transaction_cost(0.02, turnover=1.0, cost_bps=10) == pytest.approx(0.019)
    returns = log_returns(np.array([100.0, 110.0, 121.0]))
    assert returns[0] == pytest.approx(np.log(1.1))
    intercept, phi = fit_ar1(np.array([0.1, 0.2, 0.15, 0.25, 0.2, 0.3]))
    assert np.isfinite(intercept) and np.isfinite(phi)


def test_anomaly_and_psi_and_clv():
    values = np.concatenate([np.ones(30), [100.0]])
    flags, z_values = zscore_flags(values, threshold=3.0)
    assert flags[-1]
    assert abs(z_values[-1]) == max(np.abs(z_values))
    assert iqr_flags(values)[-1]
    error = pca_reconstruction_error(np.column_stack([values, values * 0.5]), n_components=1)
    assert error[-1] == max(error)
    same = population_stability_index(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float), np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float))
    shifted = population_stability_index(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float), np.array([20, 21, 22, 23, 24, 25, 26, 27, 28, 29], dtype=float))
    assert same < shifted
    assert simple_clv(50, 4, 0.2, 3) == pytest.approx(120.0)


def test_feature_store_does_not_read_the_future(tmp_path: Path):
    store = ParquetFeatureStore(tmp_path)
    history = pd.DataFrame(
        {
            "customer_id": [1, 1],
            "event_time": pd.to_datetime(["2024-01-01", "2024-06-01"]),
            "utilization": [0.2, 0.9],
        }
    )
    store.write("utilization", history, ["customer_id"], "event_time")
    entities = pd.DataFrame(
        {"customer_id": [1, 1], "as_of": pd.to_datetime(["2024-03-01", "2024-07-01"])}
    )
    joined = store.get_as_of("utilization", entities, "as_of")
    assert joined["utilization"].tolist() == pytest.approx([0.2, 0.9])
    cache = OnlineFeatureCache()
    cache.upsert("1", {"utilization": 0.9}, pd.Timestamp("2024-06-01"))
    assert training_serving_skew(0.2, cache.get_latest("1")["utilization"])


def test_generator_is_reproducible_and_dirty_then_clean():
    config = GenerateConfig(n_customers=80, n_transactions=1500, seed=7)
    first = generate_dataset(config)
    second = generate_dataset(config)
    assert first["transactions"]["amount"].tolist() == second["transactions"]["amount"].tolist()
    raw = first["transactions"]
    report = quality_report(raw)
    assert report["duplicate_transaction_ids"] > 0
    assert report["negative_purchase_amounts"] > 0
    assert validate_transactions(raw)
    clean = clean_transactions(raw)
    assert validate_transactions(clean) == []
    assert clean["transaction_id"].is_unique
    assert set(first) >= {
        "customers",
        "accounts",
        "cards",
        "merchants",
        "transactions",
        "loans",
        "payments",
        "fraud_events",
        "credit_events",
        "risk_events",
        "market_data",
    }
    frauds = first["fraud_events"]
    if not frauds.empty:
        merged = frauds.merge(raw[["transaction_id", "timestamp"]], on="transaction_id", how="left")
        assert (merged["detected_at"] >= merged["timestamp"]).all()


def test_credit_features_ignore_future_spend():
    loans = pd.DataFrame(
        {
            "loan_id": [1],
            "customer_id": [1],
            "origination_date": [pd.Timestamp("2024-06-01")],
        }
    )
    transactions = pd.DataFrame(
        {
            "customer_id": [1, 1],
            "timestamp": pd.to_datetime(["2024-05-01", "2024-07-01"]),
            "amount": [10.0, 10_000.0],
            "transaction_id": [1, 2],
        }
    )
    featured = attach_credit_transaction_features(loans, transactions, window_days=90)
    assert featured.loc[0, "txn_count_90d"] == 1
    assert featured.loc[0, "avg_amount_90d"] == pytest.approx(10.0)


def test_fraud_features_do_not_require_the_label():
    customers = pd.DataFrame({"customer_id": [1], "country": ["US"]})
    transactions = pd.DataFrame(
        {
            "customer_id": [1, 1],
            "timestamp": pd.to_datetime(["2024-01-01 10:00:00", "2024-01-01 10:20:00"]),
            "amount": [20.0, 80.0],
            "country": ["US", "BR"],
            "device_id": ["dev_a", "dev_b"],
            "merchant_category": ["grocery", "crypto"],
            "is_fraud": [0, 1],
        }
    )
    featured = engineer_fraud_features(transactions, customers)
    assert "is_fraud" in featured.columns
    assert featured.loc[1, "geo_mismatch"] == 1
    assert featured.loc[1, "new_device"] == 1
    assert featured.loc[1, "txn_count_1h"] == 2


def test_clv_label_is_after_cutoff():
    transactions = pd.DataFrame(
        {
            "customer_id": [1, 1],
            "transaction_id": [1, 2],
            "timestamp": pd.to_datetime(["2024-01-01", "2024-08-01"]),
            "amount": [30.0, 70.0],
        }
    )
    frame = horizon_revenue_frame(transactions, pd.Timestamp("2024-06-01"), horizon_days=90)
    assert frame.loc[0, "future_revenue"] == pytest.approx(70.0)
    assert frame.loc[0, "monetary"] == pytest.approx(30.0)
    assert rfm_table(transactions).loc[0, "frequency"] == 2


def test_api_health_and_missing_model(tmp_path: Path):
    from serving.api import create_app

    client = TestClient(create_app(tmp_path))
    assert client.get("/health").json()["status"] == "ok"
    response = client.post(
        "/score/fraud",
        json={
            "amount": 10,
            "log_amount": 2,
            "hour": 1,
            "night": 1,
            "geo_mismatch": 1,
            "new_device": 1,
            "high_risk_mcc": 1,
            "txn_count_1h": 4,
            "txn_count_24h": 6,
            "amount_sum_24h": 100,
            "amount_zscore": 3,
            "account_age_days": 10,
            "customer_age": 30,
        },
    )
    assert response.status_code == 503
