# coding=utf-8
"""Tools used for solving the Day 20: Grove Positioning System puzzle."""

# Standard library imports:
from typing import Union


class MixInt:
    """Wrapper around an integer value that recalls if it has been 'mixed' already."""
    def __init__(self, value, mixed: bool = False):
        self.value = value
        self.mixed = mixed

    def __eq__(self, other: Union[int, "MixInt"]) -> bool:
        if isinstance(other, MixInt):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other: "MixInt") -> bool:
        return self.value < other.value

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return repr(self.value)


class MixSeq:
    """Wrapper around a list of integer values, able to 'mix' them."""
    def __init__(self, *values: int):
        self._values = list(map(MixInt, values))

    @property
    def values(self) -> list[int]:
        """List the values of the MixInt members of this MixSeq."""
        return list(map(int, self._values))

    def mix_values(self, order_seq: list[int]) -> list[int]:
        """Mix all MixInt members of this MixSeq, processing them as in the order seq."""
        for value in order_seq:
            self._mix_value(value=value)
        return self.values

    def _mix_value(self, value: int):
        """Mix the first non-mixed MixInt member matching the provided value."""
        index = self._index(value=value)
        new_index = index + value
        self._pop(index=index)
        self._insert(index=new_index, value=value)

    def _index(self, value: int) -> int:
        """Return the index of the first non-mixed MixInt matching the provided value."""
        i = 0
        while i < len(self._values):
            if self._values[i] == value:
                if not self._values[i].mixed:
                    return i
            i += 1
        raise ValueError

    def _insert(self, index: int, value: int):
        """Insert the provided value as a mixed MixInt before the provided index."""
        index = index % len(self._values)
        self._values.insert(index, MixInt(value=value, mixed=True))

    def _pop(self, index: int) -> int:
        """Delete the MixInt member at the provided index, and return its value."""
        index = index % len(self._values)
        return self._values.pop(index).value


class EncryptedFile:
    """File containing the encrypted coordinates of the star fruit grove."""
    def __init__(self, encrypted_strings: list[str]):
        encrypted_values = list(map(int, encrypted_strings))
        self.values = self._decrypt_data(encrypted_values=encrypted_values)

    @staticmethod
    def _decrypt_data(encrypted_values: list[int]):
        """Apply 'the mixing' once to all numbers in the provided list of values."""
        mix_seq = MixSeq(*encrypted_values)
        return mix_seq.mix_values(order_seq=encrypted_values)

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
        return self.values[index]
