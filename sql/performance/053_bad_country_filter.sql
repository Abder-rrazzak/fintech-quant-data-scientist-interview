-- A filter that cannot use an index
-- Level: performance
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- The predicate wraps the column in a function. Rewrite it so a timestamp index can be used.
--
-- Approach: Rewrite a function on the filtered column into a range so the planner can seek an index.
-- Common mistake: An index on timestamp does not help if every row must be passed through date_trunc before the comparison.

-- Slow shape: function on the column
-- SELECT * FROM transactions WHERE date_trunc('month', timestamp) = DATE '2024-11-01';
-- Faster shape: a range
SELECT *
FROM transactions
WHERE timestamp >= TIMESTAMP '2024-11-01'
  AND timestamp < TIMESTAMP '2024-12-01';
