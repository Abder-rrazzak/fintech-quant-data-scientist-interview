"""Reproducible synthetic retail-finance laboratory.

Tables are simulated. They are not an extract from a bank, a card network,
or a production fraud system. Seeds make a run repeatable.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from data.quality import TRANSACTION_COLUMNS

logger = logging.getLogger(__name__)

COUNTRIES = np.array(["US", "GB", "DE", "FR", "CA", "BR", "IN", "SG", "AE", "MX"])
COUNTRY_P = np.array([0.40, 0.10, 0.08, 0.07, 0.08, 0.07, 0.08, 0.04, 0.04, 0.04])
SEGMENTS = np.array(["retail", "affluent", "mass_market", "small_business"])
SEGMENT_P = np.array([0.35, 0.15, 0.40, 0.10])
CATEGORIES = np.array(
    [
        "grocery",
        "restaurant",
        "fuel",
        "travel",
        "electronics",
        "gambling",
        "crypto",
        "wire",
        "atm",
        "subscription",
        "luxury",
        "utilities",
    ]
)
CATEGORY_TICKET = {
    "grocery": 45.0,
    "restaurant": 38.0,
    "fuel": 55.0,
    "travel": 280.0,
    "electronics": 160.0,
    "gambling": 90.0,
    "crypto": 220.0,
    "wire": 700.0,
    "atm": 120.0,
    "subscription": 18.0,
    "luxury": 450.0,
    "utilities": 95.0,
}
HIGH_RISK = {"gambling", "crypto", "wire", "luxury"}
PAYMENT_METHODS = np.array(["card_present", "card_not_present", "ach", "wire", "wallet"])
TXN_TYPES = np.array(["purchase", "refund", "cash_withdrawal", "transfer", "fee"])
TXN_TYPE_P = np.array([0.78, 0.06, 0.06, 0.07, 0.03])
CURRENCIES = np.array(["USD", "EUR", "GBP"])
EMPLOYMENT = np.array(["employed", "self_employed", "unemployed", "retired"])
EMPLOYMENT_P = np.array([0.70, 0.15, 0.05, 0.10])
INCOME_BASE = {
    "retail": 55_000.0,
    "affluent": 180_000.0,
    "mass_market": 35_000.0,
    "small_business": 90_000.0,
}

_HOUR = np.array(
    [
        0.010, 0.008, 0.007, 0.006, 0.008, 0.012,
        0.020, 0.030, 0.040, 0.045, 0.050, 0.055,
        0.060, 0.065, 0.070, 0.070, 0.065, 0.060,
        0.055, 0.050, 0.045, 0.040, 0.030, 0.020,
    ]
)
HOUR_PROBS = _HOUR / _HOUR.sum()


@dataclass(frozen=True)
class GenerateConfig:
    n_customers: int
    n_transactions: int
    seed: int = 42
    start: str = "2020-01-01"
    end: str = "2025-12-31"
    drift_date: str = "2025-06-01"
    loan_seasoning_end: str = "2024-12-31"


def generate_dataset(config: GenerateConfig) -> dict[str, pd.DataFrame]:
    """Build a consistent set of synthetic financial tables."""
    if config.n_customers < 50:
        raise ValueError("n_customers must be at least 50.")
    if config.n_transactions < config.n_customers:
        raise ValueError("n_transactions must be at least n_customers.")
    rng = np.random.default_rng(config.seed)
    start = np.datetime64(config.start, "D")
    end = np.datetime64(config.end, "D")
    customers = _customers(rng, config.n_customers, start, end)
    accounts = _accounts(rng, customers)
    cards = _cards(rng, accounts)
    merchants = _merchants(rng, max(80, config.n_customers // 25))
    transactions = _transactions(rng, config, customers, accounts, merchants)
    loans = _loans(rng, customers, accounts, config)
    payments = _payments(rng, loans)
    fraud_events = _fraud_events(rng, transactions)
    credit_events = _credit_events(loans)
    risk_events = _risk_events(rng, customers, loans, config)
    market = _market_data(rng, config.start, config.end)
    return {
        "customers": customers,
        "accounts": accounts,
        "cards": cards,
        "merchants": merchants,
        "transactions": transactions,
        "loans": loans,
        "payments": payments,
        "fraud_events": fraud_events,
        "credit_events": credit_events,
        "risk_events": risk_events,
        "market_data": market,
    }


def write_dataset(tables: dict[str, pd.DataFrame], output_dir: Path, config: GenerateConfig) -> Path:
    """Write Parquet tables and a manifest. Returns the manifest path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_parquet(output_dir / f"{name}.parquet", index=False)
    transactions = tables["transactions"]
    manifest = {
        "disclaimer": "Synthetic laboratory data. Not a production financial extract.",
        "seed": config.seed,
        "n_customers": config.n_customers,
        "n_transactions_requested": config.n_transactions,
        "rows": {name: int(len(frame)) for name, frame in tables.items()},
        "fraud_rate": float(transactions["is_fraud"].mean()),
        "default_rate": float(tables["loans"]["default_12m"].mean()),
        "start": config.start,
        "end": config.end,
        "drift_date": config.drift_date,
    }
    path = output_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info(
        "Wrote %s tables to %s (fraud rate %.4f, default rate %.4f)",
        len(tables),
        output_dir,
        manifest["fraud_rate"],
        manifest["default_rate"],
    )
    return path


def load_raw(directory: Path) -> dict[str, pd.DataFrame]:
    """Load Parquet tables written by :func:`write_dataset`."""
    tables: dict[str, pd.DataFrame] = {}
    for path in sorted(directory.glob("*.parquet")):
        tables[path.stem] = pd.read_parquet(path)
    if "transactions" not in tables:
        raise FileNotFoundError(f"No transactions.parquet in {directory}")
    for name, frame in tables.items():
        for column in frame.columns:
            if column.endswith("_date") or column in {"timestamp", "detected_at"}:
                tables[name][column] = pd.to_datetime(frame[column])
    return tables


def _customers(rng: np.random.Generator, n: int, start: np.datetime64, end: np.datetime64) -> pd.DataFrame:
    span = int((end - start) / np.timedelta64(1, "D"))
    signup = start + rng.integers(0, max(span // 2, 1), size=n).astype("timedelta64[D]")
    segment = rng.choice(SEGMENTS, size=n, p=SEGMENT_P)
    income = np.array([INCOME_BASE[value] for value in segment], dtype=float)
    income *= rng.lognormal(mean=0.0, sigma=0.35, size=n)
    score = np.clip(520 + income / 900.0 + rng.normal(0, 35, size=n), 300, 850)
    return pd.DataFrame(
        {
            "customer_id": np.arange(1, n + 1, dtype=int),
            "customer_age": rng.integers(18, 85, size=n),
            "customer_segment": segment,
            "income": np.round(income, 2),
            "country": rng.choice(COUNTRIES, size=n, p=COUNTRY_P),
            "signup_date": pd.to_datetime(signup),
            "credit_score": np.round(score, 1),
            "employment_status": rng.choice(EMPLOYMENT, size=n, p=EMPLOYMENT_P),
        }
    )


def _accounts(rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    n = len(customers)
    extra = max(1, n // 5)
    extra_ids = rng.choice(customers["customer_id"].to_numpy(), size=extra, replace=False)
    customer_ids = np.concatenate([customers["customer_id"].to_numpy(), extra_ids])
    signup = customers.set_index("customer_id").loc[customer_ids, "signup_date"].to_numpy()
    opened = signup + rng.integers(0, 120, size=len(customer_ids)).astype("timedelta64[D]")
    income = customers.set_index("customer_id").loc[customer_ids, "income"].to_numpy(dtype=float)
    limit = np.clip(income * rng.uniform(0.08, 0.45, size=len(customer_ids)), 500, 50_000)
    return pd.DataFrame(
        {
            "account_id": np.arange(1, len(customer_ids) + 1, dtype=int),
            "customer_id": customer_ids.astype(int),
            "account_type": rng.choice(["checking", "credit", "savings"], size=len(customer_ids), p=[0.45, 0.35, 0.20]),
            "opened_date": pd.to_datetime(opened),
            "status": rng.choice(["open", "closed", "restricted"], size=len(customer_ids), p=[0.90, 0.07, 0.03]),
            "credit_limit": np.round(limit, 2),
        }
    )


def _cards(rng: np.random.Generator, accounts: pd.DataFrame) -> pd.DataFrame:
    issued = accounts["opened_date"].to_numpy() + rng.integers(0, 30, size=len(accounts)).astype("timedelta64[D]")
    return pd.DataFrame(
        {
            "card_id": np.arange(1, len(accounts) + 1, dtype=int),
            "account_id": accounts["account_id"].to_numpy(),
            "customer_id": accounts["customer_id"].to_numpy(),
            "card_type": rng.choice(["debit", "credit", "prepaid"], size=len(accounts), p=[0.5, 0.4, 0.1]),
            "issued_date": pd.to_datetime(issued),
            "status": rng.choice(["active", "blocked", "expired"], size=len(accounts), p=[0.92, 0.05, 0.03]),
        }
    )


def _merchants(rng: np.random.Generator, n: int) -> pd.DataFrame:
    category = rng.choice(CATEGORIES, size=n)
    risk = np.where(np.isin(category, list(HIGH_RISK)), "high", "low")
    risk = np.where(np.isin(category, ["travel", "electronics"]), "medium", risk)
    return pd.DataFrame(
        {
            "merchant_id": np.arange(1, n + 1, dtype=int),
            "merchant_name": [f"synthetic_merchant_{i}" for i in range(1, n + 1)],
            "merchant_category": category,
            "country": rng.choice(COUNTRIES, size=n, p=COUNTRY_P),
            "risk_tier": risk,
        }
    )


def _transactions(
    rng: np.random.Generator,
    config: GenerateConfig,
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    merchants: pd.DataFrame,
) -> pd.DataFrame:
    n = config.n_transactions
    cust_ids = customers["customer_id"].to_numpy()
    weights = rng.random(len(cust_ids))
    weights = weights / weights.sum()
    customer_id = rng.choice(cust_ids, size=n, p=weights)

    primary = (
        accounts.sort_values("account_id")
        .drop_duplicates("customer_id")
        .set_index("customer_id")
    )
    account_id = primary.loc[customer_id, "account_id"].to_numpy(dtype=int)
    opened = pd.to_datetime(primary.loc[customer_id, "opened_date"]).to_numpy(dtype="datetime64[ns]")

    day_index = pd.date_range(config.start, config.end, freq="D", inclusive="left")
    month_weight = np.where(day_index.month.isin([11, 12]), 1.55, 1.0).astype(float)
    month_weight = month_weight / month_weight.sum()
    chosen_days = rng.choice(day_index.to_numpy(dtype="datetime64[ns]"), size=n, p=month_weight)
    hours = rng.choice(np.arange(24), size=n, p=HOUR_PROBS).astype("timedelta64[h]")
    minutes = rng.integers(0, 60, size=n).astype("timedelta64[m]")
    seconds = rng.integers(0, 60, size=n).astype("timedelta64[s]")
    timestamp = chosen_days + hours + minutes + seconds
    too_early = timestamp < opened
    timestamp = timestamp.copy()
    timestamp[too_early] = opened[too_early] + rng.integers(0, 20, size=n).astype("timedelta64[D]")[too_early]

    merchant_id = rng.integers(1, len(merchants) + 1, size=n)
    merchant_cat = merchants.set_index("merchant_id").loc[merchant_id, "merchant_category"].to_numpy()
    tickets = np.array([CATEGORY_TICKET[cat] for cat in merchant_cat], dtype=float)
    amount = np.round(tickets * rng.lognormal(0.0, 0.45, size=n), 2)
    months = pd.to_datetime(timestamp).month.to_numpy()
    amount = np.where(np.isin(months, [11, 12]), np.round(amount * 1.2, 2), amount)

    home = customers.set_index("customer_id").loc[customer_id, "country"].to_numpy()
    geo_draw = rng.random(n) < 0.07
    country = home.copy()
    n_geo = int(geo_draw.sum())
    if n_geo:
        country[geo_draw] = rng.choice(COUNTRIES, size=n_geo)

    new_device = rng.random(n) < 0.04
    device_num = np.where(new_device, rng.integers(1_000_000, 9_000_000, size=n), 500_000 + customer_id)
    device_id = np.char.add("dev_", device_num.astype(str))
    ip_a = rng.integers(11, 223, size=n)
    ip_b = rng.integers(0, 255, size=n)
    ip_c = rng.integers(0, 255, size=n)
    ip_d = rng.integers(1, 254, size=n)
    ip_address = [f"{a}.{b}.{c}.{d}" for a, b, c, d in zip(ip_a, ip_b, ip_c, ip_d, strict=True)]

    txn_type = rng.choice(TXN_TYPES, size=n, p=TXN_TYPE_P)
    currency = np.where(country == "GB", "GBP", np.where(np.isin(country, ["DE", "FR"]), "EUR", "USD"))
    segment = customers.set_index("customer_id").loc[customer_id, "customer_segment"].to_numpy()
    age = customers.set_index("customer_id").loc[customer_id, "customer_age"].to_numpy(dtype=int)
    account_age = ((timestamp - opened) / np.timedelta64(1, "D")).astype(int)
    account_age = np.clip(account_age, 0, None)

    order = np.lexsort((timestamp.view(np.int64), customer_id))
    customer_s = customer_id[order]
    timestamp_s = timestamp[order]
    amount_s = amount[order]
    geo_s = geo_draw[order]
    new_device_s = new_device[order]
    cat_s = merchant_cat[order]
    hour_s = pd.to_datetime(timestamp_s).hour.to_numpy()
    drift = timestamp_s >= np.datetime64(config.drift_date)

    ts_ns = timestamp_s.view(np.int64)
    vel = _prior_count(customer_s, ts_ns, np.int64(3_600_000_000_000))
    z = _prior_z(customer_s, amount_s)
    high_risk = np.isin(cat_s, list(HIGH_RISK))
    night = (hour_s >= 0) & (hour_s <= 5)
    # The intercept targets a rare fraud label. Laptop samples still contain
    # enough positives to train; a live card book is often closer to 0.1%.
    logit = (
        -6.3
        + 0.55 * np.clip(z, 0, 6)
        + 0.20 * np.clip(vel, 0, 6)
        + 1.15 * geo_s.astype(float)
        + 0.95 * new_device_s.astype(float)
        + 0.75 * high_risk.astype(float)
        + 0.25 * night.astype(float)
        + 0.40 * drift.astype(float)
    )
    probability = 1.0 / (1.0 + np.exp(-np.clip(logit, -30, 30)))
    is_fraud_s = rng.random(n) < probability
    inv = np.empty(n, dtype=int)
    inv[order] = np.arange(n)
    is_fraud = is_fraud_s[inv].astype(int)

    balance_before, balance_after = _running_balances(rng, account_id, timestamp, amount, txn_type, len(accounts))

    frame = pd.DataFrame(
        {
            "transaction_id": np.arange(1, n + 1, dtype=int),
            "customer_id": customer_id.astype(int),
            "account_id": account_id.astype(int),
            "merchant_id": merchant_id.astype(int),
            "timestamp": pd.to_datetime(timestamp),
            "amount": amount.astype(float),
            "currency": currency,
            "country": country,
            "merchant_category": merchant_cat,
            "payment_method": rng.choice(PAYMENT_METHODS, size=n),
            "device_id": device_id,
            "ip_address": ip_address,
            "account_age_days": account_age.astype(int),
            "customer_age": age.astype(int),
            "customer_segment": segment,
            "balance_before": np.round(balance_before, 2),
            "balance_after": np.round(balance_after, 2),
            "transaction_type": txn_type,
            "is_fraud": is_fraud,
        }
    )
    frame = _inject_quality_issues(rng, frame)
    return frame.loc[:, TRANSACTION_COLUMNS + ["is_duplicate"]].reset_index(drop=True)


def _prior_count(customer_ids: np.ndarray, timestamps_ns: np.ndarray, window_ns: int) -> np.ndarray:
    """Count of earlier rows in the window. Arrays are sorted by customer, then time."""
    n = len(customer_ids)
    counts = np.zeros(n, dtype=float)
    left = 0
    for i in range(n):
        if i > 0 and customer_ids[i] != customer_ids[i - 1]:
            left = i
        limit = timestamps_ns[i] - window_ns
        while timestamps_ns[left] < limit:
            left += 1
        counts[i] = i - left
    return counts


def _prior_z(customer_ids: np.ndarray, amounts: np.ndarray) -> np.ndarray:
    n = len(amounts)
    z = np.zeros(n, dtype=float)
    count = 0
    total = 0.0
    total_sq = 0.0
    for i in range(n):
        if i == 0 or customer_ids[i] != customer_ids[i - 1]:
            count = 0
            total = 0.0
            total_sq = 0.0
        if count > 1:
            mean = total / count
            var = max(total_sq / count - mean * mean, 0.0)
            std = np.sqrt(var)
            if std > 1e-8:
                z[i] = (amounts[i] - mean) / std
        count += 1
        total += float(amounts[i])
        total_sq += float(amounts[i] * amounts[i])
    return z


def _running_balances(
    rng: np.random.Generator,
    account_id: np.ndarray,
    timestamp: np.ndarray,
    amount: np.ndarray,
    txn_type: np.ndarray,
    n_accounts: int,
) -> tuple[np.ndarray, np.ndarray]:
    order = np.lexsort((timestamp.view(np.int64), account_id))
    running = rng.lognormal(mean=8.0, sigma=0.45, size=n_accounts)
    before = np.zeros(len(account_id), dtype=float)
    after = np.zeros(len(account_id), dtype=float)
    for i in order:
        slot = int(account_id[i]) - 1
        before[i] = running[slot]
        signed = float(amount[i])
        if txn_type[i] != "refund":
            signed = -signed
        running[slot] = max(running[slot] + signed, 0.0)
        after[i] = running[slot]
    return before, after


def _inject_quality_issues(rng: np.random.Generator, frame: pd.DataFrame) -> pd.DataFrame:
    """Plant the defects an interview data-quality discussion should catch."""
    out = frame.copy()
    n = len(out)
    out["is_duplicate"] = False
    n_missing_cat = max(1, int(n * 0.02))
    n_missing_device = max(1, int(n * 0.01))
    n_bad_age = max(1, int(n * 0.005))
    n_bad_amount = max(1, int(n * 0.003))
    cat_idx = rng.choice(n, size=n_missing_cat, replace=False)
    device_idx = rng.choice(n, size=n_missing_device, replace=False)
    age_idx = rng.choice(n, size=n_bad_age, replace=False)
    amount_idx = rng.choice(n, size=n_bad_amount, replace=False)
    out.loc[out.index[cat_idx], "merchant_category"] = None
    out.loc[out.index[device_idx], "device_id"] = None
    out.loc[out.index[age_idx], "customer_age"] = rng.choice([0, 140, 200], size=n_bad_age)
    out.loc[out.index[amount_idx], "amount"] = -np.abs(out.loc[out.index[amount_idx], "amount"].to_numpy())
    out.loc[out.index[amount_idx], "transaction_type"] = "purchase"
    dup_n = max(1, int(n * 0.005))
    dup_idx = rng.choice(n, size=dup_n, replace=False)
    duplicates = out.iloc[dup_idx].copy()
    duplicates["is_duplicate"] = True
    return pd.concat([out, duplicates], ignore_index=True)


def _loans(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    accounts: pd.DataFrame,
    config: GenerateConfig,
) -> pd.DataFrame:
    n_loans = max(30, int(len(customers) * 0.45))
    chosen = rng.choice(customers["customer_id"].to_numpy(), size=n_loans, replace=False)
    cust = customers.set_index("customer_id").loc[chosen]
    primary = accounts.sort_values("account_id").drop_duplicates("customer_id").set_index("customer_id")
    opened = pd.to_datetime(primary.loc[chosen, "opened_date"])
    signup = pd.to_datetime(cust["signup_date"])
    latest = pd.Timestamp(config.loan_seasoning_end)
    span_days = (latest - signup).dt.days.clip(lower=30).to_numpy()
    offset = (rng.random(n_loans) * span_days).astype(int)
    origination = signup + pd.to_timedelta(offset, unit="D")
    origination = pd.to_datetime(np.maximum(origination.to_numpy(), opened.to_numpy()))
    score = cust["credit_score"].to_numpy(dtype=float)
    income = cust["income"].to_numpy(dtype=float)
    employment = cust["employment_status"].to_numpy()
    utilization = np.clip(rng.beta(2, 5, size=n_loans) + (score < 640) * 0.2, 0.01, 1.4)
    dti = np.clip(rng.normal(0.28, 0.08, size=n_loans) + (income < 40_000) * 0.08, 0.02, 0.9)
    prior_dq = rng.poisson(0.15, size=n_loans) + (score < 600).astype(int)
    account_age = ((origination.to_numpy() - opened.to_numpy()) / np.timedelta64(1, "D")).astype(int)
    account_age = np.clip(account_age, 0, None)
    principal = np.round(np.clip(income * rng.uniform(0.05, 0.25, size=n_loans), 1_000, 40_000), 2)
    rate = np.round(np.clip(0.06 + (720 - score) / 800 + rng.normal(0, 0.01, size=n_loans), 0.05, 0.36), 4)
    unemployed = (employment == "unemployed").astype(float)
    logit = (
        -3.5
        + 1.05 * (score < 620).astype(float)
        + 0.85 * (utilization > 0.85).astype(float)
        + 0.65 * (dti > 0.55).astype(float)
        + 0.45 * (prior_dq >= 2).astype(float)
        + 0.55 * unemployed
        - 0.01 * (score - 640)
    )
    default_p = 1.0 / (1.0 + np.exp(-np.clip(logit, -30, 30)))
    defaulted = (rng.random(n_loans) < default_p).astype(int)
    lgd = np.round(np.clip(rng.normal(0.45, 0.08, size=n_loans), 0.05, 0.95), 3)
    status = np.where(defaulted == 1, "defaulted", "paid_off")
    return pd.DataFrame(
        {
            "loan_id": np.arange(1, n_loans + 1, dtype=int),
            "customer_id": chosen.astype(int),
            "account_id": primary.loc[chosen, "account_id"].to_numpy(dtype=int),
            "principal": principal,
            "interest_rate": rate,
            "term_months": np.full(n_loans, 12, dtype=int),
            "origination_date": origination,
            "status": status,
            "income": np.round(income, 2),
            "credit_score": score,
            "utilization": np.round(utilization, 4),
            "dti": np.round(dti, 4),
            "account_age_days": account_age.astype(int),
            "prior_delinquency_count": prior_dq.astype(int),
            "employment_status": employment,
            "customer_segment": cust["customer_segment"].to_numpy(),
            "default_12m": defaulted,
            "lgd": lgd,
            "ead": principal,
        }
    )


def _payments(rng: np.random.Generator, loans: pd.DataFrame) -> pd.DataFrame:
    n_loans = len(loans)
    months = 12
    loan_id = np.repeat(loans["loan_id"].to_numpy(), months)
    customer_id = np.repeat(loans["customer_id"].to_numpy(), months)
    principal = np.repeat(loans["principal"].to_numpy(), months)
    rate = np.repeat(loans["interest_rate"].to_numpy(), months)
    defaulted = np.repeat(loans["default_12m"].to_numpy(), months)
    origin = np.repeat(loans["origination_date"].to_numpy(), months)
    month_index = np.tile(np.arange(1, months + 1), n_loans)
    monthly_rate = rate / 12.0
    payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1.0)
    due = pd.to_datetime(origin) + pd.to_timedelta(month_index * 30, unit="D")
    late = (defaulted == 1) & (month_index >= 7)
    dpd = np.where(late, rng.integers(31, 120, size=len(loan_id)), rng.integers(0, 5, size=len(loan_id)))
    amount_due = np.round(payment, 2)
    amount_paid = np.where(late, np.round(amount_due * 0.35, 2), amount_due)
    paid = due + pd.to_timedelta(dpd, unit="D")
    return pd.DataFrame(
        {
            "payment_id": np.arange(1, len(loan_id) + 1, dtype=int),
            "loan_id": loan_id.astype(int),
            "customer_id": customer_id.astype(int),
            "due_date": due,
            "paid_date": paid,
            "amount_due": amount_due,
            "amount_paid": amount_paid,
            "days_past_due": dpd.astype(int),
        }
    )


def _fraud_events(rng: np.random.Generator, transactions: pd.DataFrame) -> pd.DataFrame:
    frauds = transactions.loc[transactions["is_fraud"] == 1, ["transaction_id", "customer_id", "timestamp"]].copy()
    if frauds.empty:
        return pd.DataFrame(columns=["event_id", "transaction_id", "customer_id", "fraud_type", "detected_at"])
    lag_hours = rng.integers(1, 72, size=len(frauds))
    types = rng.choice(
        ["card_testing", "account_takeover", "friendly_fraud", "mule", "geo_impossible"],
        size=len(frauds),
    )
    frauds = frauds.reset_index(drop=True)
    frauds.insert(0, "event_id", np.arange(1, len(frauds) + 1))
    frauds["fraud_type"] = types
    frauds["detected_at"] = frauds["timestamp"] + pd.to_timedelta(lag_hours, unit="h")
    return frauds[["event_id", "transaction_id", "customer_id", "fraud_type", "detected_at"]]


def _credit_events(loans: pd.DataFrame) -> pd.DataFrame:
    rows = loans.loc[loans["default_12m"] == 1, ["loan_id", "customer_id", "origination_date"]].copy()
    if rows.empty:
        return pd.DataFrame(columns=["event_id", "customer_id", "loan_id", "event_type", "event_date", "severity"])
    rows = rows.reset_index(drop=True)
    rows.insert(0, "event_id", np.arange(1, len(rows) + 1))
    rows["event_type"] = "default"
    rows["event_date"] = rows["origination_date"] + pd.Timedelta(days=180)
    rows["severity"] = "charge_off"
    return rows[["event_id", "customer_id", "loan_id", "event_type", "event_date", "severity"]]


def _risk_events(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    loans: pd.DataFrame,
    config: GenerateConfig,
) -> pd.DataFrame:
    dates = pd.date_range("2020-03-31", config.end, freq="90D")
    ids = customers["customer_id"].to_numpy()
    # One snapshot per customer per date would be huge at 100k x 24. Keep a sample of customers
    # plus every borrower so the table stays useful and laptop-friendly.
    borrower_ids = loans["customer_id"].unique()
    sample_n = min(len(ids), max(200, len(ids) // 5))
    sampled = np.unique(np.concatenate([borrower_ids, rng.choice(ids, size=sample_n, replace=False)]))
    score_map = customers.set_index("customer_id")["credit_score"]
    default_map = loans.groupby("customer_id")["default_12m"].max()
    records_id = np.repeat(sampled, len(dates))
    records_date = np.tile(dates.to_numpy(), len(sampled))
    base = score_map.loc[records_id].to_numpy(dtype=float)
    defaulted = default_map.reindex(records_id).fillna(0).to_numpy(dtype=float)
    noise = rng.normal(0, 12, size=len(records_id))
    risk_score = np.clip(base - 30 * defaulted + noise, 300, 850)
    reason = np.where(defaulted == 1, "delinquency", np.where(risk_score < 600, "utilization", "routine"))
    return pd.DataFrame(
        {
            "event_id": np.arange(1, len(records_id) + 1, dtype=int),
            "customer_id": records_id.astype(int),
            "risk_score": np.round(risk_score, 1),
            "event_date": pd.to_datetime(records_date),
            "reason": reason,
        }
    )


def _market_data(rng: np.random.Generator, start: str, end: str) -> pd.DataFrame:
    """Geometric Brownian paths. A teaching price history, not a market-data vendor feed."""
    days = pd.bdate_range(start, end, inclusive="left")
    specs = {
        "SPX": (4_000.0, 0.07, 0.16),
        "EURUSD": (1.10, 0.00, 0.08),
        "GOLD": (1_800.0, 0.04, 0.15),
    }
    frames = []
    dt = 1.0 / 252.0
    for symbol, (s0, mu, sigma) in specs.items():
        shocks = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), size=len(days))
        price = s0 * np.exp(np.cumsum(shocks))
        ret = np.empty(len(price), dtype=float)
        ret[0] = np.nan
        ret[1:] = np.diff(price) / price[:-1]
        frames.append(pd.DataFrame({"date": days, "symbol": symbol, "close": price, "simple_return": ret}))
    return pd.concat(frames, ignore_index=True)
