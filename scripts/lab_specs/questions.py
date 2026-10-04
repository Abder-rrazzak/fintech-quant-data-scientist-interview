"""Interview questions assembled from the flagship set, topic catalogs, and SQL labs."""

from __future__ import annotations

from lab_specs.catalogs import BEHAVIORAL, CASE_STUDIES, COMMUNICATION, DESIGNS, TOPIC_QUESTIONS


def build_questions(sql_problems, python_problems) -> list[dict]:
    questions = [_pack(**item) for item in FLAGSHIP]
    for item in TOPIC_QUESTIONS:
        questions.append(_pack(**item))
    for problem in python_problems:
        topic = problem.topic
        if topic not in {"pandas", "numpy"}:
            topic = "python"
        questions.append(
            {
                "id": f"py-{problem.slug}",
                "topic": topic,
                "difficulty": problem.level,
                "section": topic,
                "prompt": f"{problem.title}. {problem.prompt}",
                "answer_30s": "Solve it with an explicit, testable function and state the edge cases before optimizing.",
                "answer_2min": (
                    f"{problem.prompt} I would implement `{problem.function_name}` and cover empty inputs, "
                    "boundaries, and the financial grain. A fast wrong window is worse than a slow correct one."
                ),
                "deep_dive": problem.solution_body,
                "follow_ups": [
                    "What is the time complexity?",
                    "Which edge case would you test first?",
                ],
                "common_mistake": "Writing the happy path only, or using a future row in a feature that is supposed to be known now.",
            }
        )
    for problem in sql_problems:
        questions.append(
            {
                "id": f"sql-{problem.slug}",
                "topic": "sql",
                "difficulty": "advanced" if problem.level in {"advanced", "performance"} else "intermediate",
                "section": "SQL",
                "prompt": problem.prompt,
                "answer_30s": problem.approach,
                "answer_2min": f"{problem.approach} The business question is: {problem.prompt}",
                "deep_dive": problem.solution + "\nCommon mistake: " + problem.mistake,
                "follow_ups": [
                    "What is the grain of the result?",
                    "How does the plan change if the fact table is huge?",
                ],
                "common_mistake": problem.mistake,
            }
        )
    _require(questions)
    for index, question in enumerate(questions):
        if not question["id"]:
            question["id"] = f"{question['topic']}-{index}"
    return questions


def _pack(topic, difficulty, prompt, short, medium, deep, follow, mistake, section=None, qid=""):
    return {
        "id": qid,
        "topic": topic,
        "difficulty": difficulty,
        "section": section or topic,
        "prompt": prompt,
        "answer_30s": short,
        "answer_2min": medium,
        "deep_dive": deep,
        "follow_ups": follow,
        "common_mistake": mistake,
    }


def _require(questions: list[dict]) -> None:
    counts: dict[str, int] = {}
    for question in questions:
        counts[question["topic"]] = counts.get(question["topic"], 0) + 1
    minimums = {
        "python": 40,
        "sql": 100,
        "statistics": 100,
        "machine_learning": 30,
        "predictive_modeling": 30,
        "fraud": 30,
        "anomaly": 20,
        "credit_risk": 20,
        "clv": 15,
        "pandas": 50,
        "numpy": 30,
        "time_series": 30,
        "backtesting": 20,
        "spark": 30,
        "snowflake": 30,
        "aws": 30,
        "validation": 30,
        "bias": 20,
        "business": 30,
        "system_design": 30,
        "behavioral": 12,
    }
    missing = {topic: (counts.get(topic, 0), need) for topic, need in minimums.items() if counts.get(topic, 0) < need}
    if missing:
        raise RuntimeError(f"Question bank is short: {missing}")


def _f(topic, difficulty, prompt, short, medium, deep, mistake, follow=None):
    return {
        "topic": topic,
        "difficulty": difficulty,
        "prompt": prompt,
        "short": short,
        "medium": medium,
        "deep": deep,
        "follow": follow
        or [
            "What would you measure next?",
            "What would change your recommendation?",
        ],
        "mistake": mistake,
    }


FLAGSHIP = [
    _f(
        "pandas",
        "advanced",
        "How would you optimize a Pandas pipeline processing 100 million transactions?",
        "I would not run that volume as one in-memory Pandas frame. I would project columns, downcast types, filter early, and push the heavy aggregation to SQL or Spark.",
        "A 100 million row extract with object columns and a few merges can exceed the machine before any model fits. I profile the peak-memory line, read only columns the decision needs, use categoricals for low-cardinality fields, and ban row-wise apply. Associative reductions can stream in chunks. Anything that still needs a full shuffle belongs in the warehouse, and Pandas trains on the reduced feature table.",
        "Float32 is acceptable for many amount features and unacceptable if you must reproduce cent-level balances. Merges should happen after the fact table is filtered to the training window. toPandas on the full extract is the failure mode this question is designed to catch. If the operation is a customer-level aggregate, compute it where the data already lives and only then open Pandas.",
        "Rewriting idioms while still holding several full copies of the extract in memory.",
    ),
    _f(
        "sql",
        "advanced",
        "Write a query using window functions to identify customers whose transaction volume increased by more than 50% month-over-month.",
        "Aggregate to the customer-month, compare each month with the previous calendar month, and keep rows where volume exceeds 1.5 times a positive prior month.",
        "The grain is customer and calendar month. I define volume as count or amount up front. A join on month_start = previous month plus one month is safer than LAG, because LAG treats a skipped month as the previous month. I return both volumes so a jump from 2 to 4 is not confused with a jump from 2,000 to 3,000.",
        "WITH monthly AS (SELECT customer_id, date_trunc('month', timestamp)::date AS month_start, COUNT(*) AS volume FROM transactions GROUP BY 1, 2) SELECT cur.customer_id, cur.month_start, cur.volume, prev.volume AS prev_volume FROM monthly cur JOIN monthly prev ON cur.customer_id = prev.customer_id AND cur.month_start = (prev.month_start + INTERVAL '1 month')::date WHERE prev.volume > 0 AND cur.volume > prev.volume * 1.5;",
        "Using LAG on sparse customer-months and calling that the previous calendar month.",
    ),
    _f(
        "credit_risk",
        "advanced",
        "How would you build a credit risk model?",
        "I would model 12-month probability of default at origination, use only information known then, and set the cutoff from expected loss and approval rate.",
        "The unit is the loan. Unseasoned loans stay out of the labeled set. Features are income, utilization, debt burden, history, and account age at decision time. Logistic regression is the explainable baseline; a boosted tree is the challenger. I report ROC-AUC, KS, calibration, and the approval-versus-loss curve. Expected loss is PD times LGD times EAD. The model estimates PD. A later-origination split is the validation. I retrain when vintage performance or feature PSI moves the cutoff, not on a calendar whim.",
        "A constant LGD in this laboratory is a teaching assumption, not a regulatory downturn LGD. Using the default flag, post-origination utilization, or a random split are the usual ways to publish a number that production will not repeat. The recommendation to risk is a cutoff on the frontier, shadow-tested, not a claim that accuracy improved.",
        "Optimizing accuracy and treating 0.5 as the credit policy.",
    ),
    _f(
        "fraud",
        "advanced",
        "How would you detect fraud when only 0.1% of transactions are fraudulent?",
        "I would rank with point-in-time features, judge the ranking with PR-AUC, and choose review and block thresholds from the cost of a miss versus the cost of a false review.",
        "Accuracy is about 99.9% for a model that flags nothing. Useful features are velocity, amount versus the customer's own past, geography, device, merchant risk, and hour. A linear model or gradient boosting is the baseline a neural net has to beat. Because labels are late, I monitor precision in the review queue and leakage of fraud past the approve decision. Downsampling legitimate cases can help the fit and destroys calibration unless you correct it. The threshold is chosen on a validation window that still has the real base rate.",
        "An isolation forest or an autoencoder reconstruction error finds unusual transactions. Unusual is not the same as fraudulent. I would use anomaly scores to propose new rules and to fill a review queue, and I would not quote them as a probability of the 0.1% event. Two thresholds, approve and review and block, match the operation better than one cutoff.",
        "Leading with ROC-AUC and a 0.5 threshold.",
    ),
    _f(
        "statistics",
        "advanced",
        "How would you determine whether a change in fraud rate is statistically significant?",
        "I would compare the two rates with their sample sizes, show a confidence interval, and separate a detectable difference from a difference that changes loss or staffing.",
        "A two-proportion z-test fits large independent samples. One thousand frauds in a million transactions is a different statement from ten frauds in a thousand. Clustering by customer or by attack makes the naive test too confident, because the effective sample is the number of clusters. I also check mix: a new country or a labeling delay can move the rate. A p-value is not the probability the increase is real, and a handful of sliced p-values will produce a red cell by chance.",
        "Practical significance is extra dollars and extra reviews. I would pre-state the comparison window so I am not testing every hour until one hour looks bad. If I must monitor continuously, the threshold has to account for repeated looks. The laboratory implementation is evaluation.two_proportion_ztest.",
        "Acting on the first slice that falls below 0.05, or ignoring a large dollar gap because a small sample missed 0.05.",
    ),
    _f(
        "time_series",
        "advanced",
        "How would you validate a financial forecasting model without leakage?",
        "I would train on earlier years, validate on the next year, and test on a later year I did not use to choose the model. Features at each origin use only information already known.",
        "A random row split on a price history trains on the future and tests on the past. For a 2020-2025 series I train through 2023, validate on 2024, and touch 2025 once. Rolling z-scores and volatility must be computed inside each origin, not on the full sample before the split. I report error on the business scale and, if the decision is a position, the result after costs. A low RMSE that dies after 10 basis points is not an edge.",
        "Look-ahead bias includes revised data, a universe chosen because the names still exist, and any label window that overlaps the test period. Concept drift is why one lucky year is not a model. Walk-forward origins show whether the error is stable. This is the opposite of k-fold on shuffled days.",
        "Where would a full-sample z-score leak, and what is survivorship bias in a price history?",
    ),
    _f(
        "backtesting",
        "advanced",
        "How would you design a robust backtesting framework?",
        "Every test segment starts after its training segment. I would walk forward, charge costs and slippage, and show every origin rather than the best one.",
        "Expanding windows use all history before the origin. Rolling windows deliberately forget old regimes. If the label horizon overlaps the next origin, I purge the training rows whose labels reach into the test window. The ledger records the signal, the assumed fill, turnover, and cost in basis points. Random cross-validation is not a backtest, because neighboring days share a regime and a shuffle lets Tuesday train Monday.",
        "The framework in this lab checks that the maximum training index is strictly before the minimum test index. That single assertion catches the most common leak. Costs are a parameter, not a footnote. I would rather publish a smaller net result than a gross result that assumes free trading.",
        "Treating the best cutoff on the same history as an out-of-sample result.",
    ),
    _f(
        "spark",
        "advanced",
        "How would you process billions of transactions?",
        "I would partition the fact data by event date, broadcast small dimensions, aggregate before any Python, and never collect the full fact table to the driver.",
        "Spark pays for shuffles. A join of two large unpartitioned facts is the expensive case. A date filter should prune partitions. A merchant table that truly fits can be broadcast. Skewed keys need salting or adaptive execution. Pandas is appropriate once the grain is a customer table or a sample. Spark is the wrong tool for a few hundred megabytes, a one-off notebook, or the authorization path that needs a response in tens of milliseconds.",
        "Cache a frame you reuse and whose size you know. Coalesce, rather than a full repartition, when you only need fewer output files. A wide transformation is the line I would find in the Spark UI before I asked for a larger cluster. This repository includes a local job and a Pandas reference plan so the logic can be tested without a cluster.",
        "Calling toPandas on the full extract, or reaching for Spark because the data is 'financial'.",
    ),
    _f(
        "snowflake",
        "advanced",
        "How would you optimize a slow analytical query?",
        "I would read the query profile, turn the filter into a range that can prune micro-partitions, and only then decide whether the warehouse is the wrong size.",
        "Snowflake separates storage and compute. Bytes scanned, partitions pruned, join type, and spill tell you whether the problem is the SQL or the warehouse. A function wrapped around the filtered timestamp often disables pruning. Clustering helps a large table when the filter matches the cluster key, and it costs maintenance. A warehouse bills while it runs, so auto-suspend is part of the design. A daily aggregate or a materialized result beats scanning the raw table for every dashboard refresh.",
        "Time Travel lets you query a previous version and is not a performance feature. Streams and tasks move increments. They do not make a bad join cheap. In this lab the same habits are practiced on local SQL: filter early, do not wrap the predicate column, and aggregate before the wide join. No Snowflake account is required.",
        "Scaling the warehouse up before looking at the profile.",
    ),
    _f(
        "aws",
        "advanced",
        "Design a production architecture for real-time fraud detection.",
        "The transaction hits an API, is written to a stream, joined to fresh features, scored, and returned as approve, review, or block. The raw event is stored for labels and monitoring.",
        "Batch training is object storage, a processing job, a registry, and a model the scorer can load. The online path cannot wait for the nightly job, so features have an online copy and an offline definition that must match. A timeout needs a default decision, usually a simple rule or a review, because a hung model cannot stall authorization. Metrics are latency, queue age, score drift, and the precision of what reviewers actually see.",
        "IAM should let the scorer read the model and the feature values it needs and nothing else. This repository demonstrates the decision and the feature-timestamp rule locally. The AWS diagram is a target architecture, not a claim that I operated that stack in production.",
        "A diagram of service logos with no timeout decision and no feature timestamp.",
    ),
    _f(
        "system_design",
        "advanced",
        "Design an enterprise credit-risk prediction platform.",
        "Score probability of default with features frozen at application time, let a policy turn that PD into a decision using expected loss, and judge the book by seasoned vintages.",
        "The online path is an application service, a feature snapshot, a model, and a cutoff that risk can change without a retrain. Training uses only loans old enough to have defaulted or not. Monitoring is approval rate, score PSI, and realized default by vintage. A recent vintage that looks clean is censored, not proof the model improved. Explanations are coefficients or reason codes a credit officer can read.",
        "Product will ask for a higher approval rate and risk will ask for a lower default rate. The honest artifact is the curve of cutoff versus both, plus a shadow period. I would not describe this as a platform I have already run at a lender. It is the design this laboratory implements in small form.",
        "Retraining on unseasoned originations and concluding that recent loans are safe.",
    ),
    _f(
        "business",
        "advanced",
        "Your model improves recall but increases false positives by 40%. What do you recommend?",
        "I would price the extra fraud caught against the extra reviews and ship a threshold the queue can staff, or keep the current rule if the net cost is worse.",
        "Recall is not the decision. At the proposed threshold I want the extra true positives, the extra false positives, and the investigator hours. If misses are expensive and the team has capacity, a controlled rollout can be right. If the queue is already late, I raise the threshold until the false-positive increase fits, and I give back some recall on purpose. A shadow week checks that queue precision matches the offline estimate.",
        "The sentence I would use: the new score ranks better, and at today's threshold it would raise recall while adding about 40% more false reviews. I recommend a threshold that holds review volume flat, a two-week shadow, and a rollback if precision in the queue drops. I would not open with the AUC change.",
        "Announcing an AUC gain and leaving the 40% workload increase unpriced.",
    ),
    _f(
        "validation",
        "advanced",
        "How do you detect data leakage in a financial model?",
        "I check whether every feature was known at the decision, whether the split puts the future in training, and whether the metric is implausibly good for the base rate.",
        "Labels, post-decision balances, and investigator timestamps are banned columns. Subtler leakage is a customer aggregate computed on the whole history, including the row you are scoring, or a random split of many rows from the same account. I want a test that a feature timestamp after the decision raises an error. If a 0.1% fraud label produces a spectacular PR-AUC, I rebuild the features point-in-time before I believe it.",
        "The fix is not a different algorithm. It is to recompute the feature as of the decision and rescore. If the metric collapses, the old result was leakage. Grouping splits by customer matters when the feature is a customer history. Time splits matter when the book is drifting.",
        "Trusting a high AUC without asking when each column was known.",
    ),
    _f(
        "machine_learning",
        "intermediate",
        "When do you prefer PR-AUC over ROC-AUC?",
        "When positives are rare and the job is the precision of the queue you will actually work. ROC-AUC can look fine while that queue is mostly false alarms.",
        "ROC-AUC uses the false-positive rate, whose denominator is all the legitimate cases. PR-AUC uses precision and recall. I still quote ROC-AUC and KS for credit because that is the language of the scorecard discussion, and I pick the threshold from cost or from recall at a fixed precision. Accuracy is the wrong headline for both fraud and a low default rate. A base-rate shift changes PR-AUC even when the ranking does not, so I compare models on the same window.",
        "Calibration is separate. A model can rank well and still be a bad probability. Brier score and a calibration curve answer that. Resampling the training set and then reading predict_proba as a fraud rate mixes those two questions.",
        "Claiming a better model because accuracy moved from 99.8% to 99.9%.",
    ),
    _f(
        "anomaly",
        "intermediate",
        "Why is an outlier not the same thing as fraud?",
        "An outlier is unusual under a reference distribution. Fraud is a business label. Large legitimate purchases are often outliers, and some fraud is deliberately ordinary.",
        "Z-scores, IQR fences, isolation forests, and autoencoder error all answer 'how unusual is this row?'. They do not know the loss. I use them to propose reviews and new rules, then I measure precision against confirmed labels. If I threshold an anomaly score, I still do it with a cost or a review-capacity constraint, not because the point was far from the mean.",
        "A linear autoencoder is PCA reconstruction. It finds linear unusualness. A neural autoencoder is justified only if that residual misses a pattern a tree or a rule cannot see, and only if I can monitor the residual in production. In this lab the PCA residual is the always-on teaching version.",
        "Blocking every statistical outlier and calling the block rate a fraud catch rate.",
    ),
    _f(
        "python",
        "intermediate",
        "Why is DataFrame.apply often slower than a vectorized operation?",
        "apply usually loops in Python. A vectorized NumPy or Pandas expression runs the loop in compiled code over a contiguous array.",
        "Axis=1 apply is the expensive form because each row becomes a Series and a Python function call. A column of amounts can be clipped, logged, or standardized with array operations. groupby aggregations are also compiled. I reach for apply when the function is genuinely awkward to vectorize, and I check the timing on a realistic slice before I leave it in a pipeline. For 100 million rows I would not use apply as the design.",
        "The same point shows up in a pure Python loop over customer histories versus a searchsorted or a window function. Correctness still comes first: a fast vectorized feature that uses the future is worse than a slow feature that does not. After the definition is point-in-time, the implementation should leave Python.",
        "Assuming apply is fine because the notebook finished on 50,000 rows.",
    ),
]
