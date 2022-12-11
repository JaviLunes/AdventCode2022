# coding=utf-8
"""Compute the solution of the Day 11: Monkey in the Middle puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_11.tools import MonkeyGang


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_11/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    gang_1 = MonkeyGang.from_notes(notes=lines, infuriating=False)
    gang_1.do_rounds(rounds=20)
    gang_2 = MonkeyGang.from_notes(notes=lines, infuriating=True)
    gang_2.do_rounds(rounds=10000)
    return gang_1.monkey_business, gang_2.monkey_business
