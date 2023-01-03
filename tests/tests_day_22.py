# coding=utf-8
"""Tests for the Day 22: Monkey Map puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_22.tools import BoardTraveller


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        monkey_notes = [
            "        ...#", "        .#..", "        #...", "        ....",
            "...#.......#", "........#...", "..#....#....", "..........#.",
            "        ...#....", "        .....#..", "        .#......",
            "        ......#.", "", "10R5L5R10L4R5L5"]
        self.traveller = BoardTraveller.from_notes(monkey_notes=monkey_notes)
        self.traveller.travel()

    def test_final_position(self):
        """Your row, column and facing after completing the travel are 6, 8, 0."""
        self.assertEqual(6, self.traveller.row + 1)
        self.assertEqual(8, self.traveller.column + 1)
        self.assertEqual("→", self.traveller.facing)

    def test_final_password(self):
        """The password revealed after completing the travel is 6032."""
        self.assertEqual(6032, self.traveller.pass_code)
