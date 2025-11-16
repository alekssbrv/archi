from __future__ import annotations


def percentile(values: list[float], perc: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = (len(sorted_values) - 1) * perc / 100.0

    lower_index = int(index)
    upper_index = lower_index + 1
    if upper_index >= len(sorted_values):
        return sorted_values[lower_index]

    return sorted_values[lower_index] * (1 - index + lower_index) + sorted_values[upper_index] * (index - lower_index)
