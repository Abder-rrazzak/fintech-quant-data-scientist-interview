"""Beginner Python exercises for the interview laboratory."""

from __future__ import annotations

RAW: list[tuple] = []


def A(*row: object) -> None:
    RAW.append(row)


A("beginner", "lists", "sum_amounts", "Sum transaction amounts",
  "Sum a list of transaction amounts. An empty list sums to 0.",
  "sum_amounts", "amounts: list[float]", "return float(sum(amounts))",
  "from solution import sum_amounts\n\ndef test_sum():\n    assert sum_amounts([10.0, 2.5, 0.5]) == 13.0\n    assert sum_amounts([]) == 0.0\n")
A("beginner", "lists", "max_amount", "Largest amount",
  "Return the largest amount. Raise ValueError on an empty list.",
  "max_amount", "amounts: list[float]",
  "if not amounts:\n    raise ValueError('empty')\nreturn max(amounts)",
  "from solution import max_amount\n\ndef test_max():\n    assert max_amount([3.0, 9.0, 4.0]) == 9.0\n    try:\n        max_amount([])\n        raise AssertionError('expected')\n    except ValueError:\n        pass\n")
A("beginner", "lists", "count_above", "Count amounts above a threshold",
  "Count how many amounts are strictly greater than the threshold.",
  "count_above", "amounts: list[float], threshold: float",
  "return sum(amount > threshold for amount in amounts)",
  "from solution import count_above\n\ndef test_count():\n    assert count_above([10, 50, 51, 7], 50) == 1\n    assert count_above([], 1) == 0\n")
A("beginner", "lists", "clip_amounts", "Clip amounts into a range",
  "Clamp each amount to the inclusive range [low, high].",
  "clip_amounts", "amounts: list[float], low: float, high: float",
  "return [min(max(amount, low), high) for amount in amounts]",
  "from solution import clip_amounts\n\ndef test_clip():\n    assert clip_amounts([-5, 10, 80], 0, 50) == [0, 10, 50]\n")
A("beginner", "lists", "running_balance", "Running balance",
  "Apply signed amounts in order, starting from opening.",
  "running_balance", "opening: float, amounts: list[float]",
  "balance = opening\nout = []\nfor amount in amounts:\n    balance += amount\n    out.append(balance)\nreturn out",
  "from solution import running_balance\n\ndef test_balance():\n    assert running_balance(100.0, [-20.0, 5.0]) == [80.0, 85.0]\n    assert running_balance(10.0, []) == []\n")
A("beginner", "lists", "pairwise_diffs", "Consecutive amount changes",
  "Return amount[i] - amount[i-1] for each position after the first.",
  "pairwise_diffs", "amounts: list[float]",
  "return [amounts[i] - amounts[i - 1] for i in range(1, len(amounts))]",
  "from solution import pairwise_diffs\n\ndef test_diffs():\n    assert pairwise_diffs([10, 12, 9]) == [2, -3]\n    assert pairwise_diffs([4]) == []\n")
A("beginner", "lists", "top_k_amounts", "Top k amounts",
  "Return the k largest amounts, sorted descending.",
  "top_k_amounts", "amounts: list[float], k: int",
  "if k < 0:\n    raise ValueError('k')\nreturn sorted(amounts, reverse=True)[:k]",
  "from solution import top_k_amounts\n\ndef test_top():\n    assert top_k_amounts([4, 1, 9, 3], 2) == [9, 4]\n    assert top_k_amounts([1], 5) == [1]\n")
A("beginner", "lists", "chunk_batches", "Chunk a list",
  "Split items into contiguous batches of the given size. The last batch may be short.",
  "chunk_batches", "items: list[int], size: int",
  "if size <= 0:\n    raise ValueError('size')\nreturn [items[i:i + size] for i in range(0, len(items), size)]",
  "from solution import chunk_batches\n\ndef test_chunk():\n    assert chunk_batches([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]\n")
A("beginner", "lists", "flatten_batches", "Flatten batches",
  "Flatten a list of batches into one list, preserving order.",
  "flatten_batches", "batches: list[list[int]]",
  "return [item for batch in batches for item in batch]",
  "from solution import flatten_batches\n\ndef test_flat():\n    assert flatten_batches([[1, 2], [], [3]]) == [1, 2, 3]\n")
A("beginner", "lists", "dedupe_preserve_order", "Drop duplicate ids",
  "Remove duplicate ids and keep the first occurrence.",
  "dedupe_preserve_order", "ids: list[int]",
  "seen = set()\nout = []\nfor item in ids:\n    if item not in seen:\n        seen.add(item)\n        out.append(item)\nreturn out",
  "from solution import dedupe_preserve_order\n\ndef test_dedupe():\n    assert dedupe_preserve_order([3, 1, 3, 2, 1]) == [3, 1, 2]\n")
A("beginner", "lists", "second_largest", "Second largest distinct amount",
  "Return the second largest distinct amount, or None if it does not exist.",
  "second_largest", "amounts: list[float]",
  "unique = sorted(set(amounts), reverse=True)\nreturn unique[1] if len(unique) > 1 else None",
  "from solution import second_largest\n\ndef test_second():\n    assert second_largest([5, 5, 3, 9]) == 5\n    assert second_largest([4, 4]) is None\n")
A("beginner", "lists", "cumulative_sum", "Cumulative sum",
  "Return the cumulative sum of amounts.",
  "cumulative_sum", "amounts: list[float]",
  "total = 0.0\nout = []\nfor amount in amounts:\n    total += amount\n    out.append(total)\nreturn out",
  "from solution import cumulative_sum\n\ndef test_csum():\n    assert cumulative_sum([1.0, 2.0, 3.0]) == [1.0, 3.0, 6.0]\n")
A("beginner", "lists", "moving_sum", "Moving sum",
  "Return the sum of each contiguous window of length k.",
  "moving_sum", "amounts: list[float], k: int",
  "if k <= 0:\n    raise ValueError('k')\nif k > len(amounts):\n    return []\nwindow = sum(amounts[:k])\nout = [window]\nfor i in range(k, len(amounts)):\n    window += amounts[i] - amounts[i - k]\n    out.append(window)\nreturn out",
  "from solution import moving_sum\n\ndef test_moving():\n    assert moving_sum([1, 2, 3, 4], 2) == [3, 5, 7]\n    assert moving_sum([1, 2], 5) == []\n")
A("beginner", "lists", "count_negatives", "Count negative amounts",
  "Count amounts that are strictly negative.",
  "count_negatives", "amounts: list[float]",
  "return sum(amount < 0 for amount in amounts)",
  "from solution import count_negatives\n\ndef test_neg():\n    assert count_negatives([1, -2, 0, -3]) == 2\n")
A("beginner", "lists", "first_index_above", "First index above a limit",
  "Return the first index whose amount exceeds the limit, or -1.",
  "first_index_above", "amounts: list[float], limit: float",
  "for i, amount in enumerate(amounts):\n    if amount > limit:\n        return i\nreturn -1",
  "from solution import first_index_above\n\ndef test_idx():\n    assert first_index_above([1, 4, 9], 5) == 2\n    assert first_index_above([1, 2], 5) == -1\n")
A("beginner", "dictionaries", "count_categories", "Count merchant categories",
  "Return a dictionary of category to count.",
  "count_categories", "categories: list[str]",
  "counts = {}\nfor category in categories:\n    counts[category] = counts.get(category, 0) + 1\nreturn counts",
  "from solution import count_categories\n\ndef test_counts():\n    assert count_categories(['grocery', 'grocery', 'fuel']) == {'grocery': 2, 'fuel': 1}\n")
A("beginner", "dictionaries", "merge_amount_dicts", "Merge amount maps",
  "Add values that share a key. Keys that appear in only one map are kept.",
  "merge_amount_dicts", "left: dict[str, float], right: dict[str, float]",
  "out = dict(left)\nfor key, value in right.items():\n    out[key] = out.get(key, 0.0) + value\nreturn out",
  "from solution import merge_amount_dicts\n\ndef test_merge():\n    assert merge_amount_dicts({'a': 1.0}, {'a': 2.0, 'b': 3.0}) == {'a': 3.0, 'b': 3.0}\n")
A("beginner", "dictionaries", "customer_totals", "Totals from pairs",
  "Given (customer_id, amount) pairs, return a dict of totals.",
  "customer_totals", "pairs: list[tuple[int, float]]",
  "totals = {}\nfor customer_id, amount in pairs:\n    totals[customer_id] = totals.get(customer_id, 0.0) + amount\nreturn totals",
  "from solution import customer_totals\n\ndef test_totals():\n    assert customer_totals([(1, 10.0), (1, 2.5), (2, 4.0)]) == {1: 12.5, 2: 4.0}\n")
A("beginner", "dictionaries", "filter_large", "Keep large totals",
  "Keep dictionary entries whose value is strictly greater than the cutoff.",
  "filter_large", "totals: dict[int, float], cutoff: float",
  "return {key: value for key, value in totals.items() if value > cutoff}",
  "from solution import filter_large\n\ndef test_filter():\n    assert filter_large({1: 10.0, 2: 3.0}, 5) == {1: 10.0}\n")
A("beginner", "dictionaries", "most_frequent_category", "Most frequent category",
  "Return the category with the highest count. Ties break toward the alphabetically first category.",
  "most_frequent_category", "categories: list[str]",
  "if not categories:\n    raise ValueError('empty')\ncounts = {}\nfor category in categories:\n    counts[category] = counts.get(category, 0) + 1\nreturn sorted(counts, key=lambda key: (-counts[key], key))[0]",
  "from solution import most_frequent_category\n\ndef test_mode():\n    assert most_frequent_category(['fuel', 'grocery', 'fuel']) == 'fuel'\n    assert most_frequent_category(['b', 'a']) == 'a'\n")
A("beginner", "dictionaries", "invert_unique", "Invert a unique map",
  "Invert a dict whose values are unique. Raise ValueError if a value repeats.",
  "invert_unique", "mapping: dict[str, str]",
  "out = {}\nfor key, value in mapping.items():\n    if value in out:\n        raise ValueError(value)\n    out[value] = key\nreturn out",
  "from solution import invert_unique\n\ndef test_invert():\n    assert invert_unique({'usd': 'US'}) == {'US': 'usd'}\n    try:\n        invert_unique({'a': 'x', 'b': 'x'})\n        raise AssertionError('expected')\n    except ValueError:\n        pass\n")
A("beginner", "dictionaries", "get_nested", "Read a nested field",
  "Read mapping[outer][inner]. Return the default if either key is missing.",
  "get_nested", "mapping: dict, outer: str, inner: str, default: float",
  "inner_map = mapping.get(outer)\nif not isinstance(inner_map, dict) or inner not in inner_map:\n    return default\nreturn inner_map[inner]",
  "from solution import get_nested\n\ndef test_nested():\n    assert get_nested({'cust': {'limit': 20.0}}, 'cust', 'limit', 0.0) == 20.0\n    assert get_nested({}, 'cust', 'limit', 0.0) == 0.0\n")
A("beginner", "dictionaries", "two_sum_ids", "Two amounts that settle a target",
  "Return the indexes of the first pair that sums to target, or None.",
  "two_sum_ids", "amounts: list[float], target: float",
  "seen = {}\nfor index, amount in enumerate(amounts):\n    need = target - amount\n    if need in seen:\n        return [seen[need], index]\n    seen[amount] = index\nreturn None",
  "from solution import two_sum_ids\n\ndef test_two_sum():\n    assert two_sum_ids([2.0, 7.0, 11.0, 15.0], 18.0) == [1, 2]\n    assert two_sum_ids([1.0, 2.0], 10.0) is None\n")
A("beginner", "sets", "shared_customers", "Customers in both months",
  "Return the sorted ids that appear in both collections.",
  "shared_customers", "left: list[int], right: list[int]",
  "return sorted(set(left) & set(right))",
  "from solution import shared_customers\n\ndef test_shared():\n    assert shared_customers([1, 2, 2], [2, 3]) == [2]\n")
A("beginner", "sets", "new_customers", "Customers who appeared later",
  "Return sorted ids that are in the current period but not the prior period.",
  "new_customers", "prior: list[int], current: list[int]",
  "return sorted(set(current) - set(prior))",
  "from solution import new_customers\n\ndef test_new():\n    assert new_customers([1, 2], [2, 3, 4]) == [3, 4]\n")
A("beginner", "sets", "all_customers", "Union of customer ids",
  "Return the sorted union of the two id lists.",
  "all_customers", "left: list[int], right: list[int]",
  "return sorted(set(left) | set(right))",
  "from solution import all_customers\n\ndef test_union():\n    assert all_customers([1, 2], [2, 3]) == [1, 2, 3]\n")
A("beginner", "sets", "is_known_merchant", "Known merchant set",
  "Return True when every merchant id is already in the approved set.",
  "is_known_merchant", "approved: set[int], seen: list[int]",
  "return set(seen).issubset(approved)",
  "from solution import is_known_merchant\n\ndef test_known():\n    assert is_known_merchant({1, 2}, [1, 1]) is True\n    assert is_known_merchant({1}, [2]) is False\n")
A("beginner", "sets", "dropped_categories", "Categories that disappeared",
  "Return sorted categories present in the baseline but not in the current list.",
  "dropped_categories", "baseline: list[str], current: list[str]",
  "return sorted(set(baseline) - set(current))",
  "from solution import dropped_categories\n\ndef test_dropped():\n    assert dropped_categories(['atm', 'fuel'], ['fuel']) == ['atm']\n")
A("beginner", "tuples", "minmax_amount", "Min and max as a tuple",
  "Return (min, max). Raise ValueError on an empty list.",
  "minmax_amount", "amounts: list[float]",
  "if not amounts:\n    raise ValueError('empty')\nreturn (min(amounts), max(amounts))",
  "from solution import minmax_amount\n\ndef test_minmax():\n    assert minmax_amount([3.0, 1.0, 8.0]) == (1.0, 8.0)\n")
A("beginner", "tuples", "unpack_record", "Unpack a transaction triple",
  "A record is (customer_id, amount, country). Return a dict with those keys.",
  "unpack_record", "record: tuple[int, float, str]",
  "customer_id, amount, country = record\nreturn {'customer_id': customer_id, 'amount': amount, 'country': country}",
  "from solution import unpack_record\n\ndef test_unpack():\n    assert unpack_record((7, 12.5, 'US')) == {'customer_id': 7, 'amount': 12.5, 'country': 'US'}\n")
A("beginner", "strings", "parse_money", "Parse a money string",
  "Parse strings like '$1,200.50' or '1200.50' into a float.",
  "parse_money", "text: str",
  "cleaned = text.strip().replace('$', '').replace(',', '')\nif not cleaned:\n    raise ValueError('empty')\nreturn float(cleaned)",
  "from solution import parse_money\n\ndef test_money():\n    assert parse_money('$1,200.50') == 1200.50\n    assert parse_money('15') == 15.0\n")
A("beginner", "strings", "mask_pan", "Mask a card number",
  "Keep the last 4 characters and replace the rest with asterisks. Shorter inputs are returned unchanged.",
  "mask_pan", "pan: str",
  "if len(pan) <= 4:\n    return pan\nreturn '*' * (len(pan) - 4) + pan[-4:]",
  "from solution import mask_pan\n\ndef test_mask():\n    assert mask_pan('4111111111111111') == '************1111'\n    assert mask_pan('1234') == '1234'\n")
A("beginner", "strings", "normalize_merchant", "Normalize a merchant name",
  "Lowercase, strip, and collapse internal whitespace to a single space.",
  "normalize_merchant", "name: str",
  "return ' '.join(name.strip().lower().split())",
  "from solution import normalize_merchant\n\ndef test_norm():\n    assert normalize_merchant('  ACME   Store ') == 'acme store'\n")
A("beginner", "strings", "valid_currency", "Validate a currency code",
  "Return True only for USD, EUR, or GBP.",
  "valid_currency", "code: str",
  "return code in {'USD', 'EUR', 'GBP'}",
  "from solution import valid_currency\n\ndef test_ccy():\n    assert valid_currency('USD') is True\n    assert valid_currency('JPY') is False\n")
A("beginner", "strings", "iso_month", "Month key from an ISO timestamp",
  "Given '2024-03-15T10:00:00', return '2024-03'.",
  "iso_month", "timestamp: str",
  "if len(timestamp) < 7:\n    raise ValueError('timestamp')\nreturn timestamp[:7]",
  "from solution import iso_month\n\ndef test_month():\n    assert iso_month('2024-03-15T10:00:00') == '2024-03'\n")
A("beginner", "strings", "last4", "Last four characters",
  "Return the last four characters. Raise ValueError if the string is shorter.",
  "last4", "value: str",
  "if len(value) < 4:\n    raise ValueError('short')\nreturn value[-4:]",
  "from solution import last4\n\ndef test_last4():\n    assert last4('dev_1234') == '1234'\n")
A("beginner", "comprehensions", "positive_amounts", "Keep positive amounts",
  "Return amounts that are strictly positive, preserving order.",
  "positive_amounts", "amounts: list[float]",
  "return [amount for amount in amounts if amount > 0]",
  "from solution import positive_amounts\n\ndef test_pos():\n    assert positive_amounts([-1, 0, 2, 3]) == [2, 3]\n")
A("beginner", "comprehensions", "amount_lookup", "Map ids to amounts",
  "Build a dict from parallel id and amount lists. Later ids overwrite earlier ones.",
  "amount_lookup", "ids: list[int], amounts: list[float]",
  "if len(ids) != len(amounts):\n    raise ValueError('length')\nreturn {ids[i]: amounts[i] for i in range(len(ids))}",
  "from solution import amount_lookup\n\ndef test_lookup():\n    assert amount_lookup([1, 1], [5.0, 7.0]) == {1: 7.0}\n")
A("beginner", "comprehensions", "fraud_ids", "Ids with a fraud flag",
  "Return ids whose flag is 1.",
  "fraud_ids", "ids: list[int], flags: list[int]",
  "return [ids[i] for i in range(len(ids)) if flags[i] == 1]",
  "from solution import fraud_ids\n\ndef test_fraud_ids():\n    assert fraud_ids([10, 11, 12], [0, 1, 0]) == [11]\n")
A("beginner", "comprehensions", "squared_log_amounts", "Square log1p amounts",
  "Return (log1p(amount))**2 for each non-negative amount using the math library.",
  "squared_log_amounts", "amounts: list[float]",
  "import math\nreturn [math.log1p(amount) ** 2 for amount in amounts]",
  "import math\nfrom solution import squared_log_amounts\n\ndef test_sq():\n    assert squared_log_amounts([0.0]) == [0.0]\n    assert squared_log_amounts([math.e - 1]) == [1.0]\n")
A("beginner", "functions", "safe_divide", "Divide without crashing on zero",
  "Return numerator / denominator, or the default when the denominator is 0.",
  "safe_divide", "numerator: float, denominator: float, default: float = 0.0",
  "if denominator == 0:\n    return default\nreturn numerator / denominator",
  "from solution import safe_divide\n\ndef test_div():\n    assert safe_divide(10, 4) == 2.5\n    assert safe_divide(10, 0) == 0.0\n    assert safe_divide(10, 0, default=-1) == -1\n")
A("beginner", "functions", "weighted_mean", "Weighted mean",
  "Return the weighted mean. Raise ValueError if the weights do not match or sum to 0.",
  "weighted_mean", "values: list[float], weights: list[float]",
  "if len(values) != len(weights) or not values:\n    raise ValueError('shape')\ntotal_w = sum(weights)\nif total_w == 0:\n    raise ValueError('weights')\nreturn sum(v * w for v, w in zip(values, weights)) / total_w",
  "from solution import weighted_mean\n\ndef test_wmean():\n    assert weighted_mean([10.0, 20.0], [1.0, 1.0]) == 15.0\n    assert weighted_mean([10.0, 20.0], [3.0, 1.0]) == 12.5\n")
A("beginner", "functions", "clamp_score", "Clamp a score to [0, 1]",
  "Clamp a model score into the unit interval.",
  "clamp_score", "score: float",
  "return min(max(score, 0.0), 1.0)",
  "from solution import clamp_score\n\ndef test_clamp():\n    assert clamp_score(1.4) == 1.0\n    assert clamp_score(-0.2) == 0.0\n    assert clamp_score(0.3) == 0.3\n")
A("beginner", "functions", "make_fee", "Closure that adds a fixed fee",
  "Return a function that adds fee to its argument.",
  "make_fee", "fee: float",
  "def add_fee(amount: float) -> float:\n    return amount + fee\nreturn add_fee",
  "from solution import make_fee\n\ndef test_fee():\n    add = make_fee(1.5)\n    assert add(10) == 11.5\n")
A("beginner", "functions", "apply_ledger", "Apply deposit and withdraw operations",
  "operations are ('deposit', amount) or ('withdraw', amount). Withdrawals that exceed the balance raise ValueError.",
  "apply_ledger", "opening: float, operations: list[tuple[str, float]]",
  "balance = opening\nfor op, amount in operations:\n    if amount < 0:\n        raise ValueError('amount')\n    if op == 'deposit':\n        balance += amount\n    elif op == 'withdraw':\n        if amount > balance:\n            raise ValueError('insufficient')\n        balance -= amount\n    else:\n        raise ValueError(op)\nreturn balance",
  "from solution import apply_ledger\n\ndef test_ledger():\n    assert apply_ledger(100, [('withdraw', 40), ('deposit', 10)]) == 70\n    try:\n        apply_ledger(5, [('withdraw', 6)])\n        raise AssertionError('expected')\n    except ValueError:\n        pass\n")
A("beginner", "exceptions", "require_currency", "Reject unknown currencies",
  "Return the code if it is USD, EUR, or GBP. Otherwise raise ValueError.",
  "require_currency", "code: str",
  "if code not in {'USD', 'EUR', 'GBP'}:\n    raise ValueError(code)\nreturn code",
  "from solution import require_currency\n\ndef test_require():\n    assert require_currency('EUR') == 'EUR'\n    try:\n        require_currency('JPY')\n        raise AssertionError('expected')\n    except ValueError:\n        pass\n")
A("beginner", "json", "total_from_json", "Sum amounts in a JSON list",
  "payload is a JSON list of objects with an amount field. Return the sum.",
  "total_from_json", "payload: str",
  "import json\nrows = json.loads(payload)\nreturn float(sum(float(row['amount']) for row in rows))",
  "from solution import total_from_json\n\ndef test_json():\n    assert total_from_json('[{\"amount\": 2}, {\"amount\": 3.5}]') == 5.5\n")
A("beginner", "json", "fraud_ratio_json", "Fraud ratio from JSON",
  "payload is a JSON list of objects with is_fraud 0 or 1. Return the mean, or 0 for an empty list.",
  "fraud_ratio_json", "payload: str",
  "import json\nrows = json.loads(payload)\nif not rows:\n    return 0.0\nreturn sum(int(row['is_fraud']) for row in rows) / len(rows)",
  "from solution import fraud_ratio_json\n\ndef test_ratio():\n    assert fraud_ratio_json('[{\"is_fraud\": 1}, {\"is_fraud\": 0}]') == 0.5\n    assert fraud_ratio_json('[]') == 0.0\n")
