import unittest
from bin_search import bin_search


class TestingBinSearch(unittest.TestCase):
    def test_mid(self):
        assert bin_search([1,2,3], 2) == 1

    def test_edge_1(self):
        self.assertEqual(bin_search([1], 1), 0)

    def test_edge_2(self):
        self.assertEqual(bin_search([1,2,3], 3), 2)

    def test_edge_3(self):
        self.assertEqual(bin_search([1,2,3], 1), 0)

    def test_lower_bound(self):
        self.assertEqual(bin_search([1,2,3,5,6,7], 4), 2)

    def test_many_equals(self):
        self.assertEqual(bin_search([1,2,3,3,3,4,5,6], 3), 4)
