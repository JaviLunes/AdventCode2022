# coding=utf-8
"""Compute the solution of the Day 1: Calorie Counting puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_1.tools import ExpeditionSupplies


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_1/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    expedition = ExpeditionSupplies(calories_list=lines)
    elves = expedition.sort_elves_by_calories()
    top_one_calories = elves[0].total_calories
    top_three_calories = sum(elf.total_calories for elf in elves[:3])
    return top_one_calories, top_three_calories
