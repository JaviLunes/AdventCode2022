# coding=utf-8
"""Compute the solution of the Day 20: Grove Positioning System puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_20.tools import EncryptedFile


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_20/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    file_1 = EncryptedFile.from_strings(*lines)
    file_2 = EncryptedFile.from_strings(*lines, key=811589153, passes=10)
    return file_1.groove_sum, file_2.groove_sum
