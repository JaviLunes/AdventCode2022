# coding=utf-8
"""Tests for the Day 3: Rucksack Reorganization puzzle."""

# Standard library imports:
import unittest

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
