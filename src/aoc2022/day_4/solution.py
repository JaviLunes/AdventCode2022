# coding=utf-8
"""Compute the solution of the Day 4: Camp Cleanup puzzle."""

# Local application imports:
from aoc2022.common import read_puzzle_input
from aoc2022.day_4.tools import CleanupReviewer


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=4)
    reviewer = CleanupReviewer(assignment_pairs=lines)
    return reviewer.count_ful_overlaps, reviewer.count_partial_overlaps
