"""Assignment 5: deterministic and randomized Quicksort.

Both versions sort a list in place using the Lomuto partition scheme.
They differ only in how the pivot is chosen:
  - quicksort:            pivot is the last element of the subarray
  - randomized_quicksort: pivot is a random element of the subarray
"""
import random
import sys

# Deterministic Quicksort recurses n levels deep on sorted input,
# so Python's default limit of 1000 is too low for large tests.
sys.setrecursionlimit(50000)


class Stats:
    """Optional counters used by the empirical analysis."""

    def __init__(self):
        self.comparisons = 0   # element-to-pivot comparisons
        self.max_depth = 0     # deepest recursion level reached


def partition(arr, low, high, stats=None):
    """Partition arr[low..high] around the pivot arr[high].

    Returns the final index of the pivot. Everything to its left is
    <= pivot and everything to its right is > pivot.
    """
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    if stats:
        stats.comparisons += high - low
    return i + 1


def _sort(arr, low, high, randomized, rng, stats, depth):
    if low < high:
        if stats and depth > stats.max_depth:
            stats.max_depth = depth
        if randomized:
            # Move a randomly chosen element into the pivot position.
            r = rng.randint(low, high)
            arr[r], arr[high] = arr[high], arr[r]
        p = partition(arr, low, high, stats)
        _sort(arr, low, p - 1, randomized, rng, stats, depth + 1)
        _sort(arr, p + 1, high, randomized, rng, stats, depth + 1)


def quicksort(arr, stats=None):
    """Deterministic Quicksort (last element as pivot). Sorts in place."""
    _sort(arr, 0, len(arr) - 1, False, None, stats, 1)
    return arr


def randomized_quicksort(arr, stats=None, seed=None):
    """Randomized Quicksort (random pivot). Sorts in place."""
    rng = random.Random(seed)
    _sort(arr, 0, len(arr) - 1, True, rng, stats, 1)
    return arr
