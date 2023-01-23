# coding=utf-8
"""Tests for the Day 15: Beacon Exclusion Zone puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_15.tools import Constellation, Point, Sensor


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        sensor_reports = [
            "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
            "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
            "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
            "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
            "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
            "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
            "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
            "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
            "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
            "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
            "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
            "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
            "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
            "Sensor at x=20, y=1: closest beacon is at x=15, y=3"]
        self.constellation = Constellation.from_report(report=sensor_reports)

    def test_count_excluded_points_y_9(self):
        """There are 25 positions of y=9 guaranteed to not have a beacon."""
        self.assertEqual(25, self.constellation.count_excluded_points_at_row(y=9))

    def test_count_excluded_points_y_10(self):
        """There are 26 positions of y=10 guaranteed to not have a beacon."""
        self.assertEqual(26, self.constellation.count_excluded_points_at_row(y=10))

    def test_count_excluded_points_y_11(self):
        """There are 28 positions of y=11 guaranteed to not have a beacon."""
        self.assertEqual(28, self.constellation.count_excluded_points_at_row(y=11))

    def test_distress_beacon_location(self):
        """The only valid position for the distress beacon is (14, 11)."""
        beacon = self.constellation.find_distress_beacon(search_area_side=20)
        self.assertTupleEqual((14, 11), beacon.xy)

    def test_distress_beacon_frequency(self):
        """The tuning frequency of the distress beacon is 56000011."""
        beacon = self.constellation.find_distress_beacon(search_area_side=20)
        self.assertEqual(56000011, beacon.tuning_freq)


class CustomTests(unittest.TestCase):
    def test_perimeter_points_1(self):
        """There are 8 points one unit away from this Sensor's exclusion radius."""
        expected = {
            Point(x=0, y=2), Point(x=1, y=1), Point(x=2, y=0), Point(x=1, y=-1),
            Point(x=0, y=-2), Point(x=-1, y=-1), Point(x=-2, y=0), Point(x=-1, y=1)}
        sensor = Sensor(x=0, y=0, beacon_x=1, beacon_y=0)
        self.assertEqual(1, sensor.exclusion_radius)
        self.assertSetEqual(expected, set(sensor.perimeter_points))

    def test_perimeter_points_2(self):
        """There are 40 points one unit away from this Sensor's exclusion radius."""
        sensor = Sensor(x=8, y=7, beacon_x=2, beacon_y=10)
        self.assertEqual(9, sensor.exclusion_radius)
        self.assertEqual(40, len(list(sensor.perimeter_points)))


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_15/puzzle_input.txt"
        sensor_reports = read_puzzle_input(input_file=input_file)
        self.constellation = Constellation.from_report(report=sensor_reports)

    def test_solution_for_part_1(self):
        """There are 5525847 positions at row 2000000 guaranteed to not have a beacon."""
        excluded_points = self.constellation.count_excluded_points_at_row(y=2000000)
        self.assertEqual(5525847, excluded_points)

    def test_solution_for_part_2(self):
        """The tuning frequency of the distress beacon is 13340867187704."""
        beacon = self.constellation.find_distress_beacon(search_area_side=4000000)
        self.assertEqual(13340867187704, beacon.tuning_freq)
