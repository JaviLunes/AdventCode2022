# coding=utf-8
"""Tests for the Day 13: Distress Signal puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_13.tools import DistressSignal, Pair


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        signal_lines = [
            "[1,1,3,1,1]", "[1,1,5,1,1]", "", "[[1],[2,3,4]]", "[[1],4]", "",
            "[9]", "[[8,7,6]]", "", "[[4,4],4,4]", "[[4,4],4,4,4]", "", "[7,7,7,7]",
            "[7,7,7]", "", "[]", "[3]", "", "[[[]]]", "[[]]", "",
            "[1,[2,[3,[4,[5,6,7]]]],8,9]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"]
        self.signal = DistressSignal.from_signal_lines(signal_lines=signal_lines)

    def test_1st_pair_is_ordered(self):
        """The first Pair of packets has its inputs in the RIGHT order."""
        self.assertTrue(self.signal.pairs[0].ordered)

    def test_2nd_pair_is_ordered(self):
        """The 2nd Pair of packets has its inputs in the RIGHT order."""
        self.assertTrue(self.signal.pairs[1].ordered)

    def test_3rd_pair_is_ordered(self):
        """The 3rd Pair of packets has its inputs in the WRONG order."""
        self.assertFalse(self.signal.pairs[2].ordered)

    def test_4th_pair_is_ordered(self):
        """The 4th Pair of packets has its inputs in the RIGHT order."""
        self.assertTrue(self.signal.pairs[3].ordered)

    def test_5th_pair_is_ordered(self):
        """The 5th Pair of packets has its inputs in the WRONG order."""
        self.assertFalse(self.signal.pairs[4].ordered)

    def test_6th_pair_is_ordered(self):
        """The 6th Pair of packets has its inputs in the RIGHT order."""
        self.assertTrue(self.signal.pairs[5].ordered)

    def test_7th_pair_is_ordered(self):
        """The 7th Pair of packets has its inputs in the WRONG order."""
        self.assertFalse(self.signal.pairs[6].ordered)

    def test_8th_pair_is_ordered(self):
        """The 8th Pair of packets has its inputs in the WRONG order."""
        self.assertFalse(self.signal.pairs[7].ordered)

    def test_sum_of_pairs_in_right_order(self):
        """The indexes of the Packet pairs that are in the right order sum 13."""
        self.assertEqual(13, self.signal.ordered_pairs_sum)


class CustomTests(unittest.TestCase):
    def test_pair_order_1(self):
        """This Pair of packets has its inputs in the WRONG order."""
        packet_1 = "[[7,6],[],[[5],0,10,[7,9,[7],0]]]"
        packet_2 = "[[[[6,9,0]],0]]"
        pair = Pair.from_string_packets(packet_left=packet_1, packet_right=packet_2)
        self.assertFalse(pair.ordered)

    def test_pair_order_2(self):
        """This Pair of packets has its inputs in the RIGHT order."""
        packet_1 = "[[6,6],[],[[5],0,10,[7,9,[7],0]]]"
        packet_2 = "[[[[6,9,0]],0]]"
        pair = Pair.from_string_packets(packet_left=packet_1, packet_right=packet_2)
        self.assertTrue(pair.ordered)

    def test_pair_order_3(self):
        """This Pair of packets has its inputs in the RIGHT order."""
        packet_1 = "[[[1],3],[],[]]"
        packet_2 = "[[10,[[2,2],[6],[8],5]],[8,4]]"
        pair = Pair.from_string_packets(packet_left=packet_1, packet_right=packet_2)
        self.assertTrue(pair.ordered)
