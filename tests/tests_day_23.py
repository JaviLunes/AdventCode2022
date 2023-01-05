# coding=utf-8
"""Tests for the Day 23: Unstable Diffusion puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Local application imports:
from aoc2022.day_23.tools import ElfGrove
from aoc2022.day_23.visualization import plot_grove


class SmallExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        scan_lines = [".....", "..##.", "..#..", ".....", "..##.", "....."]
        self.grove = ElfGrove.from_scan(scan_lines=scan_lines)

    def _validate_show_and_close(self, fig: Figure):
        """Check that a matplotlib.Figure was created, show it, and then close it."""
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_empty_tiles_after_round_0(self):
        """Before doing any rounds, the Elves cover an 3-empty-tile rectangle."""
        self.assertEqual(3, self.grove.empty_tiles)

    def test_empty_tiles_after_round_1(self):
        """Before doing any rounds, the Elves cover an 5-empty-tile rectangle."""
        self.grove.evolve(rounds=1)
        self.assertEqual(5, self.grove.empty_tiles)

    def test_empty_tiles_after_round_3(self):
        """Before doing any rounds, the Elves cover an 25-empty-tile rectangle."""
        self.grove.evolve(rounds=3)
        self.assertEqual(25, self.grove.empty_tiles)

    def test_plot_grove_elves_for_3_rounds(self):
        """Plot the tested ElfGrove at start and after each of 3 rounds."""
        self._validate_show_and_close(fig=plot_grove(grove=self.grove))
        for _ in range(3):
            self.grove.evolve(rounds=1)
            self._validate_show_and_close(fig=plot_grove(grove=self.grove))


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        scan_lines = [
            "....#..", "..###.#", "#...#.#", ".#...##", "#.###..", "##.#.##", ".#..#.."]
        self.grove = ElfGrove.from_scan(scan_lines=scan_lines)

    def _validate_show_and_close(self, fig: Figure):
        """Check that a matplotlib.Figure was created, show it, and then close it."""
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_empty_tiles_after_round_0(self):
        """Before doing any rounds, the Elves cover an 27-empty-tile rectangle."""
        self.assertEqual(27, self.grove.empty_tiles)

    def test_empty_tiles_after_round_10(self):
        """After completing 10 rounds, the Elves cover an 110-empty-tile rectangle."""
        self.grove.evolve(rounds=10)
        self.assertEqual(110, self.grove.empty_tiles)

    def test_number_of_rounds_needed(self):
        """The first round where no Elf needs to move is round 20."""
        self.grove.evolve_while_needed()
        self.assertEqual(20, self.grove.completed_rounds + 1)

    def test_plot_grove_elves_for_10_rounds(self):
        """Plot the tested ElfGrove at start and after each of 10 rounds."""
        self._validate_show_and_close(fig=plot_grove(grove=self.grove))
        for _ in range(10):
            self.grove.evolve(rounds=1)
            self._validate_show_and_close(fig=plot_grove(grove=self.grove))


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_23/puzzle_input.txt"
        scan_lines = read_puzzle_input(input_file=input_file)
        self.grove = ElfGrove.from_scan(scan_lines=scan_lines)

    def test_empty_tiles_after_round_10(self):
        """After completing 10 rounds, the Elves cover an 3996-empty-tile rectangle."""
        self.grove.evolve(rounds=10)
        self.assertEqual(3996, self.grove.empty_tiles)

    def test_number_of_rounds_needed(self):
        """The first round where no Elf needs to move is round 908."""
        self.grove.evolve_while_needed()
        self.assertEqual(908, self.grove.completed_rounds + 1)
