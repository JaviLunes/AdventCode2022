# coding=utf-8
"""Compute the solution of the Day 4: Camp Cleanup puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_4.tools import CleanupReviewer


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_4/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    reviewer = CleanupReviewer(assignment_pairs=lines)
    return reviewer.count_full_overlaps, reviewer.count_partial_overlaps
