"""Utilities for merging, subtracting, and intersecting sets of half-open intervals."""

from .core import (
    Interval,
    normalize,
    merge,
    subtract,
    intersect,
    total_length,
)

__all__ = [
    "Interval",
    "normalize",
    "merge",
    "subtract",
    "intersect",
    "total_length",
]
