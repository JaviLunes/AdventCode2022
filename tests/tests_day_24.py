# coding=utf-8
"""Tests for the Day 24: Blizzard Basin puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_24.tools import Valley
from aoc2022.day_24.visualization import plot_expedition


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        map_lines = [
            "#.######", "#>>.<^<#", "#.<..<<#", "#>v.><>#", "#<^v^^>#", "######.#"]
        self.valley = Valley.from_strings(strings=map_lines)

    def test_plot_expedition_after_each_instant(self):
        """Plot the Expedition at each instant during its travel towards the goal."""
        expedition = self.valley.plan_travel_to_goal(t=0)
        for t in range(expedition.t + 1):
            fig = plot_expedition(valley=self.valley, expedition=expedition, t=t)
            self.assertIsInstance(fig, Figure)
            fig.show()
            plt.close(fig)

    def test_fastest_way_to_goal(self):
        """The fastest way to reach the goal avoiding the blizzards takes 18 minutes."""
        expedition = self.valley.plan_travel_to_goal(t=0)
        self.assertEqual(18, expedition.t)

    def test_fastest_way_back_to_start(self):
        """The fastest way to reach back the start from the goal takes 23 minutes."""
        expedition = self.valley.plan_travel_to_start(t=18)
        self.assertEqual(23, expedition.t - 18)

    def test_fastest_way_back_to_goal(self):
        """The fastest way to reach back the goal from the start takes 13 minutes."""
        expedition = self.valley.plan_travel_to_goal(t=18 + 23)
        self.assertEqual(13, expedition.t - 18 - 23)

    def test_fastest_way_to_goal_then_start_then_goal_again(self):
        """Those snacks caused the travel across the valley to take 54 minutes!"""
        expedition_1 = self.valley.plan_travel_to_goal(t=0)
        expedition_2 = self.valley.plan_travel_to_start(t=expedition_1.t)
        expedition_3 = self.valley.plan_travel_to_goal(t=expedition_2.t)
        self.assertEqual(54, expedition_3.t)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_24/puzzle_input.txt"
        map_lines = read_puzzle_input(input_file=input_file)
        self.valley = Valley.from_strings(strings=map_lines)

    def test_solution_for_part_1(self):
        """The fastest way to reach the goal avoiding the blizzards takes 332 minutes."""
        expedition = self.valley.plan_travel_to_goal(t=0)
        self.assertEqual(332, expedition.t)

    def test_solution_for_part_2(self):
        """The fastest way to make the extended travel takes 942 minutes."""
        expedition_1 = self.valley.plan_travel_to_goal(t=0)
        expedition_2 = self.valley.plan_travel_to_start(t=expedition_1.t)
        expedition_3 = self.valley.plan_travel_to_goal(t=expedition_2.t)
        self.assertEqual(942, expedition_3.t)
