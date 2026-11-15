"""Core interval operations for half-open intervals [start, end).

All intervals are represented as tuples ``(start, end)`` with ``start < end``.
Operations accept any iterable of such tuples and return a sorted list of
normalized intervals.  Empty inputs and degenerate intervals (start == end)
are handled by dropping them during normalization.
"""

from __future__ import annotations

from typing import Iterable, List, Tuple

# An interval is a half-open range [start, end).
Interval = Tuple[float, float]


def normalize(intervals: Iterable[Interval]) -> List[Interval]:
    """Return a sorted list of disjoint intervals covering the same union.

    Degenerate intervals (start >= end) are discarded.  The result is sorted
    by start and contains no overlapping or adjacent intervals.
    """
    # Filter out degenerate intervals and sort by start.
    items = sorted((s, e) for s, e in intervals if s < e)
    if not items:
        return []

    merged: List[Interval] = []
    cur_start, cur_end = items[0]
    for s, e in items[1:]:
        if s <= cur_end:
            # Overlap or touch: extend the current interval.
            if e > cur_end:
                cur_end = e
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = s, e
    merged.append((cur_start, cur_end))
    return merged


def merge(intervals: Iterable[Interval]) -> List[Interval]:
    """Merge overlapping or adjacent intervals into a normalized list.

    This is an alias for :func:`normalize` kept separate for readability.
    """
    return normalize(intervals)


def intersect(a: Iterable[Interval], b: Iterable[Interval]) -> List[Interval]:
    """Return the intersection of two sets of intervals.

    The result is a normalized list of intervals present in both inputs.
    """
    left = normalize(a)
    right = normalize(b)
    result: List[Interval] = []
    i = j = 0
    while i < len(left) and j < len(right):
        a_start, a_end = left[i]
        b_start, b_end = right[j]
        start = max(a_start, b_start)
        end = min(a_end, b_end)
        if start < end:
            result.append((start, end))
        # Advance the interval that ends first; the other may still overlap
        # with the next interval from the opposite list.
        if a_end < b_end:
            i += 1
        else:
            j += 1
    return result


def subtract(a: Iterable[Interval], b: Iterable[Interval]) -> List[Interval]:
    """Return the set difference ``a - b``.

    Every point in an interval from ``a`` that is not covered by any interval
    in ``b`` is included in the result.  The result is normalized.
    """
    left = normalize(a)
    right = normalize(b)
    result: List[Interval] = []
    j = 0
    for a_start, a_end in left:
        cur = a_start
        # Skip intervals in b that end before the current a interval starts.
        while j < len(right) and right[j][1] <= cur:
            j += 1
        k = j
        while k < len(right) and right[k][0] < a_end:
            b_start, b_end = right[k]
            if b_start > cur:
                # Gap before this b interval.
                result.append((cur, b_start))
            if b_end > cur:
                cur = b_end
            if cur >= a_end:
                break
            k += 1
        if cur < a_end:
            result.append((cur, a_end))
    return result


def total_length(intervals: Iterable[Interval]) -> float:
    """Return the total length of the union of the given intervals."""
    return sum(end - start for start, end in normalize(intervals))
