# coding=utf-8
"""Compute the solution of the Day 22: Monkey Map puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_22.tools import Board, WalkPlan


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_22/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    walk_plan = WalkPlan.from_monkey_notes(notes=lines)
    board = Board.from_notes(monkey_notes=lines, area_size=50)
    traveller = board.spawn_traveller()
    walk_plan.execute_plan(traveller=traveller, board=board)
    return traveller.pass_code, None
