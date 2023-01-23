# coding=utf-8
"""Tests for the Day 11: Monkey in the Middle puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_11.tools import MonkeyGang

# Set constants:
DATA_PATH = Path(__file__).parent / "data" / "day_11"


class MonkeyTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        notes = read_puzzle_input(input_file=DATA_PATH / "example_notes.txt")
        self.gang = MonkeyGang.from_notes(notes=notes, infuriating=False)

    def test_items_per_monkey_after_1_round(self):
        """Validate the worry levels of the items hold by each Monkey after 1 round."""
        expected = [[20, 23, 27, 26], [2080, 25, 167, 207, 401, 1046], [], []]
        self.gang.do_rounds(rounds=1)
        for monkey, expected_items in zip(self.gang.monkeys, expected):
            with self.subTest(monkey=monkey):
                self.assertListEqual(expected_items, monkey.items)

    def test_items_per_monkey_after_10_rounds(self):
        """Validate the worry levels of the items hold by each Monkey after 10 rounds."""
        expected = [[91, 16, 20, 98], [481, 245, 22, 26, 1092, 30], [], []]
        self.gang.do_rounds(rounds=10)
        for monkey, expected_items in zip(self.gang.monkeys, expected):
            with self.subTest(monkey=monkey):
                self.assertListEqual(expected_items, monkey.items)

    def test_most_active_monkeys_after_20_rounds(self):
        """The Monkeys 3 and 0 were the most active ones after 20 rounds."""
        self.gang.do_rounds(rounds=20)
        monkeys = self.gang.monkeys_per_activity_level
        self.assertEqual(3, monkeys[0].id)
        self.assertEqual(0, monkeys[1].id)

    def test_monkey_business_after_20_rounds(self):
        """The level of Monkey business after 20 rounds was over 9000!"""
        self.gang.do_rounds(rounds=20)
        self.assertEqual(10605, self.gang.monkey_business)


class InfuriatingMonkeyTests(MonkeyTests):
    def setUp(self) -> None:
        """Define objects to be tested."""
        notes = read_puzzle_input(input_file=DATA_PATH / "example_notes.txt")
        self.gang = MonkeyGang.from_notes(notes=notes, infuriating=True)

    def test_items_per_monkey_after_1_round(self):
        """This test makes no sense with InfuriatingMonkey objects."""
        pass

    def test_items_per_monkey_after_10_rounds(self):
        """This test makes no sense with InfuriatingMonkey objects."""
        pass

    def test_monkey_business_after_1_round(self):
        """The level of Monkey business after 1 round is 6 * 4."""
        self.gang.do_rounds(rounds=1)
        self.assertEqual(6 * 4, self.gang.monkey_business)

    def test_monkey_business_after_20_rounds(self):
        """The level of Monkey business after 20 rounds is 103 * 99."""
        self.gang.do_rounds(rounds=20)
        self.assertEqual(103 * 99, self.gang.monkey_business)

    def test_monkey_business_after_1000_rounds(self):
        """The level of Monkey business after 1000 rounds is 5204 * 5192."""
        self.gang.do_rounds(rounds=1000)
        self.assertEqual(5204 * 5192, self.gang.monkey_business)

    def test_monkey_business_after_10000_rounds(self):
        """The level of Monkey business after 10000 rounds is 52166 * 52013."""
        self.gang.do_rounds(rounds=10000)
        self.assertEqual(52166 * 52013, self.gang.monkey_business)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_11/puzzle_input.txt"
        self.notes = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """The level of Monkey business after 20 rounds is 61005."""
        gang = MonkeyGang.from_notes(notes=self.notes, infuriating=False)
        gang.do_rounds(rounds=20)
        self.assertEqual(61005, gang.monkey_business)

    def test_solution_for_part_2(self):
        """The level of Monkey business after 10000 rounds is 20567144694."""
        gang = MonkeyGang.from_notes(notes=self.notes, infuriating=True)
        gang.do_rounds(rounds=10000)
        self.assertEqual(20567144694, gang.monkey_business)
