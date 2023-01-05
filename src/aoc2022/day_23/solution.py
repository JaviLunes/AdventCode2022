# coding=utf-8
"""Compute the solution of the Day 23: Unstable Diffusion puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_23.tools import ElfGrove


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_23/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    grove = ElfGrove.from_scan(scan_lines=lines)
    grove.evolve(rounds=10)
    empty_tiles_after_10 = grove.empty_tiles
    grove.evolve_while_needed()
    return empty_tiles_after_10, grove.completed_rounds + 1
