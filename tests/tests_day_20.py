# coding=utf-8
"""Tests for the Day 20: Grove Positioning System puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_20.tools import EncryptedFile, MixSeq


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.encrypted_values_0 = [1, 2, -3, 3, -2, 0, 4]
        self.encrypted_values_1 = [4, 5, 6, 1, 7, 8, 9]
        self.encrypted_values_2 = [4, -2, 5, 6, 7, 8, 9]

    def test_mix_single_value_in_encrypted_values_0(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [2, 1, -3, 3, -2, 0, 4]
        mixed = MixSeq(*self.encrypted_values_0)
        self.assertListEqual(expected, mixed.mix_values(order_seq=[1]))

    def test_mix_single_value_in_encrypted_values_1(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [4, 5, 6, 7, 1, 8, 9]
        mixed = MixSeq(*self.encrypted_values_1)
        self.assertListEqual(expected, mixed.mix_values(order_seq=[1]))

    def test_mix_single_value_in_encrypted_values_2(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [4, 5, 6, 7, 8, -2, 9]
        mixed = MixSeq(*self.encrypted_values_2)
        self.assertListEqual(expected, mixed.mix_values(order_seq=[-2]))

    def test_mix_all_values_in_encrypted_values_0(self):
        """Validate the result of mixin each value in an example list."""
        expected = [-2, 1, 2, -3, 4, 0, 3]
        values = self.encrypted_values_0
        mixed = MixSeq(*values)
        self.assertListEqual(expected, mixed.mix_values(order_seq=values))

    def test_groove_coordinate_values(self):
        """The 1k-th, 2k-th and 3k-th numbers after value 0 are 4, -3 and 2."""
        encrypted_strings = list(map(str, self.encrypted_values_0))
        file = EncryptedFile(encrypted_strings=encrypted_strings)
        self.assertEqual(4, file.get_ith_value(i=1000))
        self.assertEqual(-3, file.get_ith_value(i=2000))
        self.assertEqual(2, file.get_ith_value(i=3000))

    def test_groove_coordinates(self):
        """The sum of the 1k-th, 2k-th and 3k-th numbers after value 0 add to 3."""
        encrypted_strings = list(map(str, self.encrypted_values_0))
        file = EncryptedFile(encrypted_strings=encrypted_strings)
        self.assertEqual(3, file.groove_sum)
