# coding=utf-8
"""Compute the solution of the Day 25: Full of Hot Air puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_25.tools import SNAFU, ZERO_SNAFU


def compute_solution() -> tuple[str, str]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_25/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    fuel_snafu = [SNAFU.from_string(string=string) for string in lines]
    return sum(fuel_snafu, start=ZERO_SNAFU).as_string, "-"
