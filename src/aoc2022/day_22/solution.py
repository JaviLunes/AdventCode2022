# coding=utf-8
"""Compute the solution of the Day 22: Monkey Map puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_22.tools import BoardTraveller


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_22/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    traveller = BoardTraveller.from_notes(monkey_notes=lines)
    traveller.travel()
    return traveller.pass_code, None
