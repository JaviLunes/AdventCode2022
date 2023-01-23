# coding=utf-8
"""Tests for the Day 5: Supply Stacks puzzle."""

# Standard library imports:
from pathlib import Path
import unittest

# Third party imports:
from aoc_tools import read_puzzle_input

# Local application imports:
from aoc2022.day_5.tools import CrateMover9000, CrateMover9001


class ExampleTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.instructions = [
            "    [D]    ", "[N] [C]    ", "[Z] [M] [P]", " 1   2   3  ", "",
            "move 1 from 2 to 1", "move 3 from 1 to 3", "move 2 from 2 to 1",
            "move 1 from 1 to 2"]

    def test_initial_disposition(self):
        """Validate the crate dispositions before applying any crane movement."""
        stacks = CrateMover9000(crane_instructions=self.instructions)
        self.assertEqual(3, len(stacks.stacks))
        self.assertEqual(["N", "Z"], stacks.stacks[1])
        self.assertEqual(["D", "C", "M"], stacks.stacks[2])
        self.assertEqual(["P"], stacks.stacks[3])

    def test_final_disposition_crate_mover_9000(self):
        """Validate the crate dispositions after applying all crane movements."""
        stacks = CrateMover9000(crane_instructions=self.instructions)
        stacks.rearrange_stacks()
        self.assertEqual(3, len(stacks.stacks))
        self.assertEqual(["C"], stacks.stacks[1])
        self.assertEqual(["M"], stacks.stacks[2])
        self.assertEqual(["Z", "N", "D", "P"], stacks.stacks[3])

    def test_final_top_crates_crate_mover_9000(self):
        """The names of the top crate on each stack form the string 'CMZ'."""
        stacks = CrateMover9000(crane_instructions=self.instructions)
        stacks.rearrange_stacks()
        self.assertEqual("CMZ", stacks.top_crates)

    def test_final_disposition_crate_mover_9001(self):
        """Validate the crate dispositions after applying all crane movements."""
        stacks = CrateMover9001(crane_instructions=self.instructions)
        stacks.rearrange_stacks()
        self.assertEqual(3, len(stacks.stacks))
        self.assertEqual(["M"], stacks.stacks[1])
        self.assertEqual(["C"], stacks.stacks[2])
        self.assertEqual(["D", "N", "Z", "P"], stacks.stacks[3])

    def test_final_top_crates_crate_mover_9001(self):
        """The names of the top crate on each stack form the string 'MCD'."""
        stacks = CrateMover9001(crane_instructions=self.instructions)
        stacks.rearrange_stacks()
        self.assertEqual("MCD", stacks.top_crates)


# noinspection SpellCheckingInspection
class SolutionTests(unittest.TestCase):
    def setUp(self) -> None:
        """Define objects to be tested."""
        input_file = Path(__file__).parents[1] / "src/aoc2022/day_5/puzzle_input.txt"
        self.instructions = read_puzzle_input(input_file=input_file)

    def test_solution_for_part_1(self):
        """The names of the top crates form the string 'SPFMVDTZT'."""
        crane = CrateMover9000(crane_instructions=self.instructions)
        crane.rearrange_stacks()
        self.assertEqual("SPFMVDTZT", crane.top_crates)

    def test_solution_for_part_2(self):
        """The names of the top crates form the string 'ZFSJBPRFP'."""
        crane = CrateMover9001(crane_instructions=self.instructions)
        crane.rearrange_stacks()
        self.assertEqual("ZFSJBPRFP", crane.top_crates)
