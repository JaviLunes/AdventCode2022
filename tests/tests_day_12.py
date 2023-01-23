# coding=utf-8
"""Tests for the Day 12: Hill Climbing Algorithm puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_12.tools import ElvesMaps


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        # noinspection SpellCheckingInspection
        height_strings = ["Sabqponm", "abcryxxl", "accszExk", "acctuvwj", "abdefghi"]
        self.hill_map = ElvesMaps(height_map=height_strings)

    def test_fewest_steps_from_given_start_to_goal(self):
        """The fewest steps required for reaching the goal from the 'S' start is 31."""
        self.assertEqual(31, self.hill_map.min_steps_for_ascension_route())

    def test_fewest_steps_from_best_start_to_goal(self):
        """The fewest steps required for reaching the goal from any 'a' start is 29."""
        self.assertEqual(29, self.hill_map.min_steps_for_scenic_route())


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_12/puzzle_input.txt"
        height_strings = read_puzzle_input(input_file=input_file)
        self.hill_map = ElvesMaps(height_map=height_strings)

    def test_solution_for_part_1(self):
        """The fewest steps required for reaching the goal from the 'S' start is 425."""
        self.assertEqual(425, self.hill_map.min_steps_for_ascension_route())

    def test_solution_for_part_2(self):
        """The fewest steps required for reaching the goal from any 'a' start is 418."""
        self.assertEqual(418, self.hill_map.min_steps_for_scenic_route())
