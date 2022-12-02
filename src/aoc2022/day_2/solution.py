# coding=utf-8
"""Compute the solution of the Day 2: Day 2: Rock Paper Scissors puzzle."""

# Local application imports:
from aoc2022.common import read_puzzle_input
from aoc2022.day_2.tools import Tournament


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=2)
    tournament_1 = Tournament(strategy=lines, tells_your_draw=True)
    tournament_2 = Tournament(strategy=lines, tells_your_draw=False)
    return tournament_1.total_score, tournament_2.total_score
