# coding=utf-8
"""Tests for the Day 2: Day 2: Rock Paper Scissors puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

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


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_2/puzzle_input.txt"
        self.strategy = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """The expected total score for following the strategy guide is 14297."""
        tournament = Tournament(strategy=self.strategy, tells_your_draw=True)
        self.assertEqual(14297, tournament.total_score)

    def test_solution_for_part_2(self):
        """The expected total score for following the strategy guide is 10498."""
        tournament = Tournament(strategy=self.strategy, tells_your_draw=False)
        self.assertEqual(10498, tournament.total_score)
