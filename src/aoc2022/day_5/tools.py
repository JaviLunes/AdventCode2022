# coding=utf-8
"""Tools used for solving the Day 5: Supply Stacks puzzle."""

# Standard library imports:
import abc
from collections import namedtuple


Movement = namedtuple("Movement", ["crates", "from_", "to_"])


class Crane(metaclass=abc.ABCMeta):
    """Giant cargo crane used by Elves to move crates between stacks."""
    def __init__(self, crane_instructions: list[str]):
        stacks, movements = "|".join(crane_instructions).replace("||", "@").split("@")
        self.stacks = self._process_stacks_drawing(drawing=stacks.split("|"))
        self.movements = self._process_crane_movements(movements=movements.split("|"))

    @staticmethod
    def _process_stacks_drawing(drawing: list[str]) -> dict[int, list[str]]:
        """Parse crane instruction lines relative to the starting crate disposition."""
        stacks = {int(key): [] for key in drawing[-1].split()}
        for k, key in enumerate(stacks.keys()):
            start = 4 * k + 1
            crates = [line[start:start + 1] for line in drawing[:-1]]
            stacks[key].extend([crate for crate in crates if crate not in ["", " "]])
        return stacks

    @staticmethod
    def _process_crane_movements(movements: list[str]) -> list[Movement]:
        """Parse crane instruction lines relative to moving crates."""
        return [Movement(*(map(int, move.split(" ")[1:6:2]))) for move in movements]

    def rearrange_stacks(self):
        """Apply all crate movements stored in the Crane's memory."""
        [self._apply_first_movement() for _ in range(len(self.movements))]

    @abc.abstractmethod
    def _apply_first_movement(self):
        """Apply the first movement in the Crane's memory, and remove it."""
        pass

    @property
    def top_crates(self) -> str:
        """Provide the combination of names for the crates on top of each stack."""
        return "".join(stack[0] for stack in self.stacks.values())


class CrateMover9000(Crane):
    """Basic Crane, only able to move crates one at a time."""
    def _apply_first_movement(self):
        """Apply the first movement in the Crane's memory, and remove it."""
        n, from_, to_ = self.movements.pop(0)
        self.stacks[to_] = self.stacks[from_][:n][::-1] + self.stacks[to_]
        self.stacks[from_] = self.stacks[from_][n:]


class CrateMover9001(Crane):
    """Improved version with extra cup holder and able to move multiple crates at once"""
    def _apply_first_movement(self):
        """Apply the first movement in the Crane's memory, and remove it."""
        n, from_, to_ = self.movements.pop(0)
        self.stacks[to_] = self.stacks[from_][:n] + self.stacks[to_]
        self.stacks[from_] = self.stacks[from_][n:]
