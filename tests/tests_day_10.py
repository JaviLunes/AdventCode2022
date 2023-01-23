# coding=utf-8
"""Tests for the Day 10: Cathode-Ray Tube puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_10.tools import CPURegister, CRTScreen

# Set constants:
DATA_PATH = Path(__file__).parent / "data" / "day_10"


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        # noinspection SpellCheckingInspection
        small_program = ["noop", "addx 3", "addx -5"]
        large_program = read_puzzle_input(
            input_file=DATA_PATH / "example_program_large.txt")
        self.register_small = CPURegister(program=small_program)
        self.register_large = CPURegister(program=large_program)
        self.screen = CRTScreen(register=self.register_large)

    def test_small_program_x_at_1st_cycle_start(self):
        """At the start of the 1st cycle, the X value is 1."""
        self.assertEqual(1, self.register_small.xs[1])

    def test_small_program_x_at_2nd_cycle_start(self):
        """At the start of the 2nd cycle, the X value is 1."""
        self.assertEqual(1, self.register_small.xs[2])

    def test_small_program_x_at_3rd_cycle_start(self):
        """At the start of the 3rd cycle, the X value is 1."""
        self.assertEqual(1, self.register_small.xs[3])

    def test_small_program_x_at_4th_cycle_start(self):
        """At the start of the 4th cycle, the X value is 4."""
        self.assertEqual(4, self.register_small.xs[4])

    def test_small_program_x_at_5th_cycle_start(self):
        """At the start of the 5th cycle, the X value is 4."""
        self.assertEqual(4, self.register_small.xs[5])

    def test_small_program_x_at_6th_cycle_start(self):
        """At the start of the 6th cycle, the X value is -1."""
        self.assertEqual(-1, self.register_small.xs[6])

    def test_large_program_signal_strength_at_20th_cycle(self):
        """During the 20th cycle, the signal strength is 420."""
        self.assertEqual(420, self.register_large.signal_strength[20])

    def test_large_program_signal_strength_at_60th_cycle(self):
        """During the 60th cycle, the signal strength is 1140."""
        self.assertEqual(1140, self.register_large.signal_strength[60])

    def test_large_program_signal_strength_at_100th_cycle(self):
        """During the 100th cycle, the signal strength is 1800."""
        self.assertEqual(1800, self.register_large.signal_strength[100])

    def test_large_program_signal_strength_at_140th_cycle(self):
        """During the 140th cycle, the signal strength is 2940."""
        self.assertEqual(2940, self.register_large.signal_strength[140])

    def test_large_program_signal_strength_at_180th_cycle(self):
        """During the 180th cycle, the signal strength is 2880."""
        self.assertEqual(2880, self.register_large.signal_strength[180])

    def test_large_program_signal_strength_at_220th_cycle(self):
        """During the 220th cycle, the signal strength is 3960."""
        self.assertEqual(3960, self.register_large.signal_strength[220])

    def test_draw_1st_screen_line(self):
        """The 1st line printed at the CRT screen must match the expected value."""
        expected_print = "##..##..##..##..##..##..##..##..##..##.."
        self.assertEqual(expected_print, self.screen.pixels[0])

    def test_draw_2nd_screen_line(self):
        """The 2nd line printed at the CRT screen must match the expected value."""
        expected_print = "###...###...###...###...###...###...###."
        self.assertEqual(expected_print, self.screen.pixels[1])

    def test_draw_3rd_screen_line(self):
        """The 3rd line printed at the CRT screen must match the expected value."""
        expected_print = "####....####....####....####....####...."
        self.assertEqual(expected_print, self.screen.pixels[2])

    def test_draw_4th_screen_line(self):
        """The 4th line printed at the CRT screen must match the expected value."""
        expected_print = "#####.....#####.....#####.....#####....."
        self.assertEqual(expected_print, self.screen.pixels[3])

    def test_draw_5th_screen_line(self):
        """The 5th line printed at the CRT screen must match the expected value."""
        expected_print = "######......######......######......####"
        self.assertEqual(expected_print, self.screen.pixels[4])

    def test_draw_6th_screen_line(self):
        """The 6th line printed at the CRT screen must match the expected value."""
        expected_print = "#######.......#######.......#######....."
        self.assertEqual(expected_print, self.screen.pixels[5])


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_10/puzzle_input.txt"
        program = read_puzzle_input(input_file=input_file)
        self.register = CPURegister(program=program)
        self.screen = CRTScreen(register=self.register)

    def test_solution_for_part_1(self):
        """The sum of signals' strengths at the 6 target cycles is 14360."""
        self.assertEqual(14360, self.register.significant_strength)

    # noinspection SpellCheckingInspection
    def test_solution_for_part_2(self):
        """The eight capital letters printed on the CRT screen are 'BGKAEREZ'."""
        self.assertEqual("BGKAEREZ", self.screen.characters)
