# coding=utf-8
"""Tests for the Day 16: Proboscidea Volcanium puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_16.tools import ValveSim, TunnelNetwork


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.scan_output = [
            "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
            "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
            "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
            "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
            "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
            "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
            "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
            "Valve HH has flow rate=22; tunnel leads to valve GG",
            "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
            "Valve JJ has flow rate=21; tunnel leads to valve II"]
        self.network = TunnelNetwork.from_scan_report(scan_report=self.scan_output)

    def test_travel_and_operation_times(self):
        """Validate the total time required for reaching a Valve."""
        self.assertEqual(0, self.network.get_travel(from_="AA", to_="AA"))
        self.assertEqual(2, self.network.get_travel(from_="AA", to_="JJ"))
        self.assertEqual(3, self.network.get_travel(from_="GG", to_="DD"))

    def test_pressure_of_perfect_plan(self):
        """The total pressure released by the best possible opening plan is 1651."""
        sim = ValveSim.from_scan_report(scan_report=self.scan_output, total_time=30)
        self.assertEqual(1651, sim.find_max_release())

    def test_pressure_of_perfect_plan_with_less_time(self):
        """The total pressure released by the best possible opening plan is 1651."""
        sim = ValveSim.from_scan_report(scan_report=self.scan_output, total_time=22)
        self.assertEqual(1007, sim.find_max_release())

    def test_pressure_of_perfect_plan_with_help(self):
        """The total pressure released by the best possible opening plan is 1707."""
        sim = ValveSim.from_scan_report(scan_report=self.scan_output, total_time=26)
        self.assertEqual(1707, sim.find_max_release_with_help())


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_16/puzzle_input.txt"
        self.scan_output = read_puzzle_input(input_file=input_file)
        self.network = TunnelNetwork.from_scan_report(scan_report=self.scan_output)

    def test_solution_for_part_1(self):
        """The most pressure releasable in 30 minutes is 2124."""
        sim = ValveSim.from_scan_report(scan_report=self.scan_output, total_time=30)
        self.assertEqual(2124, sim.find_max_release())

    def test_solution_for_part_2(self):
        """The most pressure releasable in 26 minutes with help is 2775."""
        sim = ValveSim.from_scan_report(scan_report=self.scan_output, total_time=26)
        self.assertEqual(2775, sim.find_max_release_with_help())
