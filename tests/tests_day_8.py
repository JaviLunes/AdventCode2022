# coding=utf-8
"""Tests for the Day 8: Treetop Tree House puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_8.tools import TreeGrid


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.tree_heights = ["30373", "25512", "65332", "33549", "35390"]

    def test_visible_trees(self):
        """The number of trees visible from outside the grid is 21."""
        grid = TreeGrid(height_strings=self.tree_heights)
        self.assertEqual(21, sum(grid.tree_visibility.flatten()))

    def test_max_view_distance(self):
        """The maximum scenic score of any tree in the TreeGrid is 8."""
        grid = TreeGrid(height_strings=self.tree_heights)
        self.assertEqual(8, max(grid.scenic_scores.flatten()))
