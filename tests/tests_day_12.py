# coding=utf-8
"""Tests for the Day 12: Hill Climbing Algorithm puzzle."""

# Standard library imports:
import unittest

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
