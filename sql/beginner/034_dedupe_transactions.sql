-- Keep the earliest duplicate transaction id
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Some transaction_id values were loaded twice. Keep the earliest timestamp for each id.
--
-- Approach: ROW_NUMBER partitioned by the business key, ordered by the rule for which copy survives.
-- Common mistake: DISTINCT does not let you choose which duplicate to keep when the other columns differ.

SELECT transaction_id, customer_id, timestamp, amount, is_fraud
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY transaction_id
               ORDER BY timestamp, customer_id
           ) AS rn
    FROM transactions
) AS ranked
WHERE rn = 1;
