-- First transaction after risk score crosses 640
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- For each customer, find the first transaction at or after the first risk_events row whose risk_score is below 640. Customers who never cross are omitted.
--
-- Approach: Aggregate the first crossing time, then pick the earliest transaction on or after it.
-- Common mistake: Joining every later transaction without row_number returns the whole tail, not the first event.

WITH crossed AS (
    SELECT customer_id,
           MIN(event_date) AS crossed_at
    FROM risk_events
    WHERE risk_score < 640
    GROUP BY customer_id
), ranked AS (
    SELECT t.customer_id,
           t.transaction_id,
           t.timestamp,
           ROW_NUMBER() OVER (PARTITION BY t.customer_id ORDER BY t.timestamp) AS rn
    FROM transactions AS t
    JOIN crossed AS c
      ON t.customer_id = c.customer_id
     AND t.timestamp >= c.crossed_at
)
SELECT customer_id, transaction_id, timestamp
FROM ranked
WHERE rn = 1;
