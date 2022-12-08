# coding=utf-8
"""Compute the solution of the Day 8: Treetop Tree House puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_8.tools import TreeGrid


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_8/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    grid = TreeGrid(height_strings=lines)
    return sum(grid.tree_visibility.flatten()), max(grid.scenic_scores.flatten())
