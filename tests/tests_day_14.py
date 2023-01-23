# coding=utf-8
"""Tests for the Day 14: Regolith Reservoir puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_14.tools import AbyssCave, FloorCave, AbyssError, SourceError


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        rock_paths = ["498,4 -> 498,6 -> 496,6", "503,4 -> 502,4 -> 502,9 -> 494,9"]
        self.cave = AbyssCave(rock_paths=rock_paths)
        self.floor_cave = FloorCave(rock_paths=rock_paths)

    def test_rock_obstacles(self):
        """There are 18 cells occupied with rock structures in the cave."""
        expected_cells = {
            (494, 9), (495, 9), (496, 9), (497, 9), (498, 9), (499, 9), (500, 9),
            (501, 9), (502, 9), (502, 8), (502, 7), (502, 6), (502, 5), (502, 4),
            (503, 4), (496, 6), (497, 6), (498, 6), (498, 5), (498, 4)}
        self.assertSetEqual(expected_cells, {c.xy for c in self.cave.rock_cells})

    def test_sand_pile_after_puring_1_block(self):
        """The pile of sand resting in the cave contains 1 cell filled with sand."""
        expected_cells = {(500, 8)}
        self.cave.pour_times(times=1)
        self.assertSetEqual(expected_cells, {c.xy for c in self.cave.sand_cells})

    def test_sand_pile_after_puring_2_block(self):
        """The pile of sand resting in the cave contains 2 cells filled with sand."""
        expected_cells = {(500, 8), (499, 8)}
        self.cave.pour_times(times=2)
        self.assertSetEqual(expected_cells, {c.xy for c in self.cave.sand_cells})

    def test_sand_pile_after_puring_5_block(self):
        """The pile of sand resting in the cave contains 5 cells filled with sand."""
        expected_cells = {(500, 8), (499, 8), (501, 8), (498, 8), (500, 7)}
        self.cave.pour_times(times=5)
        self.assertSetEqual(expected_cells, {c.xy for c in self.cave.sand_cells})

    def test_sand_pile_after_puring_22_block(self):
        """The pile of sand resting in the cave contains 22 cells filled with sand."""
        self.cave.pour_times(times=22)
        self.assertEqual(22, len(self.cave.sand_cells))

    def test_sand_pile_after_puring_24_block(self):
        """The pile of sand resting in the cave contains 24 cells filled with sand."""
        self.cave.pour_times(times=24)
        self.assertEqual(24, len(self.cave.sand_cells))

    def test_sand_pile_after_pouring_all_possible_sand_in_abyss_cave(self):
        """Only 24 blocks of sand may be poured before they start falling."""
        with self.assertRaises(AbyssError):
            self.cave.pour_while_possible(raise_error=True)
        self.assertEqual(24, len(self.cave.sand_cells))

    def test_sand_pile_after_pouring_all_possible_sand_in_floor_cave(self):
        """Only 93 blocks of sand may be poured before they block the source."""
        with self.assertRaises(SourceError):
            self.floor_cave.pour_while_possible(raise_error=True)
        self.assertEqual(93, len(self.floor_cave.sand_cells))


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_14/puzzle_input.txt"
        self.rock_paths = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """Only 728 blocks of sand may be poured before they start falling."""
        cave = AbyssCave(rock_paths=self.rock_paths)
        cave.pour_while_possible(raise_error=False)
        self.assertEqual(728, len(cave.sand_cells))

    def test_solution_for_part_2(self):
        """Only 27623 blocks of sand may be poured before they block the source."""
        floor_cave = FloorCave(rock_paths=self.rock_paths)
        floor_cave.pour_while_possible(raise_error=False)
        self.assertEqual(27623, len(floor_cave.sand_cells))
