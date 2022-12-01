# coding=utf-8
"""Tools used for solving the Day 1: Calorie Counting puzzle."""

# Standard library imports:
from collections.abc import Iterable


class ElfSupplies:
    """Account of calories carried by a single Elf."""
    def __init__(self, number: int, calories: list[int]):
        self.number = number
        self.calories = [*calories]

    def __repr__(self) -> str:
        return f"Elf #{self.number}: {sum(self.calories)}"

    @property
    def total_calories(self) -> int:
        """Provide the total sum of calories carried by this elf."""
        return sum(self.calories)


class ExpeditionSupplies:
    """Account of calories carried by all Elves in the expedition."""
    def __init__(self, calories_list: list[str]):
        self.elves = list(self._parse_list(calories_list=calories_list))

    @staticmethod
    def _parse_list(calories_list: list[str]) -> Iterable[ElfSupplies]:
        """Split a list of string annotations into accounts of calories for each Elf."""
        account = "|".join(calories_list).replace("||", "@")
        for i, calories_str in enumerate(account.split("@")):
            yield ElfSupplies(number=i, calories=list(map(int, calories_str.split("|"))))

    @property
    def calories_per_elf(self) -> list[int]:
        """Provide a list with the total calories carried by each elf."""
        return [elf.total_calories for elf in self.elves]

    def sort_elves_by_calories(self) -> list[ElfSupplies]:
        """Provide the list of ElfSupplies, sorted in decreasing total calories."""
        return sorted(self.elves, key=lambda elf: elf.total_calories, reverse=True)
