# interval_merge_utils

Merge, subtract and intersect sets of half-open intervals.

## Usage

```python
from interval_merge_utils import normalize, merge, subtract, intersect, total_length

# Normalize overlapping/adjacent intervals.
normalize([(1, 4), (2, 6), (8, 9)])   # [(1, 6), (8, 9)]

# merge is an alias for normalize.
merge([(5, 6), (1, 3), (2, 4)])       # [(1, 4), (5, 6)]

# Set difference and intersection.
subtract([(1, 10)], [(3, 5)])         # [(1, 3), (5, 10)]
intersect([(1, 5)], [(3, 7)])         # [(3, 5)]

# Total covered length of the union.
total_length([(1, 5), (3, 7)])        # 6
```

All functions accept any iterable of ``(start, end)`` tuples and return a
sorted list of disjoint, non-adjacent intervals.  Degenerate intervals where
``start >= end`` are discarded.

## Why this exists

Set operations on intervals are easy to get subtly wrong: merging adjacent
intervals, preserving half-open semantics at shared endpoints, and handling
unsorted input all require care.  This library makes one clear decision:
intervals are half-open ``[start, end)``, so ``[1, 2)`` and ``[2, 3)`` merge
into ``[1, 3)``, while their intersection is empty.  The trade-off is that
there is no closed-interval mode; users who need ``[1, 2]`` must convert
their data themselves.

## The awkward edge

Because intervals are half-open, two intervals that merely touch at a point
do not intersect.  ``intersect([(1, 2)], [(2, 3)])`` returns ``[]``, not
``[(2, 2)]``.  This is intentional and is the most common source of surprise.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

