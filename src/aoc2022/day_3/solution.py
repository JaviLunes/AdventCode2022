# coding=utf-8
"""Compute the solution of the Day 3: Rucksack Reorganization puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_3.tools import RuckSackPack


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_3/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    pack = RuckSackPack(items_list=lines)
    return pack.total_duplicated_priority, pack.total_badge_priorities
