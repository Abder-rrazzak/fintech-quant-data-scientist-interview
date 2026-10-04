-- Segment customers by credit score
-- Level: intermediate
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Label customers as subprime (<620), near_prime (<700), or prime.
--
-- Approach: CASE expressions are the SQL version of a policy rule. Keep the cut points in one place.
-- Common mistake: Overlapping WHEN clauses are order-dependent. Write them from the strictest bound upward.

SELECT customer_id,
       credit_score,
       CASE
           WHEN credit_score < 620 THEN 'subprime'
           WHEN credit_score < 700 THEN 'near_prime'
           ELSE 'prime'
       END AS score_band
FROM customers;
