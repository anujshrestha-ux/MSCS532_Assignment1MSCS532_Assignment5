"""Unit tests for deterministic and randomized Quicksort."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from quicksort import Stats, quicksort, randomized_quicksort

SORTS = [("deterministic", quicksort),
         ("randomized", lambda a: randomized_quicksort(a, seed=1))]


class QuicksortTests(unittest.TestCase):
    def check(self, data):
        for name, sort in SORTS:
            with self.subTest(sort=name, data=data[:10]):
                self.assertEqual(sort(data[:]), sorted(data))

    def test_empty_and_single(self):
        self.check([])
        self.check([7])

    def test_two_elements(self):
        self.check([2, 1])
        self.check([1, 2])

    def test_sorted_reverse_and_equal(self):
        self.check(list(range(200)))
        self.check(list(range(200, 0, -1)))
        self.check([5] * 100)

    def test_duplicates_and_negatives(self):
        self.check([3, -1, 3, 0, -1, 2, 2, 3])

    def test_random_inputs(self):
        rng = random.Random(0)
        for _ in range(50):
            n = rng.randint(0, 300)
            self.check([rng.randint(-50, 50) for _ in range(n)])

    def test_sorts_in_place_and_returns_same_list(self):
        for _, sort in SORTS:
            data = [3, 1, 2]
            self.assertIs(sort(data), data)
            self.assertEqual(data, [1, 2, 3])

    def test_randomized_is_repeatable_with_seed(self):
        data = list(range(300))
        random.Random(5).shuffle(data)
        a, b = Stats(), Stats()
        randomized_quicksort(data[:], a, seed=42)
        randomized_quicksort(data[:], b, seed=42)
        self.assertEqual(a.comparisons, b.comparisons)

    def test_worst_case_depth_for_deterministic(self):
        s = Stats()
        quicksort(list(range(500)), s)
        self.assertEqual(s.max_depth, 499)           # n - 1 partition levels
        self.assertEqual(s.comparisons, 500 * 499 // 2)  # n(n-1)/2

    def test_randomization_avoids_sorted_worst_case(self):
        s = Stats()
        randomized_quicksort(list(range(500)), s, seed=3)
        self.assertLess(s.comparisons, 500 * 499 // 4)
        self.assertLess(s.max_depth, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)
