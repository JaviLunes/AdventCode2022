# coding=utf-8
"""Tests for the Day 18: Boiling Boulders puzzle."""

# Standard library imports:
import unittest

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
