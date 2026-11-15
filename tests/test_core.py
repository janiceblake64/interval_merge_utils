import unittest

from interval_merge_utils import (
    normalize,
    merge,
    subtract,
    intersect,
    total_length,
)


class TestNormalize(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(normalize([]), [])

    def test_single(self):
        self.assertEqual(normalize([(1, 2)]), [(1, 2)])

    def test_unsorted(self):
        self.assertEqual(normalize([(3, 4), (1, 2)]), [(1, 2), (3, 4)])

    def test_overlapping(self):
        self.assertEqual(normalize([(1, 4), (2, 5)]), [(1, 5)])

    def test_adjacent(self):
        # [1,2) and [2,3) touch and should merge into [1,3).
        self.assertEqual(normalize([(1, 2), (2, 3)]), [(1, 3)])

    def test_nested(self):
        self.assertEqual(normalize([(1, 10), (3, 5)]), [(1, 10)])

    def test_degenerate_dropped(self):
        self.assertEqual(normalize([(1, 1), (2, 3), (4, 4)]), [(2, 3)])

    def test_negative_and_float(self):
        self.assertEqual(
            normalize([(-1.5, 0.0), (0.0, 1.5)]),
            [(-1.5, 1.5)],
        )


class TestMergeAlias(unittest.TestCase):
    def test_merge_is_normalize(self):
        data = [(5, 6), (1, 3), (2, 4)]
        self.assertEqual(merge(data), normalize(data))


class TestIntersect(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(intersect([], [(1, 2)]), [])
        self.assertEqual(intersect([(1, 2)], []), [])

    def test_disjoint(self):
        self.assertEqual(intersect([(1, 2)], [(3, 4)]), [])

    def test_overlap(self):
        self.assertEqual(intersect([(1, 5)], [(3, 7)]), [(3, 5)])

    def test_multiple(self):
        a = [(1, 10)]
        b = [(2, 3), (5, 6)]
        self.assertEqual(intersect(a, b), [(2, 3), (5, 6)])

    def test_touching_edges(self):
        # [1,2) and [2,3) share only the point 2, which is not in the
        # half-open intersection.
        self.assertEqual(intersect([(1, 2)], [(2, 3)]), [])


class TestSubtract(unittest.TestCase):
    def test_empty_b(self):
        self.assertEqual(subtract([(1, 2)], []), [(1, 2)])

    def test_empty_a(self):
        self.assertEqual(subtract([], [(1, 2)]), [])

    def test_remove_middle(self):
        self.assertEqual(subtract([(1, 10)], [(3, 5)]), [(1, 3), (5, 10)])

    def test_remove_cover(self):
        self.assertEqual(subtract([(1, 5)], [(0, 6)]), [])

    def test_remove_left(self):
        self.assertEqual(subtract([(1, 5)], [(0, 3)]), [(3, 5)])

    def test_remove_right(self):
        self.assertEqual(subtract([(1, 5)], [(3, 6)]), [(1, 3)])

    def test_multiple_holes(self):
        self.assertEqual(
            subtract([(1, 10)], [(2, 3), (5, 6)]),
            [(1, 2), (3, 5), (6, 10)],
        )

    def test_subtract_unsorted(self):
        self.assertEqual(
            subtract([(5, 8), (1, 4)], [(2, 3), (6, 7)]),
            [(1, 2), (3, 4), (5, 6), (7, 8)],
        )


class TestTotalLength(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(total_length([]), 0)

    def test_single(self):
        self.assertEqual(total_length([(1, 3)]), 2)

    def test_overlapping(self):
        self.assertEqual(total_length([(1, 5), (3, 7)]), 6)

    def test_float(self):
        self.assertAlmostEqual(total_length([(0.0, 0.5), (0.25, 1.0)]), 1.0)


if __name__ == "__main__":
    unittest.main()
