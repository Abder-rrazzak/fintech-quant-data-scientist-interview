-- customer spend up more than 25%
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find customers whose monthly spend increased by more than 25% versus the previous calendar month. Ignore months with a zero or missing prior value. Do not treat a missing month as zero unless the question says so; here a missing month means there is no row to compare.
--
-- Approach: Aggregate to the calendar month, join each month to the prior calendar month, and filter on the ratio.
-- Common mistake: Using LAG without checking that the previous row is the previous calendar month treats a gap as a real prior month.

WITH monthly AS (
    SELECT customer_id AS entity_id,
           date_trunc('month', timestamp)::date AS month_start,
           SUM(amount) AS metric_value
    FROM transactions
    GROUP BY 1, 2
)
SELECT cur.entity_id,
       cur.month_start,
       cur.metric_value,
       prev.metric_value AS previous_value,
       (cur.metric_value - prev.metric_value) / prev.metric_value AS pct_change
FROM monthly AS cur
JOIN monthly AS prev
  ON cur.entity_id = prev.entity_id
 AND cur.month_start = (prev.month_start + INTERVAL '1 month')::date
WHERE prev.metric_value > 0
  AND cur.metric_value > prev.metric_value * (1 + 25 / 100.0);
