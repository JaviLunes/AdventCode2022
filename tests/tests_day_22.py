# coding=utf-8
"""Tests for the Day 22: Monkey Map puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_22.tools import BoardTraveller
from aoc2022.day_22.visualization import plot_board, plot_traveller


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        monkey_notes = [
            "        ...#", "        .#..", "        #...", "        ....",
            "...#.......#", "........#...", "..#....#....", "..........#.",
            "        ...#....", "        .....#..", "        .#......",
            "        ......#.", "", "10R5L5R10L4R5L5"]
        self.traveller = BoardTraveller.from_notes(monkey_notes=monkey_notes)

    def test_final_position(self):
        """Your row, column and facing after completing the travel are 6, 8, 0."""
        self.traveller.travel()
        row, column, facing = self.traveller.coordinates
        self.assertEqual(6, row + 1)
        self.assertEqual(8, column + 1)
        self.assertEqual("→", facing)

    def test_final_password(self):
        """The password revealed after completing the travel is 6032."""
        self.traveller.travel()
        self.assertEqual(6032, self.traveller.pass_code)

    def test_plot_board(self):
        """Plot the tested MonkeyBoard."""
        fig = plot_board(board=self.traveller.board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_traveller_at_begin(self):
        """Plot the tested BoardTraveller before the start of their walk."""
        fig = plot_traveller(traveller=self.traveller)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_traveller_at_end(self):
        """Plot the tested BoardTraveller at the end of their walk."""
        self.traveller.travel()
        fig = plot_traveller(traveller=self.traveller)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_22/puzzle_input.txt"
        monkey_notes = read_puzzle_input(input_file=input_file)
        self.traveller = BoardTraveller.from_notes(monkey_notes=monkey_notes)

    def test_final_password(self):
        """The password revealed after completing the travel is 189140."""
        self.traveller.travel()
        self.assertEqual(189140, self.traveller.pass_code)
