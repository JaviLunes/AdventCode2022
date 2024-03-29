# coding=utf-8
"""Tests for the Day 4: Camp Cleanup puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_4.tools import CleanupReviewer


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        sections = ["2-4,6-8", "2-3,4-5", "5-7,7-9", "2-8,3-7", "6-6,4-6", "2-6,4-8"]
        self.reviewer = CleanupReviewer(assignment_pairs=sections)

    def test_number_of_fully_overlapping_assignment_pairs(self):
        """The number of assignment pairs with full overlap is 2."""
        self.assertEqual(2, self.reviewer.count_full_overlaps)

    def test_number_of_partially_overlapping_assignment_pairs(self):
        """The number of assignment pairs with partial overlap is 4."""
        self.assertEqual(4, self.reviewer.count_partial_overlaps)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_4/puzzle_input.txt"
        lines = read_puzzle_input(input_file=input_file)
        self.reviewer = CleanupReviewer(assignment_pairs=lines)

    def test_solution_for_part_1(self):
        """The number of assignment pairs with full overlap is 509."""
        self.assertEqual(509, self.reviewer.count_full_overlaps)

    def test_solution_for_part_2(self):
        """The number of assignment pairs with partial overlap is 870."""
        self.assertEqual(870, self.reviewer.count_partial_overlaps)
