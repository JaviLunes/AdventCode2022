# coding=utf-8
"""Compute the solution of the Day 24: Blizzard Basin puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_24.tools import Valley


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_24/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    valley = Valley.from_strings(strings=lines)
    expedition_1 = valley.plan_travel_to_goal(t=0)
    expedition_2 = valley.plan_travel_to_start(t=expedition_1.t)
    expedition_3 = valley.plan_travel_to_goal(t=expedition_2.t)
    return expedition_1.t, expedition_3.t
