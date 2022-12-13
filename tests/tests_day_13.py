# coding=utf-8
"""Tests for the Day 13: Distress Signal puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_13.tools import DistressSignal, Packet


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        packets = [
            "[1,1,3,1,1]", "[1,1,5,1,1]", "", "[[1],[2,3,4]]", "[[1],4]", "",
            "[9]", "[[8,7,6]]", "", "[[4,4],4,4]", "[[4,4],4,4,4]", "", "[7,7,7,7]",
            "[7,7,7]", "", "[]", "[3]", "", "[[[]]]", "[[]]", "",
            "[1,[2,[3,[4,[5,6,7]]]],8,9]", "[1,[2,[3,[4,[5,6,0]]]],8,9]"]
        self.signal = DistressSignal.from_strings(signal_lines=packets)

    def test_1st_pair_is_ordered(self):
        """The 1st pair of Packet objects is stored in the RIGHT order."""
        pair = self.signal.pairs[0]
        self.assertTrue(pair[0] < pair[1])

    def test_2nd_pair_is_ordered(self):
        """The 2nd pair of Packet objects is stored in the RIGHT order."""
        pair = self.signal.pairs[1]
        self.assertTrue(pair[0] < pair[1])

    def test_3rd_pair_is_ordered(self):
        """The 3rd pair of Packet objects is stored in the WRONG order."""
        pair = self.signal.pairs[2]
        self.assertFalse(pair[0] < pair[1])

    def test_4th_pair_is_ordered(self):
        """The 4th pair of Packet objects is stored in the RIGHT order."""
        pair = self.signal.pairs[3]
        self.assertTrue(pair[0] < pair[1])

    def test_5th_pair_is_ordered(self):
        """The 5th pair of Packet objects is stored in the WRONG order."""
        pair = self.signal.pairs[4]
        self.assertFalse(pair[0] < pair[1])

    def test_6th_pair_is_ordered(self):
        """The 6th pair of Packet objects is stored in the RIGHT order."""
        pair = self.signal.pairs[5]
        self.assertTrue(pair[0] < pair[1])

    def test_7th_pair_is_ordered(self):
        """The 7th pair of Packet objects is stored in the WRONG order."""
        pair = self.signal.pairs[6]
        self.assertFalse(pair[0] < pair[1])

    def test_8th_pair_is_ordered(self):
        """The 8th pair of Packet objects is stored in the WRONG order."""
        pair = self.signal.pairs[7]
        self.assertFalse(pair[0] < pair[1])

    def test_sum_of_pairs_in_right_order(self):
        """The indexes of the Packet pairs that are in the right order sum 13."""
        self.assertEqual(13, self.signal.ordered_pairs_sum)

    def test_sorted_packets(self):
        """The sorted list of packets in the signal must match the expected list."""
        expected_values = [
            "[]", "[[]]", "[[[]]]", "[1,1,3,1,1]", "[1,1,5,1,1]", "[[1],[2,3,4]]",
            "[1,[2,[3,[4,[5,6,0]]]],8,9]", "[1,[2,[3,[4,[5,6,7]]]],8,9]", "[[1],4]",
            "[[2]]", "[3]", "[[4,4],4,4]", "[[4,4],4,4,4]", "[[6]]", "[7,7,7]",
            "[7,7,7,7]", "[[8,7,6]]", "[9]"]
        sorted_values = [packet.value for packet in self.signal.sorted_packets]
        self.assertListEqual(expected_values, sorted_values)

    def test_decoder_key(self):
        """The decoder key for this DistressSignal is 140."""
        self.assertEqual(140, self.signal.decoder_key)

    def test_decoder_key_fast(self):
        """The decoder key for this DistressSignal is 140."""
        self.assertEqual(140, self.signal.decoder_key_fast)


class CustomTests(unittest.TestCase):
    def test_pair_order_1(self):
        """This pair of Packet objects is stored in the WRONG order."""
        packet_1 = Packet(value="[[7,6],[],[[5],0,10,[7,9,[7],0]]]")
        packet_2 = Packet(value="[[[[6,9,0]],0]]")
        self.assertFalse(packet_1 < packet_2)

    def test_pair_order_2(self):
        """This pair of Packet objects is stored in the RIGHT order."""
        packet_1 = Packet(value="[[6,6],[],[[5],0,10,[7,9,[7],0]]]")
        packet_2 = Packet(value="[[[[6,9,0]],0]]")
        self.assertTrue(packet_1 < packet_2)

    def test_pair_order_3(self):
        """This pair of Packet objects is stored in the RIGHT order."""
        packet_1 = Packet(value="[[[1],3],[],[]]")
        packet_2 = Packet(value="[[10,[[2,2],[6],[8],5]],[8,4]]")
        self.assertTrue(packet_1 < packet_2)
