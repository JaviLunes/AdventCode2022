# coding=utf-8
"""Compute the solution of the Day 5: Supply Stacks puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_5.tools import CrateMover9000, CrateMover9001


def compute_solution() -> tuple[str, str]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_5/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    crane_0 = CrateMover9000(crane_instructions=lines)
    crane_1 = CrateMover9001(crane_instructions=lines)
    crane_0.rearrange_stacks()
    crane_1.rearrange_stacks()
    return crane_0.top_crates, crane_1.top_crates
