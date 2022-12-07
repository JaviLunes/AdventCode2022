# coding=utf-8
"""Tests for the Day 7: No Space Left On Device puzzle."""

# Standard library imports:
import unittest

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
        heavyweight_dirs = self.system.find_heavy_dirs(max_size=8381165)
        self.assertListEqual(["/", "d"], [d.name for d in heavyweight_dirs])

    def test_directory_to_delete(self):
        """The best directory to delete when requiring 30000000 of space is 'd'."""
        target_dir = self.system.find_directory_to_delete(required_space=30000000)
        self.assertEqual("d", target_dir.name)
        self.assertEqual(24933642, target_dir.size)
