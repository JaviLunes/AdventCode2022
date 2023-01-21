# coding=utf-8
"""Tests for the Day 25: Full of Hot Air puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_25.tools import SNAFU, ZERO_SNAFU


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.fuel_snafu = [
            "1=-0-2", "12111", "2=0=", "21", "2=01", "111", "20012", "112", "1=-1=",
            "1-12", "12", "1=", "122"]
        self.fuel_decimal = [
            1747, 906, 198, 11, 201, 31, 1257, 32, 353, 107, 7, 3, 37]
        self.brochure_snafu = [
            "1", "2", "1=", "1-", "10", "11", "12", "2=", "2-", "20", "1=0", "1-0",
            "1=11-2", "1-0---0", "1121-1110-1=0"]
        self.brochure_decimal = [
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 2022, 12345, 314159265]

    def test_brochure_conversion_decimal_to_snafu(self):
        """Generate SNAFU numbers from their known decimal number counterparts."""
        decimal_values = self.brochure_decimal
        expected_snafu_values = self.brochure_snafu
        for decimal, expected in zip(decimal_values, expected_snafu_values):
            snafu = SNAFU.from_decimal(decimal=decimal)
            self.assertEqual(SNAFU.from_string(string=expected), snafu)

    def test_brochure_conversion_snafu_to_decimal(self):
        """Generate known decimal numbers from their known SNAFU counterparts."""
        snafu_values = self.brochure_snafu
        expected_decimal_values = self.brochure_decimal
        for snafu, expected in zip(snafu_values, expected_decimal_values):
            decimal = SNAFU.from_string(string=snafu).as_decimal
            self.assertEqual(expected, decimal)

    def test_fuel_conversion_decimal_to_snafu(self):
        """Generate SNAFU numbers from their known decimal number counterparts."""
        decimal_values = self.fuel_decimal
        expected_snafu_values = self.fuel_snafu
        for decimal, expected in zip(decimal_values, expected_snafu_values):
            snafu = SNAFU.from_decimal(decimal=decimal)
            self.assertEqual(SNAFU.from_string(string=expected), snafu)

    def test_fuel_conversion_snafu_to_decimal(self):
        """Generate known decimal numbers from their known SNAFU counterparts."""
        snafu_values = self.fuel_snafu
        expected_decimal_values = self.fuel_decimal
        for snafu, expected in zip(snafu_values, expected_decimal_values):
            decimal = SNAFU.from_string(string=snafu).as_decimal
            self.assertEqual(expected, decimal)

    def test_total_fuel_requirement_in_decimal(self):
        """The decimal value of the sum of fuel requirements is 4890."""
        values = [SNAFU.from_string(string=string) for string in self.fuel_snafu]
        self.assertEqual(4890, sum(values, start=ZERO_SNAFU).as_decimal)

    def test_total_fuel_requirement_in_snafu(self):
        """The SNAFU value of the sum of fuel requirements is '2=-1=0'."""
        values = [SNAFU.from_string(string=string) for string in self.fuel_snafu]
        self.assertEqual("2=-1=0", sum(values, start=ZERO_SNAFU).as_string)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_25/puzzle_input.txt"
        self.fuel_snafu = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """The SNAFU value of the sum of fuel requirements is '2=0-2-1-0=20-01-2-20'."""
        values = [SNAFU.from_string(string=string) for string in self.fuel_snafu]
        self.assertEqual("2=0-2-1-0=20-01-2-20", sum(values, start=ZERO_SNAFU).as_string)

    def test_solution_for_part_2(self):
        """There is no second part, the star-fruit smoothie is blended!."""
        pass
