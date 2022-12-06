# coding=utf-8
"""Compute the solution of the Day 6: Tuning Trouble puzzle."""

# Local application imports:
from aoc2022.common import read_puzzle_input
from aoc2022.day_6.tools import StreamDecoder


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=6)
    decoder = StreamDecoder(datastream="".join(lines))
    return decoder.first_packet_start, decoder.first_message_start
