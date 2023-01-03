# coding=utf-8
"""Tests for the Day 21: Monkey Math puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_21.tools import MonkeyGang, FixedMonkeyGang


# noinspection SpellCheckingInspection
class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.monkeys = ["root: pppw + sjmn", "dbpl: 5", "cczh: sllz + lgvd", "zczc: 2",
                        "ptdq: humn - dvpt", "dvpt: 3", "lfqf: 4", "humn: 5", "ljgn: 2",
                        "sjmn: drzm * dbpl", "sllz: 4", "pppw: cczh / lfqf",
                        "lgvd: ljgn * ptdq", "drzm: hmdt - zczc", "hmdt: 32"]

    def test_number_of_monkey_hmdt(self):
        """This Monkey yells the number 32."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(32, gang["hmdt"])

    def test_number_of_monkey_zczc(self):
        """This Monkey yells the number 2."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(2, gang["zczc"])

    def test_number_of_monkey_drzm(self):
        """This Monkey yells the number 30."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(30, gang["drzm"])

    def test_number_of_monkey_dbpl(self):
        """This Monkey yells the number 5."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(5, gang["dbpl"])

    def test_number_of_monkey_sjmn(self):
        """This Monkey yells the number 150."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(150, gang["sjmn"])

    def test_number_of_monkey_root(self):
        """This Monkey yells the number 152."""
        gang = MonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(152, gang["root"])

    def test_number_of_monkey_root_in_fixed_gang(self):
        """After fixing the mistranslation, this Monkey yells the number 0."""
        gang = FixedMonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(0, gang["root"])

    def test_your_number_in_fixed_gang(self):
        """After fixing the mistranslation, you should yell the number 301."""
        gang = FixedMonkeyGang.from_strings(strings=self.monkeys)
        self.assertEqual(301, gang["humn"])
