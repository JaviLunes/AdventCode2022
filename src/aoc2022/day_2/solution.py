# coding=utf-8
"""Compute the solution of the Day 2: Day 2: Rock Paper Scissors puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_2.tools import Tournament


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_2/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    tournament_1 = Tournament(strategy=lines, tells_your_draw=True)
    tournament_2 = Tournament(strategy=lines, tells_your_draw=False)
    return tournament_1.total_score, tournament_2.total_score
