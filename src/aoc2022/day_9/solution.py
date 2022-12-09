# coding=utf-8
"""Compute the solution of the Day 9: Rope Bridge puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_9.tools import Rope


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_9/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    short_rope, long_rope = Rope(nodes=2), Rope(nodes=10)
    short_rope.apply_motions(motions=lines)
    long_rope.apply_motions(motions=lines)
    return len(set(short_rope.tail_positions)), len(set(long_rope.tail_positions))
