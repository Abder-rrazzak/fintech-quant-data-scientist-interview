from __future__ import annotations

def count_categories(categories: list[str]):
    """Count merchant categories."""
    counts = {}
    for category in categories:
        counts[category] = counts.get(category, 0) + 1
    return counts
