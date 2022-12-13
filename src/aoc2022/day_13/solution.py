# coding=utf-8
"""Compute the solution of the Day 13: Distress Signal puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_13.tools import DistressSignal


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_13/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    distress_signal = DistressSignal.from_strings(signal_lines=lines)
    return distress_signal.ordered_pairs_sum, distress_signal.decoder_key_fast
