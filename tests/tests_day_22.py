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
from aoc2022.day_22.tools import Board, WalkPlan
from aoc2022.day_22.visualization import plot_board, plot_traveller


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        monkey_notes = [
            "        ...#", "        .#..", "        #...", "        ....",
            "...#.......#", "........#...", "..#....#....", "..........#.",
            "        ...#....", "        .....#..", "        .#......",
            "        ......#.", "", "10R5L5R10L4R5L5"]
        self.walk_plan = WalkPlan.from_monkey_notes(notes=monkey_notes)
        self.board = Board.from_notes(monkey_notes=monkey_notes, area_size=4)

    def test_final_position(self):
        """Your row, column and facing after completing the travel are 6, 8, 0."""
        traveller = self.board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=self.board)
        self.assertEqual(6, traveller.position[0] + 1)
        self.assertEqual(8, traveller.position[1] + 1)
        self.assertEqual("→", str(traveller.position[2]))

    def test_final_password(self):
        """The password revealed after completing the travel is 6032."""
        traveller = self.board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=self.board)
        self.assertEqual(6032, traveller.pass_code)

    def test_plot_board(self):
        """Plot the tested Board."""
        fig = plot_board(board=self.board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_travel(self):
        """Plot the tested Traveller at the end of their walk."""
        traveller = self.board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=self.board)
        fig = plot_traveller(traveller=traveller, board=self.board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_22/puzzle_input.txt"
        monkey_notes = read_puzzle_input(input_file=input_file)
        self.walk_plan = WalkPlan.from_monkey_notes(notes=monkey_notes)
        self.board = Board.from_notes(monkey_notes=monkey_notes, area_size=50)

    def test_final_password(self):
        """The password revealed after completing the travel is 189140."""
        traveller = self.board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=self.board)
        self.assertEqual(189140, traveller.pass_code)
