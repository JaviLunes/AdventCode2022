# coding=utf-8
"""Tools used for solving the Day 13: Distress Signal puzzle."""


class Packet:
    """Unit of data forming a distress signal."""
    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return self.value


class Pair:
    """Group of two Packet objects."""
    def __init__(self, packet_left: Packet, packet_right: Packet):
        self._left = packet_left
        self._right = packet_right

    @property
    def ordered(self) -> bool:
        """Check if the two packets of this Pair are properly ordered."""
        return self._is_ordered(left=self._left.value, right=self._right.value)

    def _is_ordered(self, left: str, right: str) -> bool:
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

    @classmethod
    def from_string_packets(cls, packet_left: str, packet_right: str) -> "Pair":
        """Create a new Pair from the string representations of two Packet objects."""
        return cls(packet_left=Packet(value=packet_left),
                   packet_right=Packet(value=packet_right))


class DistressSignal:
    """Sequence of Packet objects composing a mysterious communication."""
    def __init__(self, packet_pairs: list[Pair]):
        self.pairs = packet_pairs

    @property
    def ordered_pairs_sum(self) -> int:
        """Sum of indexes of the stored Pair objects that are ordered."""
        return sum(i + 1 for i, pair in enumerate(self.pairs) if pair.ordered)

    @classmethod
    def from_signal_lines(cls, signal_lines: list[str]) -> "DistressSignal":
        """Create a new DistressSignal from string rows representing pairs of packets."""
        pairs_lines = "|".join(signal_lines).split("||")
        pairs = [Pair.from_string_packets(*s.split("|")) for s in pairs_lines]
        return cls(packet_pairs=pairs)
