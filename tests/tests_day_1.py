# coding=utf-8
"""Tests for the Day 1: Calorie Counting puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

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


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_1/puzzle_input.txt"
        calories_list = read_puzzle_input(input_file=input_file)
        expedition = ExpeditionSupplies(calories_list=calories_list)
        self.elves_list = expedition.sort_elves_by_calories()

    def test_solution_for_part_1(self):
        """The elf with the highest amount of calories is carrying 69206 calories."""
        self.assertEqual(69206, self.elves_list[0].total_calories)

    def test_solution_for_part_2(self):
        """The top three elves are carrying 197400 calories."""
        self.assertEqual(197400, sum(elf.total_calories for elf in self.elves_list[:3]))
