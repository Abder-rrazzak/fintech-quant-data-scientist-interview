from __future__ import annotations

def most_frequent_category(categories: list[str]):
    """Most frequent category."""
    if not categories:
        raise ValueError('empty')
    counts = {}
    for category in categories:
        counts[category] = counts.get(category, 0) + 1
    return sorted(counts, key=lambda key: (-counts[key], key))[0]
