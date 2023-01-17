# coding=utf-8
"""Compute the solution of the Day 22: Monkey Map puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_22.tools import Board, WalkPlan
from aoc2022.day_22.hardcoded_edges import INPUT_EDGES


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_22/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    walk_plan = WalkPlan.from_monkey_notes(notes=lines)
    board_1 = Board.from_notes(notes=lines, area_size=50, cube_mode=False)
    board_2 = Board.from_notes(
        notes=lines, area_size=50, cube_mode=True, hardcoded_edges=INPUT_EDGES)
    traveller_1 = board_1.spawn_traveller()
    traveller_2 = board_2.spawn_traveller()
    walk_plan.execute_plan(traveller=traveller_1, board=board_1)
    walk_plan.execute_plan(traveller=traveller_2, board=board_2)
    return traveller_1.pass_code, traveller_2.pass_code
