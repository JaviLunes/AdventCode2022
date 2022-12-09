# coding=utf-8
"""Tests for the Day 9: Rope Bridge puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_9.tools import Rope


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.movements_1 = ["R 4", "U 4", "L 3", "D 1", "R 4", "D 1", "L 5", "R 2"]
        self.movements_2 = ["R 5", "U 8", "L 8", "D 3", "R 17", "D 10", "L 25", "U 20"]

    def test_short_rope_doing_short_movements(self):
        """The tail has been in 13 different locations after completing all motions."""
        rope = Rope(nodes=2)
        rope.apply_motions(motions=self.movements_1)
        self.assertEqual(13, len(set(rope.tail_positions)))

    def test_long_rope_doing_short_movements(self):
        """The tail has been in 1 different locations after completing all motions."""
        rope = Rope(nodes=10)
        rope.apply_motions(motions=self.movements_1)
        self.assertEqual(1, len(set(rope.tail_positions)))

    def test_long_rope_doing_long_movements(self):
        """The tail has been in 36 different locations after completing all motions."""
        rope = Rope(nodes=10)
        rope.apply_motions(motions=self.movements_2)
        self.assertEqual(36, len(set(rope.tail_positions)))
