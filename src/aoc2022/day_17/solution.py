# coding=utf-8
"""Compute the solution of the Day 17: Pyroclastic Flow puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_17.tools import RockPit


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_17/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    pit = RockPit(jet_patterns=lines[0])
    pit.drop_rocks(n_rocks=2022)
    return pit.tower_height, None
