# coding=utf-8
"""Tests for the Day 3: Rucksack Reorganization puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_3.tools import RuckSackPack


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        # noinspection SpellCheckingInspection
        items_list = ["vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                      "PmmdzqPrVvPwwTWBwg", "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                      "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"]
        self.pack = RuckSackPack(items_list=items_list)

    def test_duplicated_items(self):
        """The duplicated items in the RuckBackPack are p, L, P, v, t, s."""
        expected = ["p", "L", "P", "v", "t", "s"]
        self.assertListEqual(expected, self.pack.duplicated_items)

    def test_total_duplicated_priority(self):
        """The sum of priorities for duplicated items in each RuckSack is 157."""
        self.assertEqual(157, self.pack.total_duplicated_priority)

    def test_group_badges(self):
        """The badges for the two groups of elves are r and Z."""
        self.assertListEqual(["r", "Z"], self.pack.group_badges)

    def test_total_badge_priorities(self):
        """The sum of priorities for the badges of each group of elves is 70."""
        self.assertEqual(70, self.pack.total_badge_priorities)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_3/puzzle_input.txt"
        items = read_puzzle_input(input_file=input_file)
        self.pack = RuckSackPack(items_list=items)

    def test_solution_for_part_1(self):
        """The sum of priorities for duplicated items in each RuckSack is 7997."""
        self.assertEqual(7997, self.pack.total_duplicated_priority)

    def test_solution_for_part_2(self):
        """The sum of priorities for the badges of each group of elves is 2545."""
        self.assertEqual(2545, self.pack.total_badge_priorities)
