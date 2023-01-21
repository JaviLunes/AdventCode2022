# coding=utf-8
"""Tools used for solving the Day 25: Full of Hot Air puzzle."""

# Set constants:
CHAR_MAP = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
CHAR_MAP_INV = {v: k for k, v in CHAR_MAP.items()}


class SNAFU:
    """Special Numeral-Analogue Fuel Units™, a totally reasonable numeral system!"""
    __slots__ = ["_slots"]

    def __init__(self, slots: list[int]):
        self._slots = self._reduce_slots(slots=slots)

    def __repr__(self) -> str:
        return f"{self.as_string}: {self.as_decimal}"

    def __eq__(self, other: "SNAFU") -> bool:
        return self._slots == other._slots

    def __add__(self, other: "SNAFU"):
        return SNAFU.from_decimal(decimal=self.as_decimal + other.as_decimal)

    @staticmethod
    def _reduce_slots(slots: list[int]) -> list[int]:
        """Make sure all slot values are lower than 2."""
        slots = slots + [0]
        while any(value > 2 for value in slots):
            for i, value in enumerate(slots):
                if value > 2:
                    slots[i] = value - 5
                    slots[i + 1] += 1
        if slots[-1] == 0:
            slots.pop(-1)
        return slots

    @property
    def as_decimal(self) -> int:
        """The value of this SNAFU number, in decimal-digits format."""
        return sum(value * 5 ** i for i, value in enumerate(self._slots))

    @property
    def as_string(self) -> str:
        """The value of this SNAFU number, in SNAFU-digits string format."""
        return "".join(CHAR_MAP_INV[value] for value in self._slots[::-1])

    @classmethod
    def from_decimal(cls, decimal: int) -> "SNAFU":
        """Create a new SNAFU number from a value in decimal-digits format."""
        if decimal == 0:
            return SNAFU(slots=[0])
        string_inv = ""
        while decimal != 0:
            decimal, char = divmod(decimal, 5)
            string_inv += str(char)
        return SNAFU(slots=list(map(int, string_inv)))

    @classmethod
    def from_string(cls, string: str) -> "SNAFU":
        """Create a new SNAFU number from a string in SNAFU-digits format."""
        return SNAFU(slots=[CHAR_MAP[char] for char in string[::-1]])


ZERO_SNAFU = SNAFU.from_decimal(decimal=0)
