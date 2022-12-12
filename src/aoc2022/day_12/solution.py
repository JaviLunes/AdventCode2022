# coding=utf-8
"""Compute the solution of the Day 12: Hill Climbing Algorithm puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_12.tools import ElvesMaps


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_12/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    app = ElvesMaps(height_map=lines)
    return len(app.build_route_from_start()), len(app.build_scenic_route())
