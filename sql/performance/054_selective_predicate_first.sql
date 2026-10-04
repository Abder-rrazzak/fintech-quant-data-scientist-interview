-- Filter before the join
-- Level: performance
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Compute the November fraud rate by merchant category without joining merchants before the date filter.
--
-- Approach: Filter the large fact table first, then join the small dimension.
-- Common mistake: Joining the full fact table to a dimension and filtering afterward can shuffle far more data than necessary.

WITH november AS (
    SELECT merchant_id, is_fraud
    FROM transactions
    WHERE timestamp >= TIMESTAMP '2024-11-01'
      AND timestamp < TIMESTAMP '2024-12-01'
)
SELECT m.merchant_category,
       AVG(n.is_fraud::numeric) AS fraud_rate,
       COUNT(*) AS transactions
FROM november AS n
JOIN merchants AS m
  ON n.merchant_id = m.merchant_id
GROUP BY m.merchant_category;
