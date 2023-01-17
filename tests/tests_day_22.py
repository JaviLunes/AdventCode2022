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
from aoc2022.day_22.hardcoded_edges import EXAMPLE_EDGES, INPUT_EDGES


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.notes = [
            "        ...#", "        .#..", "        #...", "        ....",
            "...#.......#", "........#...", "..#....#....", "..........#.",
            "        ...#....", "        .....#..", "        .#......",
            "        ......#.", "", "10R5L5R10L4R5L5"]
        self.walk_plan = WalkPlan.from_monkey_notes(notes=self.notes)

    def test_final_position_for_board_plane(self):
        """Your row, column and facing after completing the travel are 6, 8, 0."""
        board = Board.from_notes(notes=self.notes, area_size=4, cube_mode=False)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        (row, col), facing = traveller.position
        self.assertEqual(6, row + 1)
        self.assertEqual(8, col + 1)
        self.assertEqual("→", str(facing))

    def test_final_password_for_board_plane(self):
        """The password revealed after completing the travel is 6032."""
        board = Board.from_notes(notes=self.notes, area_size=4, cube_mode=False)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        self.assertEqual(6032, traveller.pass_code)

    def test_final_position_for_board_cube(self):
        """Your row, column and facing after completing the travel are 5, 7, 3."""
        board = Board.from_notes(
            notes=self.notes, area_size=4, cube_mode=True, hardcoded_edges=EXAMPLE_EDGES)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        (row, col), facing = traveller.position
        self.assertEqual(5, row + 1)
        self.assertEqual(7, col + 1)
        self.assertEqual("↑", str(facing))

    def test_final_password_for_board_cube(self):
        """The password revealed after completing the travel is 5031."""
        board = Board.from_notes(
            notes=self.notes, area_size=4, cube_mode=True, hardcoded_edges=EXAMPLE_EDGES)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        self.assertEqual(5031, traveller.pass_code)

    def test_plot_board_plane(self):
        """Plot the tested Board in 2D-plane mode."""
        board = Board.from_notes(notes=self.notes, area_size=4, cube_mode=False)
        fig = plot_board(board=board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_board_cube(self):
        """Plot the tested Board in 3D-cube mode."""
        board = Board.from_notes(
            notes=self.notes, area_size=4, cube_mode=True, hardcoded_edges=EXAMPLE_EDGES)
        fig = plot_board(board=board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_board_plane_travel(self):
        """Plot the tested Traveller at the end of their walk."""
        board = Board.from_notes(notes=self.notes, area_size=4, cube_mode=False)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        fig = plot_traveller(traveller=traveller, board=board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)

    def test_plot_board_cube_travel(self):
        """Plot the tested Traveller at the end of their walk."""
        board = Board.from_notes(
            notes=self.notes, area_size=4, cube_mode=True, hardcoded_edges=EXAMPLE_EDGES)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        fig = plot_traveller(traveller=traveller, board=board)
        self.assertIsInstance(fig, Figure)
        fig.show()
        plt.close(fig)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_22/puzzle_input.txt"
        self.notes = read_puzzle_input(input_file=input_file)
        self.walk_plan = WalkPlan.from_monkey_notes(notes=self.notes)

    def test_solution_for_part_1(self):
        """The password revealed after completing the travel is 189140."""
        board = Board.from_notes(notes=self.notes, area_size=50, cube_mode=False)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        self.assertEqual(189140, traveller.pass_code)

    def test_solution_for_part_2(self):
        """The password revealed after completing the travel is 115063."""
        board = Board.from_notes(
            notes=self.notes, area_size=50, cube_mode=True, hardcoded_edges=INPUT_EDGES)
        traveller = board.spawn_traveller()
        self.walk_plan.execute_plan(traveller=traveller, board=board)
        self.assertEqual(115063, traveller.pass_code)
