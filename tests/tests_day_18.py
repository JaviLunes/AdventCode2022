# coding=utf-8
"""Tests for the Day 18: Boiling Boulders puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_18.tools import Droplet


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        scan_output = ["2,2,2", "1,2,2", "3,2,2", "2,1,2", "2,3,2", "2,2,1", "2,2,3",
                       "2,2,4", "2,2,6", "1,2,5", "3,2,5", "2,1,5", "2,3,5"]
        self.droplet = Droplet.from_scan_output(scan_output=scan_output)

    def test_surface_area(self):
        """The surface area of the scanned Droplet is 64."""
        self.assertEqual(64, self.droplet.surface_area)

    def test_external_surface_area(self):
        """The external surface area of the scanned Droplet is 58."""
        self.assertEqual(58, self.droplet.external_surface_area)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_18/puzzle_input.txt"
        scan_output = read_puzzle_input(input_file=input_file)
        self.droplet = Droplet.from_scan_output(scan_output=scan_output)

    def test_solution_for_part_1(self):
        """The surface area of the lava droplet is 4322."""
        self.assertEqual(4322, self.droplet.surface_area)

    def test_solution_for_part_2(self):
        """The external surface area of the lava droplet is 2516."""
        self.assertEqual(2516, self.droplet.external_surface_area)
