"""Intermediate Python exercises."""

from __future__ import annotations

RAW: list[tuple] = []


def A(*row: object) -> None:
    RAW.append(row)


A("intermediate", "generators", "batch_stream", "Yield batches",
  "Yield successive batches of size n.",
  "batch_stream", "items: list[int], size: int",
  "if size <= 0:\n    raise ValueError('size')\nfor i in range(0, len(items), size):\n    yield items[i:i + size]",
  "from solution import batch_stream\n\ndef test_batches():\n    assert list(batch_stream([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]\n")
A("intermediate", "generators", "running_mean_stream", "Streaming running mean",
  "Yield the running mean after each value.",
  "running_mean_stream", "values: list[float]",
  "total = 0.0\nfor i, value in enumerate(values, start=1):\n    total += value\n    yield total / i",
  "from solution import running_mean_stream\n\ndef test_stream():\n    assert list(running_mean_stream([2.0, 4.0, 6.0])) == [2.0, 3.0, 4.0]\n")
A("intermediate", "generators", "pairwise_stream", "Consecutive pairs",
  "Yield (previous, current) after the first item.",
  "pairwise_stream", "values: list[float]",
  "for i in range(1, len(values)):\n    yield (values[i - 1], values[i])",
  "from solution import pairwise_stream\n\ndef test_pairs():\n    assert list(pairwise_stream([1, 3, 6])) == [(1, 3), (3, 6)]\n")
A("intermediate", "iterators", "take_first", "Take the first n items",
  "Return the first n items of an iterable.",
  "take_first", "items, n: int",
  "if n < 0:\n    raise ValueError('n')\nout = []\nfor item in items:\n    if len(out) == n:\n        break\n    out.append(item)\nreturn out",
  "from solution import take_first\n\ndef test_take():\n    assert take_first(iter([1, 2, 3, 4]), 2) == [1, 2]\n")
A("intermediate", "decorators", "non_negative", "Reject negative amounts",
  "Decorator that raises ValueError if the first argument is negative.",
  "non_negative", "func",
  "def wrapper(value, *args, **kwargs):\n    if value < 0:\n        raise ValueError('negative')\n    return func(value, *args, **kwargs)\nreturn wrapper",
  "from solution import non_negative\n\ndef test_decorator():\n    @non_negative\n    def identity(value):\n        return value\n    assert identity(3) == 3\n    try:\n        identity(-1)\n        raise AssertionError('expected')\n    except ValueError:\n        pass\n")
A("intermediate", "decorators", "count_calls", "Count calls",
  "Decorator that stores the call count on wrapper.calls.",
  "count_calls", "func",
  "def wrapper(*args, **kwargs):\n    wrapper.calls += 1\n    return func(*args, **kwargs)\nwrapper.calls = 0\nreturn wrapper",
  "from solution import count_calls\n\ndef test_calls():\n    @count_calls\n    def add(a, b):\n        return a + b\n    add(1, 2)\n    add(0, 0)\n    assert add.calls == 2\n")
A("intermediate", "typing", "parse_record", "Parse a record",
  "Return (customer_id, amount) from a dict.",
  "parse_record", "record: dict[str, object]",
  "return int(record['customer_id']), float(record['amount'])",
  "from solution import parse_record\n\ndef test_parse():\n    assert parse_record({'customer_id': '7', 'amount': '3.5'}) == (7, 3.5)\n")
A("intermediate", "logging", "decision_message", "Decision log line",
  "Return decision=<value> score=<score with 3 decimals>.",
  "decision_message", "decision: str, score: float",
  "return f'decision={decision} score={score:.3f}'",
  "from solution import decision_message\n\ndef test_msg():\n    assert decision_message('review', 0.2) == 'decision=review score=0.200'\n")
A("intermediate", "testing", "confusion_counts", "Confusion counts",
  "Return tp, fp, tn, fn for binary labels.",
  "confusion_counts", "y_true: list[int], y_pred: list[int]",
  "if len(y_true) != len(y_pred):\n    raise ValueError('length')\ntp = fp = tn = fn = 0\nfor truth, pred in zip(y_true, y_pred):\n    if pred == 1 and truth == 1:\n        tp += 1\n    elif pred == 1 and truth == 0:\n        fp += 1\n    elif pred == 0 and truth == 0:\n        tn += 1\n    else:\n        fn += 1\nreturn {'tp': tp, 'fp': fp, 'tn': tn, 'fn': fn}",
  "from solution import confusion_counts\n\ndef test_cm():\n    assert confusion_counts([1, 0, 1, 0], [1, 1, 0, 0]) == {'tp': 1, 'fp': 1, 'tn': 1, 'fn': 1}\n")
A("intermediate", "testing", "precision_recall", "Precision and recall",
  "Return (precision, recall). Empty denominators yield 0.",
  "precision_recall", "tp: int, fp: int, fn: int",
  "precision = tp / (tp + fp) if (tp + fp) else 0.0\nrecall = tp / (tp + fn) if (tp + fn) else 0.0\nreturn (precision, recall)",
  "from solution import precision_recall\n\ndef test_pr():\n    assert precision_recall(2, 2, 0) == (0.5, 1.0)\n")
A("intermediate", "functions", "brier_score", "Brier score",
  "Mean squared error between probabilities and binary labels.",
  "brier_score", "y_true: list[int], probs: list[float]",
  "if len(y_true) != len(probs) or not y_true:\n    raise ValueError('shape')\nreturn sum((probs[i] - y_true[i]) ** 2 for i in range(len(y_true))) / len(y_true)",
  "from solution import brier_score\n\ndef test_brier():\n    assert brier_score([1, 0], [1.0, 0.0]) == 0.0\n")
A("intermediate", "functions", "expected_loss_identity", "Expected loss",
  "Return PD x LGD x EAD.",
  "expected_loss_identity", "pd: float, lgd: float, ead: float",
  "if not 0 <= pd <= 1 or not 0 <= lgd <= 1 or ead < 0:\n    raise ValueError('inputs')\nreturn pd * lgd * ead",
  "from solution import expected_loss_identity\n\ndef test_el():\n    assert abs(expected_loss_identity(0.02, 0.45, 10000) - 90.0) < 1e-6\n")
A("intermediate", "functions", "sigmoid_score", "Safe sigmoid",
  "Sigmoid with the logit clipped to [-30, 30].",
  "sigmoid_score", "value: float",
  "import math\nx = min(max(value, -30.0), 30.0)\nreturn 1.0 / (1.0 + math.exp(-x))",
  "from solution import sigmoid_score\n\ndef test_sig():\n    assert sigmoid_score(0) == 0.5\n")
A("intermediate", "functions", "time_split_indexes", "Time split indexes",
  "Return (train_end, valid_end) for a 70/15/15 split of n ordered rows.",
  "time_split_indexes", "n: int",
  "if n < 3:\n    raise ValueError('n')\ntrain_end = max(1, int(n * 0.70))\nvalid_end = min(n - 1, max(train_end + 1, int(n * 0.85)))\nreturn train_end, valid_end",
  "from solution import time_split_indexes\n\ndef test_idx():\n    train_end, valid_end = time_split_indexes(100)\n    assert 0 < train_end < valid_end < 100\n")
A("intermediate", "functions", "cost_at_threshold", "Cost at a threshold",
  "Predicted positive means score >= threshold. Cost is fp * fp_cost + fn * fn_cost.",
  "cost_at_threshold", "y_true: list[int], scores: list[float], threshold: float, fp_cost: float, fn_cost: float",
  "fp = fn = 0\nfor truth, score in zip(y_true, scores):\n    pred = score >= threshold\n    if pred and truth == 0:\n        fp += 1\n    if (not pred) and truth == 1:\n        fn += 1\nreturn fp * fp_cost + fn * fn_cost",
  "from solution import cost_at_threshold\n\ndef test_cost():\n    assert cost_at_threshold([1, 0], [0.2, 0.9], 0.5, 5, 500) == 505\n")
A("intermediate", "functions", "fraud_decision", "Approve, review, or block",
  "Map a score to approve, review, or block.",
  "fraud_decision", "score: float, review_threshold: float, block_threshold: float",
  "if block_threshold < review_threshold:\n    raise ValueError('thresholds')\nif score >= block_threshold:\n    return 'block'\nif score >= review_threshold:\n    return 'review'\nreturn 'approve'",
  "from solution import fraud_decision\n\ndef test_decision():\n    assert fraud_decision(0.1, 0.4, 0.8) == 'approve'\n    assert fraud_decision(0.5, 0.4, 0.8) == 'review'\n    assert fraud_decision(0.9, 0.4, 0.8) == 'block'\n")
A("intermediate", "functions", "zscore_list", "Population z-score",
  "A zero standard deviation returns zeros.",
  "zscore_list", "values: list[float]",
  "if not values:\n    return []\nmean = sum(values) / len(values)\nvar = sum((v - mean) ** 2 for v in values) / len(values)\nif var == 0:\n    return [0.0 for _ in values]\nstd = var ** 0.5\nreturn [(v - mean) / std for v in values]",
  "from solution import zscore_list\n\ndef test_z():\n    assert zscore_list([5.0, 5.0]) == [0.0, 0.0]\n")
A("intermediate", "functions", "prior_mean_list", "Prior mean",
  "The first position is None.",
  "prior_mean_list", "values: list[float]",
  "out = []\ntotal = 0.0\nfor i, value in enumerate(values):\n    out.append(None if i == 0 else total / i)\n    total += value\nreturn out",
  "from solution import prior_mean_list\n\ndef test_prior():\n    assert prior_mean_list([10.0, 30.0, 50.0]) == [None, 10.0, 20.0]\n")
A("intermediate", "functions", "velocity_count", "Events inside a window",
  "timestamps are sorted seconds. Include the current event.",
  "velocity_count", "timestamps: list[int], window: int",
  "counts = []\nleft = 0\nfor i, stamp in enumerate(timestamps):\n    while timestamps[left] < stamp - window:\n        left += 1\n    counts.append(i - left + 1)\nreturn counts",
  "from solution import velocity_count\n\ndef test_velocity():\n    assert velocity_count([0, 10, 50], 20) == [1, 2, 1]\n")
A("intermediate", "functions", "month_over_month", "Month-over-month change",
  "Return None when the previous value is missing or zero.",
  "month_over_month", "previous: float | None, current: float",
  "if previous is None or previous == 0:\n    return None\nreturn (current - previous) / previous",
  "from solution import month_over_month\n\ndef test_mom():\n    assert month_over_month(100.0, 150.0) == 0.5\n    assert month_over_month(None, 10.0) is None\n")
A("intermediate", "functions", "flag_increase", "Flag a volume jump",
  "True when current > previous * (1 + threshold) and previous > 0.",
  "flag_increase", "previous: float, current: float, threshold: float = 0.5",
  "return previous > 0 and current > previous * (1 + threshold)",
  "from solution import flag_increase\n\ndef test_flag():\n    assert flag_increase(100, 160, 0.5) is True\n    assert flag_increase(100, 140, 0.5) is False\n")
A("intermediate", "functions", "group_sum", "Group and sum",
  "rows are (customer_id, amount).",
  "group_sum", "rows: list[tuple[int, float]]",
  "totals = {}\nfor customer_id, amount in rows:\n    totals[customer_id] = totals.get(customer_id, 0.0) + amount\nreturn totals",
  "from solution import group_sum\n\ndef test_group():\n    assert group_sum([(1, 2.0), (2, 3.0), (1, 4.0)]) == {1: 6.0, 2: 3.0}\n")
A("intermediate", "functions", "rolling_mean_py", "Rolling mean",
  "None until the window is full.",
  "rolling_mean_py", "values: list[float], k: int",
  "if k <= 0:\n    raise ValueError('k')\nout = []\nfor i in range(len(values)):\n    if i + 1 < k:\n        out.append(None)\n    else:\n        window = values[i + 1 - k:i + 1]\n        out.append(sum(window) / k)\nreturn out",
  "from solution import rolling_mean_py\n\ndef test_roll():\n    assert rolling_mean_py([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]\n")
A("intermediate", "functions", "dedupe_rows", "Drop duplicate transaction dicts",
  "Keep the first dict for each transaction_id.",
  "dedupe_rows", "rows: list[dict]",
  "seen = set()\nout = []\nfor row in rows:\n    key = row['transaction_id']\n    if key in seen:\n        continue\n    seen.add(key)\n    out.append(row)\nreturn out",
  "from solution import dedupe_rows\n\ndef test_rows():\n    rows = [{'transaction_id': 1, 'amount': 5}, {'transaction_id': 1, 'amount': 9}]\n    assert dedupe_rows(rows) == [{'transaction_id': 1, 'amount': 5}]\n")
A("intermediate", "functions", "fraud_rule", "Transparent fraud rule",
  "Flag a large z-score, a velocity burst, or a new device in a new country.",
  "fraud_rule", "amount_z: float, count_1h: int, geo_mismatch: int, new_device: int",
  "return amount_z >= 3 or count_1h >= 5 or (geo_mismatch == 1 and new_device == 1)",
  "from solution import fraud_rule\n\ndef test_rule():\n    assert fraud_rule(3.2, 1, 0, 0) is True\n    assert fraud_rule(0.1, 1, 1, 0) is False\n    assert fraud_rule(0.1, 1, 1, 1) is True\n")
A("intermediate", "functions", "log1p_amount", "Log1p of a clipped amount",
  "Clip negatives to zero before log1p.",
  "log1p_amount", "amount: float",
  "import math\nreturn math.log1p(max(amount, 0.0))",
  "from solution import log1p_amount\n\ndef test_log():\n    assert log1p_amount(0) == 0.0\n    assert log1p_amount(-5) == 0.0\n")
A("intermediate", "functions", "night_flag", "Night flag",
  "Hours 0 through 5 are night.",
  "night_flag", "hour: int",
  "if hour < 0 or hour > 23:\n    raise ValueError('hour')\nreturn int(hour <= 5)",
  "from solution import night_flag\n\ndef test_night():\n    assert night_flag(2) == 1\n    assert night_flag(14) == 0\n")
A("intermediate", "functions", "geo_mismatch_flag", "Country mismatch",
  "Return 1 when both countries are present and different.",
  "geo_mismatch_flag", "home: str | None, country: str | None",
  "if not home or not country:\n    return 0\nreturn int(home != country)",
  "from solution import geo_mismatch_flag\n\ndef test_geo():\n    assert geo_mismatch_flag('US', 'BR') == 1\n    assert geo_mismatch_flag(None, 'US') == 0\n")
A("intermediate", "functions", "high_risk_mcc", "High-risk category",
  "Gambling, crypto, wire, and luxury are high risk in this lab.",
  "high_risk_mcc", "category: str",
  "return int(category in {'gambling', 'crypto', 'wire', 'luxury'})",
  "from solution import high_risk_mcc\n\ndef test_mcc():\n    assert high_risk_mcc('crypto') == 1\n    assert high_risk_mcc('grocery') == 0\n")
A("intermediate", "functions", "simple_clv_identity", "Historical CLV",
  "AOV times purchase rate times margin times lifespan.",
  "simple_clv_identity", "aov: float, purchases: float, margin: float, lifespan: float",
  "if min(purchases, margin, lifespan) < 0:\n    raise ValueError('negative')\nreturn aov * purchases * margin * lifespan",
  "from solution import simple_clv_identity\n\ndef test_clv():\n    assert simple_clv_identity(50, 4, 0.2, 3) == 120\n")
A("intermediate", "functions", "one_log_return", "One log return",
  "log(price_now / price_prev). Prices must be positive.",
  "one_log_return", "price_prev: float, price_now: float",
  "import math\nif price_prev <= 0 or price_now <= 0:\n    raise ValueError('price')\nreturn math.log(price_now / price_prev)",
  "import math\nfrom solution import one_log_return\n\ndef test_ret():\n    assert abs(one_log_return(100, 110) - math.log(1.1)) < 1e-12\n")
A("intermediate", "functions", "causal_split_ok", "Causal split check",
  "True when the training end index is at or before the test start.",
  "causal_split_ok", "train_end: int, test_start: int",
  "return train_end <= test_start",
  "from solution import causal_split_ok\n\ndef test_causal():\n    assert causal_split_ok(10, 10) is True\n    assert causal_split_ok(11, 10) is False\n")
A("intermediate", "functions", "net_return", "Return after transaction cost",
  "Subtract turnover * bps / 10000 from the gross return.",
  "net_return", "gross: float, turnover: float, cost_bps: float",
  "return gross - turnover * cost_bps / 10000.0",
  "from solution import net_return\n\ndef test_net():\n    assert abs(net_return(0.02, 1.0, 10) - 0.019) < 1e-12\n")
A("intermediate", "functions", "slippage_price", "Slippage-adjusted price",
  "Buys fill higher and sells fill lower.",
  "slippage_price", "price: float, side: str, slippage_bps: float",
  "bump = slippage_bps / 10000.0\nif side == 'buy':\n    return price * (1 + bump)\nif side == 'sell':\n    return price * (1 - bump)\nraise ValueError(side)",
  "from solution import slippage_price\n\ndef test_slip():\n    assert slippage_price(100, 'buy', 10) == 100.1\n    assert abs(slippage_price(100, 'sell', 10) - 99.9) < 1e-9\n")
A("intermediate", "files", "csv_amount_sum", "Sum a CSV amount column",
  "Header includes amount. Sum the column. Ignore blank lines.",
  "csv_amount_sum", "text: str",
  "lines = [line for line in text.splitlines() if line.strip()]\nheader = lines[0].split(',')\nidx = header.index('amount')\nreturn sum(float(line.split(',')[idx]) for line in lines[1:])",
  "from solution import csv_amount_sum\n\ndef test_csv():\n    assert csv_amount_sum('id,amount\\n1,2.5\\n2,3\\n') == 5.5\n")
A("intermediate", "files", "missing_columns", "Missing required columns",
  "Return sorted names that are required but absent.",
  "missing_columns", "header: list[str], required: list[str]",
  "have = set(header)\nreturn sorted(name for name in required if name not in have)",
  "from solution import missing_columns\n\ndef test_missing():\n    assert missing_columns(['amount'], ['amount', 'country']) == ['country']\n")
A("intermediate", "api", "score_payload", "Stable JSON payload",
  "Dump features as JSON with sorted keys.",
  "score_payload", "features: dict[str, float]",
  "import json\nreturn json.dumps(features, sort_keys=True)",
  "from solution import score_payload\n\ndef test_payload():\n    assert score_payload({'b': 1, 'a': 2}) == '{\"a\": 2, \"b\": 1}'\n")
A("intermediate", "api", "parse_decision_response", "Read a decision",
  "Return the decision field from a JSON object.",
  "parse_decision_response", "payload: str",
  "import json\nreturn str(json.loads(payload)['decision'])",
  "from solution import parse_decision_response\n\ndef test_response():\n    assert parse_decision_response('{\"decision\": \"review\"}') == 'review'\n")
A("intermediate", "performance", "vector_dot", "Dot product",
  "Dot product of two equal-length lists.",
  "vector_dot", "left: list[float], right: list[float]",
  "if len(left) != len(right):\n    raise ValueError('length')\nreturn sum(a * b for a, b in zip(left, right))",
  "from solution import vector_dot\n\ndef test_dot():\n    assert vector_dot([1, 2, 3], [4, 5, 6]) == 32\n")
A("intermediate", "performance", "online_mean_var", "Welford mean and variance",
  "Return (mean, population variance) in one pass.",
  "online_mean_var", "values: list[float]",
  "if not values:\n    raise ValueError('empty')\nmean = 0.0\nm2 = 0.0\nfor i, value in enumerate(values, start=1):\n    delta = value - mean\n    mean += delta / i\n    m2 += delta * (value - mean)\nreturn mean, m2 / len(values)",
  "from solution import online_mean_var\n\ndef test_welford():\n    mean, var = online_mean_var([1.0, 2.0, 3.0])\n    assert mean == 2.0\n    assert abs(var - (2 / 3)) < 1e-12\n")
