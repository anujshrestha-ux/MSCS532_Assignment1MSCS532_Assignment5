"""Empirical comparison of deterministic and randomized Quicksort."""
import csv
import random
import time

from quicksort import Stats, quicksort, randomized_quicksort

SIZES = [500, 1000, 2000, 4000, 8000]
KINDS = ["random", "sorted", "reverse", "equal"]


def make_data(kind, n):
    if kind == "sorted":
        return list(range(n))
    if kind == "reverse":
        return list(range(n, 0, -1))
    if kind == "equal":
        return [7] * n
    rng = random.Random(42)          # fixed seed so runs are repeatable
    return [rng.randint(0, n) for _ in range(n)]


def best_time(sort, data, repeats=3):
    """Best wall-clock time in milliseconds over several runs."""
    best = float("inf")
    for _ in range(repeats):
        copy = data[:]
        start = time.perf_counter()
        sort(copy)
        best = min(best, time.perf_counter() - start)
    return best * 1000


def main():
    algos = {
        "deterministic": quicksort,
        "randomized": lambda a, s=None: randomized_quicksort(a, s, seed=1),
    }
    rows = []
    print(f"{'data':8} {'n':>5} {'algorithm':14} {'time_ms':>10} "
          f"{'comparisons':>12} {'depth':>6}")
    for kind in KINDS:
        for n in SIZES:
            data = make_data(kind, n)
            for name, sort in algos.items():
                ms = best_time(sort, data)
                stats = Stats()
                sort(data[:], stats)
                rows.append((kind, n, name, round(ms, 2),
                             stats.comparisons, stats.max_depth))
                print(f"{kind:8} {n:5} {name:14} {ms:10.2f} "
                      f"{stats.comparisons:12} {stats.max_depth:6}")
    with open("results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "n", "algorithm", "time_ms",
                    "comparisons", "max_depth"])
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    main()
