# coding=utf-8
"""Tests for the Day 17: Pyroclastic Flow puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools.puzzle_solving import read_puzzle_input

# Local application imports:
from aoc2022.day_17.tools import RockPit


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        patterns = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
        self.pit = RockPit(jet_patterns=patterns)

    def test_rock_height_after_1_rock(self):
        """The rock tower reaches 1 height after 1 rock have stopped falling."""
        self.pit.drop_rocks(n_rocks=1)
        self.assertEqual(1, self.pit.tower_height)

    def test_rock_height_after_2_rocks(self):
        """The rock tower reaches 4 height after 2 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=2)
        self.assertEqual(4, self.pit.tower_height)

    def test_rock_height_after_3_rocks(self):
        """The rock tower reaches 6 height after 2 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=3)
        self.assertEqual(6, self.pit.tower_height)

    def test_rock_height_after_4_rocks(self):
        """The rock tower reaches 7 height after 2 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=4)
        self.assertEqual(7, self.pit.tower_height)

    def test_rock_height_after_5_rocks(self):
        """The rock tower reaches 9 height after 2 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=5)
        self.assertEqual(9, self.pit.tower_height)

    def test_rock_height_after_10_rocks(self):
        """The rock tower reaches 17 height after 2 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=10)
        self.assertEqual(17, self.pit.tower_height)

    def test_rock_height_after_2022_rocks(self):
        """The rock tower reaches 3068 height after 2022 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=2022)
        self.assertEqual(3068, self.pit.tower_height)

    @unittest.skip
    def test_rock_height_after_1e12_rocks(self):
        """The rock tower reaches a HUGE height after 1e12 rocks have stopped falling."""
        self.pit.drop_rocks(n_rocks=int(1e12))
        self.assertEqual(1514285714288, self.pit.tower_height)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_17/puzzle_input.txt"
        patterns = read_puzzle_input(input_file=input_file)[0]
        self.pit = RockPit(jet_patterns=patterns)

    def test_solution_for_part_1(self):
        """After 2022 thrown rocks, the tower reaches a height of 3117 units."""
        self.pit.drop_rocks(n_rocks=2022)
        self.assertEqual(3117, self.pit.tower_height)
