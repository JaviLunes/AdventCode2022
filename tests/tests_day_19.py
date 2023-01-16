# coding=utf-8
"""Tests for the Day 19: Not Enough Minerals puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_19.tools import Factory, Pool

# Set constants:
DATA_PATH = Path(__file__).parent / "data" / "day_19"
DAY_PATH = Path(__file__).parents[1] / "src" / "aoc2022" / "day_19"


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.strings = read_puzzle_input(input_file=DATA_PATH / "example_blueprints.txt")

    def test_robot_costs_for_blueprint_1(self):
        """Validate the 1st blueprint's resources required for building each robot."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        blueprint = factory.blueprints[0]
        self.assertEqual(Pool(ore=4), blueprint.costs["ore"])
        self.assertEqual(Pool(ore=2), blueprint.costs["clay"])
        self.assertEqual(Pool(ore=3, clay=14), blueprint.costs["obsidian"])
        self.assertEqual(Pool(ore=2, obsidian=7), blueprint.costs["geode"])

    def test_robot_costs_for_blueprint_2(self):
        """Validate the 2nd blueprint's resources required for building each robot."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        blueprint = factory.blueprints[1]
        self.assertEqual(Pool(ore=2), blueprint.costs["ore"])
        self.assertEqual(Pool(ore=3), blueprint.costs["clay"])
        self.assertEqual(Pool(ore=3, clay=8), blueprint.costs["obsidian"])
        self.assertEqual(Pool(ore=3, obsidian=12), blueprint.costs["geode"])

    def test_maximum_geodes_for_factory_1_with_24_minutes(self):
        """The 1st blueprint can open a maximum of 9 geodes in 24 minutes."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(9, factory.blueprints[0].geode_output)

    def test_maximum_geodes_for_factory_2_with_24_minutes(self):
        """The 2nd blueprint can open a maximum of 12 geodes in 24 minutes."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(12, factory.blueprints[1].geode_output)

    def test_max_geodes_for_factory_1_with_32_minutes(self):
        """The 1st blueprint can open a maximum of 56 geodes in 32 minutes"""
        factory = Factory.from_strings(strings=self.strings, operation_time=32)
        self.assertEqual(56, factory.blueprints[0].geode_output)

    def test_max_geodes_for_factory_2_with_32_minutes(self):
        """The 2nd blueprint can open a maximum of 62 geodes in 32 minutes"""
        factory = Factory.from_strings(strings=self.strings, operation_time=32)
        self.assertEqual(62, factory.blueprints[1].geode_output)

    def test_quality_level_for_factory_1_with_24_minutes(self):
        """The 1st blueprint has a quality level of 9."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(9, factory.blueprints[0].quality_level)

    def test_quality_level_for_factory_2_with_24_minutes(self):
        """The 2nd blueprint has a quality level of 24."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(24, factory.blueprints[1].quality_level)

    def test_total_quality_level_with_24_minutes(self):
        """The sum of quality levels for all blueprints is 33."""
        factory = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(33, factory.total_quality_level)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.strings = read_puzzle_input(input_file=DAY_PATH / "puzzle_input.txt")

    def test_solution_for_part_1(self):
        """The total quality level for the available blueprints is 994."""
        factory_1 = Factory.from_strings(strings=self.strings, operation_time=24)
        self.assertEqual(994, factory_1.total_quality_level)

    def test_solution_for_part_2(self):
        """The product of geode outputs for the available blueprints is 15960."""
        factory_2 = Factory.from_strings(strings=self.strings[:3], operation_time=32)
        self.assertEqual(15960, factory_2.geode_product)
