# coding=utf-8
"""Compute the solution of the Day 6: Tuning Trouble puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_6.tools import StreamDecoder


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_6/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    decoder = StreamDecoder(datastream="".join(lines))
    return decoder.first_packet_start, decoder.first_message_start
