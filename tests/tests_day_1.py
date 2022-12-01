# coding=utf-8
"""Tests for the Day 1: Calorie Counting puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_1.tools import ExpeditionSupplies


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.calories_list = ["1000", "2000", "3000", "", "4000", "", "5000", "6000",
                              "", "7000", "8000", "9000", "", "10000"]

    def test_calories_per_elf(self):
        """Validate the number of total calories carried by each Elf."""
        expedition = ExpeditionSupplies(calories_list=self.calories_list)
        expected = [6000, 4000, 11000, 24000, 10000]
        self.assertListEqual(expected, expedition.calories_per_elf)

    def test_elf_with_most_calories(self):
        """The Elf with the highest amount of calories is carrying a total of 24000."""
        expedition = ExpeditionSupplies(calories_list=self.calories_list)
        elves = expedition.sort_elves_by_calories()
        self.assertEqual(24000, elves[0].total_calories)

    def test_top_three_elves_with_most_calories(self):
        """The three Elves with the most calories carry a total of 45000."""
        expedition = ExpeditionSupplies(calories_list=self.calories_list)
        elves = expedition.sort_elves_by_calories()
        self.assertEqual(45000, sum(elf.total_calories for elf in elves[:3]))
