-- Refund totals
-- Level: beginner
-- Dialect: PostgreSQL / Snowflake-compatible teaching SQL.
--
-- Sum amounts where transaction_type is refund, by customer.
--
-- Approach: Filter first, then aggregate. Say whether refunds are stored as positive amounts of type refund.
-- Common mistake: Summing negative purchases as if they were refunds mixes data-quality defects with real refunds.

SELECT customer_id, SUM(amount) AS refund_amount, COUNT(*) AS refunds
FROM transactions
WHERE transaction_type = 'refund'
GROUP BY customer_id;
