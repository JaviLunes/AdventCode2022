# coding=utf-8
"""Compute the solution of the Day 19: Not Enough Minerals puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_19.tools import Factory


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_19/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    factory_1 = Factory.from_strings(strings=lines, operation_time=24)
    factory_2 = Factory.from_strings(strings=lines[:3], operation_time=32)
    return factory_1.total_quality_level, factory_2.geode_product
