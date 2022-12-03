# coding=utf-8
"""Tools used for solving the Day 3: Rucksack Reorganization puzzle."""

# Standard library import:
from string import ascii_letters


class RuckSack:
    """Container with two compartments used for carrying the supplies of one Elf."""
    def __init__(self, items: str):
        self.left, self.right = self._divide_items(items=items)

    def __repr__(self) -> str:
        return self.left + self.right

    @property
    def items(self) -> set[str]:
        """Provide the set of unique items stored in this RuckSack."""
        return set(self.left + self.right)

    @staticmethod
    def _divide_items(items: str) -> tuple[str, str]:
        """Separate all items into two halves."""
        sep_idx = len(items) // 2
        return items[:sep_idx], items[sep_idx:]

    @property
    def duplicated_item(self) -> str:
        """Provide the ONLY item stored in both left and right compartments."""
        return list(set(self.left) & set(self.right))[0]


class RuckSackPack:
    """Sequence of the RuckSack of each Elf in the expedition."""
    def __init__(self, items_list: list[str]):
        self.sacks = [RuckSack(items=items) for items in items_list]
        self._priority_map = {char: i + 1 for i, char in enumerate(ascii_letters)}

    @property
    def duplicated_items(self) -> list[str]:
        """Provide the duplicated item in each stored RuckSack."""
        return [sack.duplicated_item for sack in self.sacks]

    @property
    def duplicated_priorities(self) -> list[int]:
        """Provide the priority for the duplicated item in each stored RackSack."""
        return [self._priority_map[item] for item in self.duplicated_items]

    @property
    def total_duplicated_priority(self) -> int:
        """Provide the sum of priorities for duplicated items in this RuckSackPack."""
        return sum(self.duplicated_priorities)

    @property
    def group_badges(self) -> list[str]:
        """Provide the group badge for each group of three RuckSack objects stored."""
        groups = list(zip(self.sacks[::3], self.sacks[1::3], self.sacks[2::3]))
        return [list(a.items & b.items & c.items)[0] for a, b, c in groups]

    @property
    def total_badge_priorities(self) -> int:
        """Provide the sum of badge priorities for the groups in this RuckSackPack."""
        return sum(self._priority_map[badge] for badge in self.group_badges)
