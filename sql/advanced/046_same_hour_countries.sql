-- Two countries in the same hour
-- Level: advanced
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Find transactions that have another transaction for the same customer in a different country within the previous 60 minutes.
--
-- Approach: A self-join on customer and a time predicate expresses 'another event in the window'.
-- Common mistake: This can explode if a customer has many events. In Spark or Snowflake, prefer a window or an as-of pattern and then filter.

SELECT a.transaction_id,
       a.customer_id,
       a.timestamp,
       a.country,
       b.country AS other_country
FROM transactions AS a
JOIN transactions AS b
  ON a.customer_id = b.customer_id
 AND a.transaction_id <> b.transaction_id
 AND b.timestamp <= a.timestamp
 AND b.timestamp > a.timestamp - INTERVAL '60 minutes'
 AND a.country <> b.country;
