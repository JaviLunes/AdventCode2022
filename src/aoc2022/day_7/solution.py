# coding=utf-8
"""Compute the solution of the Day 7: No Space Left On Device puzzle."""

# Standard library imports:
from pathlib import Path

# Local application imports:
from aoc_tools import read_puzzle_input
from aoc2022.day_7.tools import FileSystem


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    input_file = Path(__file__).parents[1] / "day_7/puzzle_input.txt"
    lines = read_puzzle_input(input_file=input_file)
    file_system = FileSystem.from_terminal_output(output=lines)
    light_dirs = file_system.find_light_dirs(max_size=100000)
    deleted_dir = file_system.find_directory_to_delete(required_space=30000000)
    return sum(d.size for d in light_dirs), deleted_dir.size
