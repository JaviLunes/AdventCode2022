# coding=utf-8
"""Compute the solution of the Day 21: Monkey Math puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_21.tools import MonkeyGang


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_21/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    gang = MonkeyGang.from_strings(strings=lines)
    return gang["root"], None
