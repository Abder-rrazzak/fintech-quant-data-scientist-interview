-- Local stand-in for an offline feature table.
-- This is PostgreSQL. It is not a Snowflake account and it does not grant one.
-- Point-in-time reads use the latest row at or before the decision time.

CREATE TABLE IF NOT EXISTS customer_features_offline (
    customer_id TEXT NOT NULL,
    event_time TIMESTAMPTZ NOT NULL,
    utilization DOUBLE PRECISION,
    txn_count_24h DOUBLE PRECISION,
    amount_zscore DOUBLE PRECISION,
    feature_version TEXT NOT NULL,
    PRIMARY KEY (customer_id, event_time, feature_version)
);

CREATE INDEX IF NOT EXISTS customer_features_asof
    ON customer_features_offline (customer_id, event_time DESC);

-- Example as-of lookup. Replace the literals with the decision you are scoring.
-- SELECT f.*
-- FROM customer_features_offline AS f
-- WHERE f.customer_id = 'C0001'
--   AND f.event_time <= TIMESTAMPTZ '2024-06-01 12:00:00+00'
-- ORDER BY f.event_time DESC
-- LIMIT 1;
