# coding=utf-8
"""Tools used for solving the Day 20: Grove Positioning System puzzle."""

# Standard library imports:
from typing import Any, Union


class IndexInt:
    """Wrapper around an integer value that stores its index in a sequence."""
    __slots__ = ["value", "index"]

    def __init__(self, value: int, index: int):
        self.value = value
        self.index = index

    def __eq__(self, other: Union["IndexInt", int]) -> bool:
        if isinstance(other, IndexInt):
            return self.value == other.value and self.index == other.index
        return self.value == other

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return repr(self.value)


class CircularList:
    """Wrapper around a list that allows for moving its items in a circular way."""
    def __init__(self, *items: Any):
        self._values = list(items)
        self._n = len(items)

    def __getitem__(self, index: int) -> Any:
        return self._values[index]

    @property
    def values(self) -> list[Any]:
        """Provide a shallow copy of the internal list of this CircularList."""
        return [*self._values]

    def index(self, item: Any) -> int:
        """Find the location of an item within the internal list."""
        return self._values.index(item)

    def move(self, index: int, new_index: int):
        """Remove the item at the given index and insert it at the new index."""
        index = index % self._n
        new_index = new_index % (self._n - 1)
        item = self._values.pop(index)
        self._values.insert(new_index, item)


class EncryptedFile:
    """File containing the encrypted coordinates of the star fruit grove."""
    def __init__(self, *values: int, key: int = 1, passes: int = 1):
        indexed_values = [IndexInt(value=v * key, index=i) for i, v in enumerate(values)]
        self.values = self._decrypt(values=indexed_values, passes=passes)

    @staticmethod
    def _decrypt(values: list[IndexInt], passes: int):
        """Apply 'the mixing' once to all numbers in the provided list of values."""
        seq = CircularList(*values)
        for _ in range(passes):
            for item in values:
                original_index = seq.index(item)
                new_index = original_index + item.value
                seq.move(index=original_index, new_index=new_index)
        return seq.values

    @property
    def groove_sum(self) -> int:
        """Sum of 1000th, 2000th and 3000th main values."""
        a = self.get_ith_value(i=1000)
        b = self.get_ith_value(i=2000)
        c = self.get_ith_value(i=3000)
        return a + b + c

    def get_ith_value(self, i: int) -> int:
        """Read the ith number after the 0 value in the mixed data sequence."""
        idx_0 = self.values.index(0)
        index = (idx_0 + i) % len(self.values)
        return self.values[index].value

    @classmethod
    def from_strings(cls, *strings: str, key: int = 1, passes: int = 1):
        """Create a new EncryptedFile from string values, instead of integer values."""
        return cls(*map(int, strings), key=key, passes=passes)
