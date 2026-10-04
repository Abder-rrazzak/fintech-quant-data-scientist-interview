"""Executable SQL patterns against an in-memory SQLite database.

The teaching files use PostgreSQL syntax. These tests cover the same decisions
in SQLite so the laboratory does not need a running warehouse.
"""

from __future__ import annotations

import sqlite3

import pandas as pd


def _connection() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    pd.DataFrame(
        [
            ("t1", "c1", "m1", "2024-01-05", 10.0, 0),
            ("t2", "c1", "m1", "2024-01-06", 10.0, 0),
            ("t3", "c2", "m1", "2024-01-08", 100.0, 0),
            ("t4", "c3", "m2", "2024-01-09", 5.0, 0),
            ("t5", "c1", "m1", "2024-02-02", 40.0, 1),
            ("t6", "c1", "m2", "2024-02-03", 40.0, 1),
            ("t8", "c1", "m1", "2024-02-05", 12.0, 0),
            ("t9", "c1", "m2", "2024-02-06", 12.0, 0),
            ("t7", "c2", "m1", "2024-02-04", 10.0, 0),
        ],
        columns=["transaction_id", "customer_id", "merchant_id", "timestamp", "amount", "is_fraud"],
    ).to_sql("transactions", conn, index=False)
    return conn


def test_top_3_customers_by_month() -> None:
    conn = _connection()
    rows = pd.read_sql_query(
        """
        WITH monthly AS (
            SELECT substr(timestamp, 1, 7) AS month_start,
                   customer_id AS entity_id,
                   SUM(amount) AS total_amount
            FROM transactions
            GROUP BY 1, 2
        ), ranked AS (
            SELECT month_start, entity_id, total_amount,
                   ROW_NUMBER() OVER (
                       PARTITION BY month_start
                       ORDER BY total_amount DESC, entity_id
                   ) AS rn
            FROM monthly
        )
        SELECT month_start, entity_id, rn
        FROM ranked
        WHERE rn <= 3
        ORDER BY month_start, rn
        """,
        conn,
    )
    january = rows[rows["month_start"] == "2024-01"]["entity_id"].tolist()
    assert january[0] == "c2"
    assert set(january) == {"c2", "c1", "c3"}


def test_month_over_month_volume_increase() -> None:
    conn = _connection()
    rows = pd.read_sql_query(
        """
        WITH monthly AS (
            SELECT customer_id AS entity_id,
                   substr(timestamp, 1, 7) AS month_start,
                   COUNT(*) AS metric_value
            FROM transactions
            GROUP BY 1, 2
        )
        SELECT cur.entity_id,
               (cur.metric_value - prev.metric_value) * 1.0 / prev.metric_value AS pct_change
        FROM monthly AS cur
        JOIN monthly AS prev
          ON cur.entity_id = prev.entity_id
         AND cur.month_start = substr(date(prev.month_start || '-01', '+1 month'), 1, 7)
        WHERE prev.metric_value > 0
          AND cur.metric_value > prev.metric_value * 1.5
        """,
        conn,
    )
    # c1 moves from 2 January transactions to 4 in February.
    assert rows["entity_id"].tolist() == ["c1"]
    assert float(rows["pct_change"].iloc[0]) == 1.0


def test_consecutive_fraud_run() -> None:
    conn = _connection()
    rows = pd.read_sql_query(
        """
        WITH ordered AS (
            SELECT customer_id, timestamp, is_fraud,
                   ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY timestamp) AS rn
            FROM transactions
        ), marked AS (
            SELECT customer_id, is_fraud, rn,
                   rn - ROW_NUMBER() OVER (
                       PARTITION BY customer_id, is_fraud ORDER BY timestamp
                   ) AS grp
            FROM ordered
        )
        SELECT customer_id, COUNT(*) AS run_length
        FROM marked
        WHERE is_fraud = 1
        GROUP BY customer_id, grp
        HAVING COUNT(*) >= 2
        """,
        conn,
    )
    assert rows["customer_id"].tolist() == ["c1"]
    assert int(rows["run_length"].iloc[0]) == 2
