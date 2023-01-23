# coding=utf-8
"""Tests for the Day 20: Grove Positioning System puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_20.tools import CircularList, EncryptedFile, IndexInt


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.encrypted_values_0 = [1, 2, -3, 3, -2, 0, 4]
        self.encrypted_values_1 = [4, 5, 6, 1, 7, 8, 9]
        self.encrypted_values_2 = [4, -2, 5, 6, 7, 8, 9]

    def test_mix_single_value_in_encrypted_values_0(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [2, 1, -3, 3, -2, 0, 4]
        item = IndexInt(value=1, index=1)
        seq = CircularList(*self.encrypted_values_0)
        original_index = seq.index(item)
        new_index = original_index + item.value
        seq.move(index=original_index, new_index=new_index)
        self.assertListEqual(expected, seq.values)

    def test_mix_single_value_in_encrypted_values_1(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [4, 5, 6, 7, 1, 8, 9]
        item = IndexInt(value=1, index=4)
        seq = CircularList(*self.encrypted_values_1)
        original_index = seq.index(item)
        new_index = original_index + item.value
        seq.move(index=original_index, new_index=new_index)
        self.assertListEqual(expected, seq.values)

    def test_mix_single_value_in_encrypted_values_2(self):
        """Validate the result of mixin one single value in an example list."""
        expected = [4, 5, 6, 7, 8, -2, 9]
        item = IndexInt(value=-2, index=5)
        seq = CircularList(*self.encrypted_values_2)
        original_index = seq.index(item)
        new_index = original_index + item.value
        seq.move(index=original_index, new_index=new_index)
        self.assertListEqual(expected, seq.values)

    def test_mix_all_values_in_encrypted_values_0(self):
        """Validate the result of mixin each value in an example list."""
        expected = [-2, 1, 2, -3, 4, 0, 3]
        file = EncryptedFile(*self.encrypted_values_0)
        self.assertListEqual(expected, file.values)

    def test_mix_all_values_in_encrypted_values_0_with_key_and_10_passes(self):
        """Validate applying a key multiplier and mixing all values 10 times."""
        expected = [0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459,
                    811589153]
        file = EncryptedFile(*self.encrypted_values_0, key=811589153, passes=10)
        self.assertListEqual(expected, file.values)

    def test_groove_coordinate_values(self):
        """The 1k-th, 2k-th and 3k-th numbers after value 0 are 4, -3 and 2."""
        strings = map(str, self.encrypted_values_0)
        file = EncryptedFile.from_strings(*strings)
        self.assertEqual(4, file.get_ith_value(i=1000))
        self.assertEqual(-3, file.get_ith_value(i=2000))
        self.assertEqual(2, file.get_ith_value(i=3000))

    def test_groove_coordinates(self):
        """The sum of the 1k-th, 2k-th and 3k-th numbers after value 0 add to 3."""
        strings = map(str, self.encrypted_values_0)
        file = EncryptedFile.from_strings(*strings)
        self.assertEqual(3, file.groove_sum)


class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_20/puzzle_input.txt"
        self.lines = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """The sum of the groove coordinates' values add to 17490."""
        file = EncryptedFile.from_strings(*self.lines)
        self.assertEqual(17490, file.groove_sum)

    def test_solution_for_part_2(self):
        """The sum of groove coordinates, with 10 passes and key, is 1632917375836."""
        file = EncryptedFile.from_strings(*self.lines, key=811589153, passes=10)
        self.assertEqual(1632917375836, file.groove_sum)
