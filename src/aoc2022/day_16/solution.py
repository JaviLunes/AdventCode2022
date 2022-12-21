# coding=utf-8
"""Compute the solution of the Day 16: Proboscidea Volcanium puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_16.tools import ValveSim


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_16/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    plan_1 = ValveSim.from_scan_report(scan_report=lines, total_time=30)
    plan_2 = ValveSim.from_scan_report(scan_report=lines, total_time=26)
    return plan_1.find_max_release(), plan_2.find_max_release_with_help()
