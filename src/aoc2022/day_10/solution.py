# coding=utf-8
"""Compute the solution of the Day 10: Cathode-Ray Tube puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_10.tools import CPURegister, CRTScreen


def compute_solution() -> tuple[int, str]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_10/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    register = CPURegister(program=lines)
    screen = CRTScreen(register=register)
    return register.significant_strength, screen.characters
