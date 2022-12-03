# coding=utf-8
"""Compute the solution of the Day 3: Rucksack Reorganization puzzle."""

# Local application imports:
from aoc2022.common import read_puzzle_input
from aoc2022.day_3.tools import RuckSackPack


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=3)
    pack = RuckSackPack(items_list=lines)
    return pack.total_duplicated_priority, pack.total_badge_priorities
