# Assignment 5: Quicksort Implementation, Analysis, and Randomization

Deterministic and randomized Quicksort in Python, with tests and a
benchmark. Both versions sort in place with the Lomuto partition scheme.

## Files
- `quicksort.py`: `quicksort` (last element as pivot) and `randomized_quicksort` (random pivot)
- `tests/test_quicksort.py`: unit tests
- `benchmark.py`: timing, comparison counts, and recursion depth
- `results.csv`, `results.png`: benchmark output
- `report.md`: full report

## How to run
```
py -m unittest discover -s tests -v
py benchmark.py
```

## Summary of findings
- On random input both versions grow like n log n. The deterministic version is slightly faster because the randomized version pays for a random number call at every partition.
- On sorted and reverse sorted input, the deterministic version is quadratic. At n = 8000 it needs 31,996,000 comparisons and a recursion depth of 7999. The randomized version needs about 119,000 comparisons and a depth near 30.
- Randomization does not help when all elements are equal. Both versions are quadratic, because the partition puts every element on one side.
