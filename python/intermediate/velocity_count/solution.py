from __future__ import annotations

def velocity_count(timestamps: list[int], window: int):
    """Events inside a window."""
    counts = []
    left = 0
    for i, stamp in enumerate(timestamps):
        while timestamps[left] < stamp - window:
            left += 1
        counts.append(i - left + 1)
    return counts
