# coding=utf-8
"""Tests for the Day 2: Day 2: Rock Paper Scissors puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_2.tools import Tournament


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        strategy = ["A Y", "B X", "C Z"]
        self.tournament_1 = Tournament(strategy=strategy, tells_your_draw=True)
        self.tournament_2 = Tournament(strategy=strategy, tells_your_draw=False)

    def test_tournament_1_score(self):
        """The expected total score for following the strategy guide is 15."""
        self.assertEqual(15, self.tournament_1.total_score)

    def test_tournament_2_score(self):
        """The expected total score for following the strategy guide is 12."""
        self.assertEqual(12, self.tournament_2.total_score)
