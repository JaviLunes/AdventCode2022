# coding=utf-8
"""Compute the solution of the Day 14: Regolith Reservoir puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_14.tools import AbyssCave, FloorCave


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_14/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    cave_1, cave_2 = AbyssCave(rock_paths=lines), FloorCave(rock_paths=lines)
    cave_1.pour_while_possible()
    cave_2.pour_while_possible()
    return len(cave_1.sand_cells), len(cave_2.sand_cells)
