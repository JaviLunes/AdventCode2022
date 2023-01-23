# coding=utf-8
"""Tests for the Day 8: Treetop Tree House puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

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


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_8/puzzle_input.txt"
        lines = read_puzzle_input(input_file=input_file)
        self.grid = TreeGrid(height_strings=lines)

    def test_solution_for_part_1(self):
        """There are 1801 trees visible from outside the grid."""
        self.assertEqual(1801, sum(self.grid.tree_visibility.flatten()))

    def test_solution_for_part_2(self):
        """The highest scenic score of any tree is 209880."""
        self.assertEqual(209880, max(self.grid.scenic_scores.flatten()))
