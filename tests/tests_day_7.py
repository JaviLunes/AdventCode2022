# coding=utf-8
"""Tests for the Day 7: No Space Left On Device puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_7.tools import FileSystem


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        terminal_output = [
            "$ cd /", "$ ls", "dir a", "14848514 b.txt", "8504156 c.dat", "dir d",
            "$ cd a", "$ ls", "dir e", "29116 f", "2557 g", "62596 h.lst", "$ cd e",
            "$ ls", "584 i", "$ cd ..", "$ cd ..", "$ cd d", "$ ls", "4060174 j",
            "8033020 d.log", "5626152 d.ext", "7214296 k"]
        self.system = FileSystem.from_terminal_output(output=terminal_output)

    def test_lightweight_directories(self):
        """The directories with size equal or less than 100000 are 'a' and 'e'."""
        lightweight_dirs = self.system.find_light_dirs(max_size=100000)
        self.assertListEqual(["a", "e"], [d.name for d in lightweight_dirs])
        self.assertEqual(95437, sum([d.size for d in lightweight_dirs]))

    def test_heavyweight_directories(self):
        """The directories with size equal or more than 8381165 are '/' and 'd'."""
        heavyweight_dirs = self.system.find_heavy_dirs(min_size=8381165)
        self.assertListEqual(["/", "d"], [d.name for d in heavyweight_dirs])

    def test_directory_to_delete(self):
        """The best directory to delete when requiring 30000000 of space is 'd'."""
        target_dir = self.system.find_directory_to_delete(required_space=30000000)
        self.assertEqual("d", target_dir.name)
        self.assertEqual(24933642, target_dir.size)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_7/puzzle_input.txt"
        lines = read_puzzle_input(input_file=input_file)
        self.file_system = FileSystem.from_terminal_output(output=lines)

    def test_solution_for_part_1(self):
        """The total size of the light-weight directories is 1390824."""
        light_dirs = self.file_system.find_light_dirs(max_size=100000)
        self.assertEqual(1390824, sum(d.size for d in light_dirs))

    def test_solution_for_part_2(self):
        """The best directory to delete weights 7490863."""
        deleted_dir = self.file_system.find_directory_to_delete(required_space=30000000)
        self.assertEqual(7490863, deleted_dir.size)
