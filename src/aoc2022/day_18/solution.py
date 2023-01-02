# coding=utf-8
"""Compute the solution of the Day 18: Boiling Boulders puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_18.tools import Droplet


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_18/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    droplet = Droplet.from_scan_output(scan_output=lines)
    return droplet.surface_area, droplet.external_surface_area
