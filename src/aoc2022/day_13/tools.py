# coding=utf-8
"""Tools used for solving the Day 13: Distress Signal puzzle."""

# Standard library imports:
import math


class Packet:
    """Unit of data forming a distress signal."""
    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return self.value

    def __eq__(self, other: "Packet") -> bool:
        return self.value == other.value

    def __lt__(self, other: "Packet") -> bool:
        return self._is_lower(other=other)

    def __le__(self, other) -> bool:
        return self == other or self < other

    def _is_lower(self, other: "Packet") -> bool:
        """Check if the value of this Packet is lower than other Packet's value."""
        left, right = self.value, other.value
        if left == right:
            return False
        while left or right:
            left_char, right_char = left[0], right[0]
            left, right = left[1:], right[1:]
            # Check for more-than-one_digit scalars:
            if left_char.isdecimal():
                left_char, left = self._consume_digits(number=left_char, remain=left)
            if right_char.isdecimal():
                right_char, right = self._consume_digits(number=right_char, remain=right)
            # Ignore if equal scalars or list parts:
            if left_char == right_char:
                continue
            # If different scalars, compare and stop:
            if left_char.isdecimal() and right_char.isdecimal():
                return int(left_char) < int(right_char)
            # If only one exhausted list:
            if left_char == "]":
                return True
            if right_char == "]":
                return False
            # If scalar and list start:
            if left_char == "[" and right_char.isdecimal():  # New list | Scalar.
                right = right_char + "]" + right  # Restore chopped scalar.
                continue
            elif left_char.isdecimal() and right_char == "[":  # Scalar | New list.
                left = left_char + "]" + left  # Restore chopped scalar.
                continue
            else:
                raise ValueError("The code reached an unexpected point.")
        raise ValueError("The code reached an unexpected point.")

    @staticmethod
    def _consume_digits(number: str, remain: str) -> tuple[str, str]:
        """Keep moving chars from remain to current until first non-digit in former."""
        while remain[0].isdecimal():
            number += remain[0]
            remain = remain[1:]
        return number, remain


class DistressSignal:
    """Sequence of Packet objects composing a mysterious communication."""
    def __init__(self, packets: list[Packet]):
        self._packets = packets

    @property
    def pairs(self) -> list[tuple[Packet, Packet]]:
        """Provide all stored Packet objects, grouped in pairs."""
        n = len(self._packets)
        left_slice, right_slice = slice(0, n, 2), slice(1, n, 2)
        return list(zip(self._packets[left_slice], self._packets[right_slice]))

    @property
    def ordered_pairs_sum(self) -> int:
        """Provide the sum of indexes of the stored Pair objects that are ordered."""
        return sum(i + 1 for i, pair in enumerate(self.pairs) if pair[0] < pair[1])

    @property
    def sorted_packets(self) -> list[Packet]:
        """Provide the stored Packet objects, sorted in increasing value order."""
        packets = [*self._packets] + self._get_divider_packets()
        return sorted(packets)

    @staticmethod
    def _get_divider_packets() -> list[Packet]:
        """Provide additional Packet objects required by the distress signal protocol."""
        return [Packet(value="[[2]]"), Packet(value="[[6]]")]

    @property
    def decoder_key(self) -> int:
        """Provide the decoder key for this DistressSignal."""
        sorted_packets = self.sorted_packets
        dividers = self._get_divider_packets()
        return math.prod(sorted_packets.index(divider) + 1 for divider in dividers)

    @property
    def decoder_key_fast(self) -> int:
        """Provide the decoder key for this DistressSigna, faster but less pretty."""
        dividers = self._get_divider_packets()
        lower_than_counts = {divider.value: 0 for divider in dividers}
        for packet in self._packets + dividers:
            for divider in dividers:
                if packet < divider:
                    lower_than_counts[divider.value] += 1
        return math.prod(count + 1 for count in lower_than_counts.values())

    @classmethod
    def from_strings(cls, signal_lines: list[str]) -> "DistressSignal":
        """Create a new DistressSignal from string rows representing Packet objects."""
        packet_lines = "|".join(signal_lines).replace("||", "|").split("|")
        return cls(packets=[Packet(value=line) for line in packet_lines])
