"""PostgreSQL interview queries on the laboratory schema.

The schema is customers, accounts, transactions, merchants, loans, payments,
fraud_events, and risk_events, as produced by scripts/generate_data.py.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SqlProblem:
    level: str
    slug: str
    title: str
    prompt: str
    solution: str
    approach: str
    mistake: str


def build_sql_problems() -> list[SqlProblem]:
    problems: list[SqlProblem] = []

    def add(level: str, slug: str, title: str, prompt: str, solution: str, approach: str, mistake: str) -> None:
        problems.append(SqlProblem(level, slug, title, prompt, solution.strip() + "\n", approach, mistake))

    entities = [("customer", "customer_id"), ("merchant", "merchant_id")]
    metrics = [("amount", "SUM(amount)", "spend"), ("volume", "COUNT(*)", "transaction count")]
    thresholds = [25, 50, 100]
    for entity, key in entities:
        for metric_name, metric_sql, metric_label in metrics:
            for threshold in thresholds:
                add(
                    "intermediate",
                    f"mom_{entity}_{metric_name}_{threshold}",
                    f"{entity} {metric_label} up more than {threshold}%",
                    (
                        f"Find {entity}s whose monthly {metric_label} increased by more than {threshold}% "
                        "versus the previous calendar month. Ignore months with a zero or missing prior value. "
                        "Do not treat a missing month as zero unless the question says so; here a missing month "
                        "means there is no row to compare."
                    ),
                    f"""
WITH monthly AS (
    SELECT {key} AS entity_id,
           date_trunc('month', timestamp)::date AS month_start,
           {metric_sql} AS metric_value
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
  AND cur.metric_value > prev.metric_value * (1 + {threshold} / 100.0);
""",
                    "Aggregate to the calendar month, join each month to the prior calendar month, and filter on the ratio.",
                    "Using LAG without checking that the previous row is the previous calendar month treats a gap as a real prior month.",
                )

    for entity, key in entities:
        for k in (1, 3, 5):
            add(
                "intermediate",
                f"top_{k}_{entity}_by_month",
                f"Top {k} {entity}s by monthly amount",
                f"For each calendar month, return the top {k} {entity}s by total amount. Break ties by {key}.",
                f"""
WITH monthly AS (
    SELECT date_trunc('month', timestamp)::date AS month_start,
           {key} AS entity_id,
           SUM(amount) AS total_amount
    FROM transactions
    GROUP BY 1, 2
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY month_start
               ORDER BY total_amount DESC, entity_id
           ) AS rn
    FROM monthly
)
SELECT month_start, entity_id, total_amount, rn
FROM ranked
WHERE rn <= {k};
""",
                f"Aggregate, then ROW_NUMBER partitioned by month. Filter rn <= {k}.",
                "RANK keeps ties and can return more than k rows. Say which behavior you want.",
            )

    windows = [("7 days", "7"), ("30 days", "30"), ("24 hours", "1")]
    for label, days in windows:
        add(
            "advanced",
            f"rolling_{days}_amount",
            f"Trailing {label} amount",
            (
                f"For each transaction, compute the sum of that customer's amounts over the trailing {label}, "
                "including the current transaction. The frame must not see future rows."
            ),
            f"""
SELECT transaction_id,
       customer_id,
       timestamp,
       amount,
       SUM(amount) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           RANGE BETWEEN INTERVAL '{days} days' PRECEDING AND CURRENT ROW
       ) AS trailing_amount
FROM transactions;
""",
            "A window ordered by time, with RANGE limited to the trailing interval, is the point-in-time sum.",
            "ROWS BETWEEN 7 PRECEDING is seven rows, not seven days.",
        )

    for z in (2, 3, 4):
        add(
            "advanced",
            f"amount_z_{z}",
            f"Amounts more than {z} prior standard deviations",
            (
                f"Flag transactions whose amount is more than {z} standard deviations above the customer's "
                "history strictly before that transaction."
            ),
            f"""
WITH scored AS (
    SELECT transaction_id,
           customer_id,
           amount,
           AVG(amount) OVER (
               PARTITION BY customer_id
               ORDER BY timestamp
               ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
           ) AS prior_mean,
           STDDEV_SAMP(amount) OVER (
               PARTITION BY customer_id
               ORDER BY timestamp
               ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
           ) AS prior_std
    FROM transactions
)
SELECT *
FROM scored
WHERE prior_std > 0
  AND (amount - prior_mean) / prior_std > {z};
""",
            "Use a window that ends one row before the current row so the point is not inside its own baseline.",
            "Including the current amount in the mean and standard deviation shrinks the z-score of the outlier.",
        )

    for n in (2, 3, 4):
        add(
            "advanced",
            f"consecutive_fraud_{n}",
            f"{n} consecutive fraudulent transactions",
            f"Find customers with at least {n} consecutive transactions flagged is_fraud = 1, ordered by time.",
            f"""
WITH ordered AS (
    SELECT customer_id,
           timestamp,
           is_fraud,
           ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY timestamp) AS rn,
           ROW_NUMBER() OVER (PARTITION BY customer_id, is_fraud ORDER BY timestamp) AS rn_flag
    FROM transactions
), islands AS (
    SELECT customer_id,
           rn - rn_flag AS island_key,
           COUNT(*) AS run_length
    FROM ordered
    WHERE is_fraud = 1
    GROUP BY customer_id, rn - rn_flag
)
SELECT customer_id, run_length
FROM islands
WHERE run_length >= {n};
""",
            "Gaps-and-islands: the difference of two row numbers is constant inside a consecutive run.",
            "Counting frauds in a day is not the same as consecutive transactions.",
        )

    for score in (600, 640, 700):
        add(
            "advanced",
            f"first_after_risk_{score}",
            f"First transaction after risk score crosses {score}",
            (
                f"For each customer, find the first transaction at or after the first risk_events row "
                f"whose risk_score is below {score}. Customers who never cross are omitted."
            ),
            f"""
WITH crossed AS (
    SELECT customer_id,
           MIN(event_date) AS crossed_at
    FROM risk_events
    WHERE risk_score < {score}
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
""",
            "Aggregate the first crossing time, then pick the earliest transaction on or after it.",
            "Joining every later transaction without row_number returns the whole tail, not the first event.",
        )

    for days in (1, 7, 30):
        add(
            "intermediate",
            f"running_total_{days}",
            f"Running amount by customer, {days}-day hint",
            (
                "Compute a running total of amount per customer in timestamp order. "
                f"In the interview, say how you would restrict it to {days} days if the business asked."
            ),
            f"""
SELECT transaction_id,
       customer_id,
       timestamp,
       amount,
       SUM(amount) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_amount
FROM transactions;
""",
            "A running total is SUM with the default expanding frame. A trailing window replaces UNBOUNDED PRECEDING.",
            "Ordering only by timestamp without partitioning mixes customers together.",
        )

    add(
        "beginner",
        "dedupe_transactions",
        "Keep the earliest duplicate transaction id",
        "Some transaction_id values were loaded twice. Keep the earliest timestamp for each id.",
        """
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
""",
        "ROW_NUMBER partitioned by the business key, ordered by the rule for which copy survives.",
        "DISTINCT does not let you choose which duplicate to keep when the other columns differ.",
    )
    add(
        "intermediate",
        "fraud_rate_by_country_month",
        "Fraud rate by country and month",
        "Compute the fraud rate and the fraud count by transaction country and calendar month.",
        """
SELECT country,
       date_trunc('month', timestamp)::date AS month_start,
       COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1, 2
ORDER BY 2, 1;
""",
        "Fraud rate is the mean of a 0/1 flag. Always return the denominator next to the rate.",
        "Averaging a rate of rates, weighted equally by country, is not the portfolio fraud rate.",
    )
    add(
        "intermediate",
        "customers_without_transactions",
        "Customers with no transactions",
        "Return customers who have no rows in transactions.",
        """
SELECT c.customer_id
FROM customers AS c
LEFT JOIN transactions AS t
  ON c.customer_id = t.customer_id
WHERE t.customer_id IS NULL;
""",
        "A left join plus IS NULL is the anti-join. NOT EXISTS is the same plan shape on many engines.",
        "NOT IN (SELECT customer_id ...) becomes unknown if the subquery can return NULL.",
    )
    add(
        "intermediate",
        "delinquent_loans",
        "Loans with a 30-day delinquency",
        "Find loans that have at least one payment with days_past_due >= 30.",
        """
SELECT loan_id,
       customer_id,
       MAX(days_past_due) AS worst_dpd
FROM payments
GROUP BY loan_id, customer_id
HAVING MAX(days_past_due) >= 30;
""",
        "Aggregate to the loan and filter with HAVING, because the condition is on a group.",
        "WHERE days_past_due >= 30 before the group still works here, but HAVING is the right tool for an aggregate predicate.",
    )
    add(
        "advanced",
        "expected_loss_book",
        "Portfolio expected loss",
        "For each defaulted-or-not loan, compute PD stand-in default_12m times lgd times ead, then the book sum. This is a teaching query, not a capital model.",
        """
SELECT SUM(default_12m * lgd * ead) AS portfolio_expected_loss,
       AVG(default_12m::numeric) AS observed_default_rate
FROM loans;
""",
        "Expected loss adds facility-level PD x LGD x EAD. Here the realized 0/1 label stands in for PD only as a classroom query.",
        "Do not use the realized default flag as a feature in the model that is supposed to predict it.",
    )
    add(
        "intermediate",
        "segment_case",
        "Segment customers by credit score",
        "Label customers as subprime (<620), near_prime (<700), or prime.",
        """
SELECT customer_id,
       credit_score,
       CASE
           WHEN credit_score < 620 THEN 'subprime'
           WHEN credit_score < 700 THEN 'near_prime'
           ELSE 'prime'
       END AS score_band
FROM customers;
""",
        "CASE expressions are the SQL version of a policy rule. Keep the cut points in one place.",
        "Overlapping WHEN clauses are order-dependent. Write them from the strictest bound upward.",
    )
    add(
        "advanced",
        "retention_cohort",
        "Monthly retention by signup cohort",
        "For each signup month, compute how many customers transacted in each later month, and the retention rate versus the cohort size.",
        """
WITH cohort AS (
    SELECT customer_id,
           date_trunc('month', signup_date)::date AS cohort_month
    FROM customers
), activity AS (
    SELECT DISTINCT customer_id,
           date_trunc('month', timestamp)::date AS active_month
    FROM transactions
)
SELECT c.cohort_month,
       a.active_month,
       COUNT(*) AS active_customers,
       COUNT(*)::numeric / NULLIF(COUNT(*) OVER (PARTITION BY c.cohort_month), 0) AS retention
FROM cohort AS c
JOIN activity AS a
  ON c.customer_id = a.customer_id
 AND a.active_month >= c.cohort_month
GROUP BY c.cohort_month, a.active_month;
""",
        "Attach a cohort date that does not change, then count distinct active customers by later month.",
        "Defining the cohort from the first transaction drops customers who never transact and answers a different question.",
    )
    add(
        "advanced",
        "percentile_amount",
        "Amount percentile by segment",
        "Within each customer_segment, return the 95th percentile of transaction amount using a window percentile.",
        """
SELECT DISTINCT customer_segment,
       PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY amount) AS p95_amount
FROM transactions
GROUP BY customer_segment;
""",
        "PERCENTILE_CONT is the continuous percentile. PERCENTILE_DISC returns an observed value.",
        "A global percentile hides that affluent and mass-market tickets are different populations.",
    )
    add(
        "intermediate",
        "night_fraud",
        "Fraud rate by night versus day",
        "Treat hours 0 through 5 as night. Compare fraud rate and volume.",
        """
SELECT CASE WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 0 AND 5 THEN 'night' ELSE 'day' END AS day_part,
       COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1;
""",
        "Put the hour rule in a CASE so the two rates are one aggregation, not two queries that can drift.",
        "A higher night rate with tiny volume may not be a stable segment.",
    )
    add(
        "advanced",
        "merchant_concentration",
        "Share of spend in the top merchant",
        "For each customer, compute the share of amount that went to their single largest merchant.",
        """
WITH by_merchant AS (
    SELECT customer_id,
           merchant_id,
           SUM(amount) AS merchant_amount,
           SUM(SUM(amount)) OVER (PARTITION BY customer_id) AS customer_amount
    FROM transactions
    GROUP BY customer_id, merchant_id
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY customer_id
               ORDER BY merchant_amount DESC, merchant_id
           ) AS rn
    FROM by_merchant
)
SELECT customer_id,
       merchant_id,
       merchant_amount / NULLIF(customer_amount, 0) AS top_merchant_share
FROM ranked
WHERE rn = 1;
""",
        "Aggregate to the merchant, rank inside the customer, and divide by the customer total.",
        "The customer total must be computed before filtering to rank 1, or the share becomes 1 by construction.",
    )
    add(
        "beginner",
        "refund_totals",
        "Refund totals",
        "Sum amounts where transaction_type is refund, by customer.",
        """
SELECT customer_id, SUM(amount) AS refund_amount, COUNT(*) AS refunds
FROM transactions
WHERE transaction_type = 'refund'
GROUP BY customer_id;
""",
        "Filter first, then aggregate. Say whether refunds are stored as positive amounts of type refund.",
        "Summing negative purchases as if they were refunds mixes data-quality defects with real refunds.",
    )
    add(
        "intermediate",
        "account_age_band",
        "Transactions on young accounts",
        "Return transactions where account_age_days is under 30, with the customer segment.",
        """
SELECT t.transaction_id, t.customer_id, t.amount, t.account_age_days, c.customer_segment
FROM transactions AS t
JOIN customers AS c
  ON t.customer_id = c.customer_id
WHERE t.account_age_days < 30;
""",
        "The age on the transaction is a snapshot. Joining the customer table adds attributes that were not denormalized.",
        "Filtering on a current account-open date at scoring time is a different feature from the age stored on the historical row.",
    )
    add(
        "advanced",
        "same_hour_countries",
        "Two countries in the same hour",
        "Find transactions that have another transaction for the same customer in a different country within the previous 60 minutes.",
        """
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
""",
        "A self-join on customer and a time predicate expresses 'another event in the window'.",
        "This can explode if a customer has many events. In Spark or Snowflake, prefer a window or an as-of pattern and then filter.",
    )
    add(
        "intermediate",
        "lead_next_amount",
        "Next amount for the customer",
        "Show each transaction and the customer's next amount. The last transaction has a null lead.",
        """
SELECT transaction_id,
       customer_id,
       amount,
       LEAD(amount) OVER (PARTITION BY customer_id ORDER BY timestamp) AS next_amount
FROM transactions;
""",
        "LEAD looks forward. It is useful in analysis and dangerous as a training feature.",
        "Using LEAD as a model feature is look-ahead leakage.",
    )
    add(
        "intermediate",
        "lag_amount",
        "Previous amount",
        "Show each transaction and the previous amount for that customer.",
        """
SELECT transaction_id,
       customer_id,
       amount,
       LAG(amount) OVER (PARTITION BY customer_id ORDER BY timestamp) AS previous_amount
FROM transactions;
""",
        "LAG is the previous row in the specified order. It is a legitimate feature if that row is already known.",
        "LAG is not the previous calendar day when the customer skipped a day.",
    )
    add(
        "advanced",
        "first_value_country",
        "First country seen for the customer",
        "Attach the customer's earliest transaction country to every later row.",
        """
SELECT transaction_id,
       customer_id,
       country,
       FIRST_VALUE(country) OVER (
           PARTITION BY customer_id
           ORDER BY timestamp
           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
       ) AS first_country
FROM transactions;
""",
        "FIRST_VALUE needs a frame that can see the first row. The default frame stops at the current row, which happens to include the first row if you are ordered ascending, so the unbounded frame makes the intent obvious.",
        "LAST_VALUE with the default frame returns the current row, not the last row in the partition.",
    )
    add(
        "advanced",
        "ntile_spend",
        "Spend quintiles",
        "Assign customers to five quintiles by total amount, 1 being the lowest.",
        """
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT customer_id,
       total_amount,
       NTILE(5) OVER (ORDER BY total_amount) AS spend_quintile
FROM totals;
""",
        "NTILE splits the ordered customers into buckets. Uneven counts go to the earlier buckets.",
        "Quintiles on a short book are unstable. Do not treat the cut points as a permanent policy.",
    )
    add(
        "beginner",
        "active_loans",
        "Loan status counts",
        "Count loans by status.",
        """
SELECT status, COUNT(*) AS loans, SUM(principal) AS principal
FROM loans
GROUP BY status
ORDER BY loans DESC;
""",
        "A one-dimension aggregation is the right first query before any model.",
        "Counting customers instead of loans understates exposure when a customer can have one loan in this lab but the grain is the loan.",
    )
    add(
        "intermediate",
        "payment_shortfall",
        "Payment shortfall",
        "For each loan, sum amount_due minus amount_paid.",
        """
SELECT loan_id,
       customer_id,
       SUM(amount_due - amount_paid) AS shortfall
FROM payments
GROUP BY loan_id, customer_id
HAVING SUM(amount_due - amount_paid) > 0
ORDER BY shortfall DESC;
""",
        "Shortfall is an amount, not a rate. Report both if the audience might confuse them.",
        "A customer can look current on a rate and still owe a large dollar shortfall.",
    )

    # Performance lab queries are included so the catalog covers the optimization path.
    add(
        "performance",
        "bad_country_filter",
        "A filter that cannot use an index",
        "The predicate wraps the column in a function. Rewrite it so a timestamp index can be used.",
        """
-- Slow shape: function on the column
-- SELECT * FROM transactions WHERE date_trunc('month', timestamp) = DATE '2024-11-01';
-- Faster shape: a range
SELECT *
FROM transactions
WHERE timestamp >= TIMESTAMP '2024-11-01'
  AND timestamp < TIMESTAMP '2024-12-01';
""",
        "Rewrite a function on the filtered column into a range so the planner can seek an index.",
        "An index on timestamp does not help if every row must be passed through date_trunc before the comparison.",
    )
    add(
        "performance",
        "selective_predicate_first",
        "Filter before the join",
        "Compute the November fraud rate by merchant category without joining merchants before the date filter.",
        """
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
""",
        "Filter the large fact table first, then join the small dimension.",
        "Joining the full fact table to a dimension and filtering afterward can shuffle far more data than necessary.",
    )

    group_columns = [
        "country",
        "merchant_category",
        "customer_segment",
        "payment_method",
        "currency",
        "transaction_type",
    ]
    aggregates = [
        ("txn_count", "COUNT(*)", "transaction count"),
        ("spend", "SUM(amount)", "total spend"),
        ("fraud_rate", "AVG(is_fraud::numeric)", "fraud rate"),
        ("avg_ticket", "AVG(amount)", "average ticket"),
        ("fraud_count", "SUM(is_fraud)", "fraud count"),
        ("customers", "COUNT(DISTINCT customer_id)", "distinct customers"),
    ]
    for column in group_columns:
        for agg_name, agg_sql, label in aggregates:
            add(
                "beginner",
                f"groupby_{column}_{agg_name}",
                f"{label} by {column}",
                f"Compute the {label} of transactions by {column}. Return the group, the metric, and order by the metric descending.",
                f"""
SELECT {column} AS bucket,
       {agg_sql} AS metric_value,
       COUNT(*) AS transactions
FROM transactions
GROUP BY {column}
ORDER BY metric_value DESC;
""",
                f"Group by {column} and aggregate. Keep the transaction count beside any rate so a small bucket cannot look precise.",
                "Sorting groups by a rate without a minimum volume promotes tiny noisy buckets.",
            )
    for left_i, left in enumerate(group_columns):
        for right in group_columns[left_i + 1 :]:
            add(
                "intermediate",
                f"fraud_rate_{left}_by_{right}",
                f"Fraud rate by {left} and {right}",
                f"Break the fraud rate down by {left} and {right}. Include the transaction count.",
                f"""
SELECT {left},
       {right},
       COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
GROUP BY 1, 2
HAVING COUNT(*) >= 30
ORDER BY fraud_rate DESC;
""",
                "A two-way rate with a HAVING floor is the start of a segment review, not a causal finding.",
                "A high rate on a handful of rows is not a reason to block a whole segment.",
            )
    for minimum in (1, 2, 3, 4, 5, 8, 10, 15):
        add(
            "intermediate",
            f"customers_with_{minimum}_frauds",
            f"Customers with at least {minimum} fraud labels",
            f"Return customers whose fraud-labeled transaction count is at least {minimum}.",
            f"""
SELECT customer_id, COUNT(*) AS frauds, SUM(amount) AS fraud_amount
FROM transactions
WHERE is_fraud = 1
GROUP BY customer_id
HAVING COUNT(*) >= {minimum}
ORDER BY frauds DESC, customer_id;
""",
            "Filter to the label, aggregate to the customer, and use HAVING for the count threshold.",
            "This query uses the label. It is an investigation query, not a feature you can compute before the fraud is confirmed.",
        )
    for factor in ("1.5", "2", "3", "5", "8", "10"):
        add(
            "advanced",
            f"amount_over_{factor.replace('.', '_')}_x_mean",
            f"Amount over {factor} times the customer mean",
            (
                f"Find transactions whose amount exceeds {factor} times that customer's average amount. "
                "Then explain why the average in this query is slightly biased."
            ),
            f"""
WITH stats AS (
    SELECT customer_id, AVG(amount) AS avg_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT t.transaction_id, t.customer_id, t.amount, s.avg_amount
FROM transactions AS t
JOIN stats AS s
  ON t.customer_id = s.customer_id
WHERE s.avg_amount > 0
  AND t.amount > s.avg_amount * {factor};
""",
            "Join the customer mean and filter. Say that this mean includes the current row, so a production feature should use prior rows only.",
            "Shipping the inclusive mean as a live feature makes extreme amounts look closer to normal than they were at decision time.",
        )
    for year in (2020, 2021, 2022, 2023, 2024, 2025):
        add(
            "beginner",
            f"fraud_rate_{year}",
            f"Fraud rate in {year}",
            f"Compute transaction count, fraud count, and fraud rate for calendar year {year}.",
            f"""
SELECT COUNT(*) AS transactions,
       SUM(is_fraud) AS frauds,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE timestamp >= TIMESTAMP '{year}-01-01'
  AND timestamp < TIMESTAMP '{year + 1}-01-01';
""",
            "Use a half-open timestamp range rather than a function on the column.",
            "EXTRACT(YEAR FROM timestamp) = {year} is correct and often prevents a plain index seek.",
        )
    for dpd in (15, 30, 45, 60, 90, 120):
        add(
            "intermediate",
            f"payments_dpd_{dpd}",
            f"Payments at least {dpd} days past due",
            f"Count payments and customers with days_past_due >= {dpd}.",
            f"""
SELECT COUNT(*) AS payments,
       COUNT(DISTINCT customer_id) AS customers,
       SUM(amount_due - amount_paid) AS shortfall
FROM payments
WHERE days_past_due >= {dpd};
""",
            "A delinquency bucket is a policy definition. State the DPD cut before quoting the rate.",
            "Customers and payments are different grains. A customer rate and a payment rate answer different questions.",
        )
    for offset in (1, 2, 3, 4, 5):
        add(
            "intermediate",
            f"lag_amount_{offset}",
            f"Amount lagged by {offset} transactions",
            f"For each transaction, show the customer's amount {offset} transactions earlier.",
            f"""
SELECT transaction_id,
       customer_id,
       amount,
       LAG(amount, {offset}) OVER (PARTITION BY customer_id ORDER BY timestamp) AS lagged_amount
FROM transactions;
""",
            f"LAG(amount, {offset}) stays inside the customer partition and cannot see the future.",
            "A lag of rows is not a lag of days. Say which one the feature definition uses.",
        )
    for buckets in (3, 4, 5, 10):
        add(
            "intermediate",
            f"ntile_spend_{buckets}",
            f"Spend buckets with NTILE({buckets})",
            f"Split customers into {buckets} buckets by total spend.",
            f"""
WITH totals AS (
    SELECT customer_id, SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT customer_id,
       total_amount,
       NTILE({buckets}) OVER (ORDER BY total_amount) AS spend_bucket
FROM totals;
""",
            "NTILE assigns buckets after the customer grain is built. Do not ntile raw transactions if the decision is about customers.",
            "Bucket edges from a small sample will not match next month. Refit or use fixed cut points for a policy.",
        )
    for limit in (10, 20, 50):
        add(
            "beginner",
            f"top_{limit}_merchants",
            f"Top {limit} merchants by spend",
            f"Return the {limit} merchants with the highest total amount.",
            f"""
SELECT merchant_id, SUM(amount) AS spend, COUNT(*) AS transactions
FROM transactions
GROUP BY merchant_id
ORDER BY spend DESC, merchant_id
LIMIT {limit};
""",
            "Aggregate, order, and limit. Add a tie break so the result is stable.",
            "LIMIT without an aggregate returns arbitrary transaction rows, not top merchants.",
        )
    for share in ("0.10", "0.25", "0.50"):
        add(
            "advanced",
            f"geo_mismatch_share_{share.replace('.', '_')}",
            f"Customers with country mismatch share above {share}",
            (
                f"A mismatch is a transaction country different from the customer's home country. "
                f"Return customers whose mismatch share exceeds {share} and who have at least 5 transactions."
            ),
            f"""
SELECT t.customer_id,
       AVG((t.country <> c.country)::int) AS mismatch_share,
       COUNT(*) AS transactions
FROM transactions AS t
JOIN customers AS c
  ON t.customer_id = c.customer_id
GROUP BY t.customer_id
HAVING COUNT(*) >= 5
   AND AVG((t.country <> c.country)::int) > {share};
""",
            "Define the mismatch with a join to the home country, then threshold the share and the sample size together.",
            "A single foreign transaction on a new customer is not the same evidence as a 50% mismatch rate on a long history.",
        )
    for minutes in (5, 10, 30, 60, 120):
        add(
            "advanced",
            f"repeat_merchant_{minutes}m",
            f"Same merchant again within {minutes} minutes",
            f"Find a transaction that repeats the same customer and merchant within the previous {minutes} minutes.",
            f"""
SELECT a.transaction_id, a.customer_id, a.merchant_id, a.timestamp
FROM transactions AS a
JOIN transactions AS b
  ON a.customer_id = b.customer_id
 AND a.merchant_id = b.merchant_id
 AND a.transaction_id <> b.transaction_id
 AND b.timestamp < a.timestamp
 AND b.timestamp >= a.timestamp - INTERVAL '{minutes} minutes';
""",
            "A self-join expresses a repeat event. Deduplicate if one transaction matches several priors and you only need a flag.",
            "This join multiplies rows. If the deliverable is a flag, aggregate back to one row per transaction.",
        )
    for spend in (100, 500, 1000, 5000):
        add(
            "beginner",
            f"customers_spend_over_{spend}",
            f"Customers with spend over {spend}",
            f"Return customers whose total transaction amount exceeds {spend}.",
            f"""
SELECT customer_id, SUM(amount) AS spend, COUNT(*) AS transactions
FROM transactions
GROUP BY customer_id
HAVING SUM(amount) > {spend}
ORDER BY spend DESC;
""",
            "HAVING filters after the aggregate. WHERE cannot see SUM.",
            "Putting SUM(amount) > {spend} in WHERE is a syntax error.",
        )
    for category in ("gambling", "crypto", "wire", "luxury", "travel", "electronics"):
        add(
            "intermediate",
            f"category_vs_grocery_{category}",
            f"{category} versus grocery",
            f"Compare fraud rate and average ticket for merchant_category '{category}' against grocery.",
            f"""
SELECT merchant_category,
       COUNT(*) AS transactions,
       AVG(amount) AS avg_ticket,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE merchant_category IN ('{category}', 'grocery')
GROUP BY merchant_category;
""",
            "Hold the comparison set to two categories so the reader sees a baseline, not a sorted list of everything.",
            "A higher fraud rate at a category can be mix, ticket size, or channel. Do not jump to a block rule from one query.",
        )

    for hour in range(24):
        add(
            "beginner",
            f"fraud_rate_hour_{hour:02d}",
            f"Fraud rate during hour {hour}",
            f"Compute the fraud rate and transaction count for timestamp hour {hour}.",
            f"""
SELECT COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE EXTRACT(HOUR FROM timestamp) = {hour};
""",
            "A single-hour slice is a diagnostic. Compare it with the book rate before calling it a pattern.",
            "Hour is timezone-dependent. Say which clock the timestamp uses.",
        )
    for dow, name in enumerate(["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
        add(
            "beginner",
            f"fraud_rate_{name}",
            f"Fraud rate on {name}",
            f"Compute the fraud rate for {name}. In PostgreSQL, EXTRACT(DOW) uses 0 for Sunday.",
            f"""
SELECT COUNT(*) AS transactions,
       AVG(is_fraud::numeric) AS fraud_rate
FROM transactions
WHERE EXTRACT(DOW FROM timestamp) = {dow};
""",
            "Weekday seasonality is a feature and a monitoring cut. Keep the DOW convention explicit.",
            "A quiet Sunday rate can be volume mix, not a safer population.",
        )
    for score in (500, 550, 580, 600, 620, 640, 660, 680, 700, 740):
        add(
            "intermediate",
            f"customers_score_below_{score}",
            f"Customers with credit score below {score}",
            f"Count customers and their average income with credit_score below {score}.",
            f"""
SELECT COUNT(*) AS customers,
       AVG(income) AS avg_income,
       AVG(credit_score) AS avg_score
FROM customers
WHERE credit_score < {score};
""",
            "A score cut is a policy. Report the count under the cut, not only the average score.",
            "The same cut on a different scorecard is not the same risk.",
        )

    if len(problems) < 200:
        raise RuntimeError(f"SQL catalog has only {len(problems)} problems")
    slugs = [problem.slug for problem in problems]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("Duplicate SQL slug")
    return problems
