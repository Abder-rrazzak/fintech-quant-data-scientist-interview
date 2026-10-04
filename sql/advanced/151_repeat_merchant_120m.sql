-- Same merchant again within 120 minutes
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find a transaction that repeats the same customer and merchant within the previous 120 minutes.
--
-- Approach: A self-join expresses a repeat event. Deduplicate if one transaction matches several priors and you only need a flag.
-- Common mistake: This join multiplies rows. If the deliverable is a flag, aggregate back to one row per transaction.

SELECT a.transaction_id, a.customer_id, a.merchant_id, a.timestamp
FROM transactions AS a
JOIN transactions AS b
  ON a.customer_id = b.customer_id
 AND a.merchant_id = b.merchant_id
 AND a.transaction_id <> b.transaction_id
 AND b.timestamp < a.timestamp
 AND b.timestamp >= a.timestamp - INTERVAL '120 minutes';
