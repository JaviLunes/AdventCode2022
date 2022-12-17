# coding=utf-8
"""Compute the solution of the Day 15: Beacon Exclusion Zone puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_15.tools import Constellation


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_15/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    constellation = Constellation.from_report(report=lines)
    excluded_locations = constellation.count_excluded_points_at_row(y=2000000)
    distress_beacon = constellation.find_distress_beacon(search_area_side=4000000)
    return excluded_locations, distress_beacon.tuning_freq
