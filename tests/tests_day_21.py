# coding=utf-8
"""Tests for the Day 21: Monkey Math puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_21.tools import MonkeyGang


# noinspection SpellCheckingInspection
class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        monkeys = ["root: pppw + sjmn", "dbpl: 5", "cczh: sllz + lgvd", "zczc: 2",
                   "ptdq: humn - dvpt", "dvpt: 3", "lfqf: 4", "humn: 5", "ljgn: 2",
                   "sjmn: drzm * dbpl", "sllz: 4", "pppw: cczh / lfqf",
                   "lgvd: ljgn * ptdq", "drzm: hmdt - zczc", "hmdt: 32"]
        self.gang = MonkeyGang.from_strings(strings=monkeys, target_monkey_name="root")

    def test_number_of_monkey_hmdt(self):
        """This Monkey yells the number 32."""
        self.assertEqual(32, self.gang["hmdt"])

    def test_number_of_monkey_zczc(self):
        """This Monkey yells the number 2."""
        self.assertEqual(2, self.gang["zczc"])

    def test_number_of_monkey_drzm(self):
        """This Monkey yells the number 30."""
        self.assertEqual(30, self.gang["drzm"])

    def test_number_of_monkey_dbpl(self):
        """This Monkey yells the number 5."""
        self.assertEqual(5, self.gang["dbpl"])

    def test_number_of_monkey_sjmn(self):
        """This Monkey yells the number 150."""
        self.assertEqual(150, self.gang["sjmn"])

    def test_number_of_monkey_root(self):
        """This Monkey yells the number 152."""
        self.assertEqual(152, self.gang["root"])
