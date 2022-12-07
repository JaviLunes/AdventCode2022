# coding=utf-8
"""Compute the solution of the Day 7: No Space Left On Device puzzle."""

# Local application imports:
from aoc2022.common import read_puzzle_input
from aoc2022.day_7.tools import FileSystem


def compute_solution() -> tuple[int, int]:
    """Compute the answers for the two parts of this day."""
    lines = read_puzzle_input(day=7)
    file_system = FileSystem.from_terminal_output(output=lines)
    light_dirs = file_system.find_light_dirs(max_size=100000)
    deleted_dir = file_system.find_directory_to_delete(required_space=30000000)
    return sum(d.size for d in light_dirs), deleted_dir.size
