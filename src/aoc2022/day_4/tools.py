# coding=utf-8
"""Tools used for solving the Day 4: Camp Cleanup puzzle."""

# Standard library imports:
from collections.abc import Iterable


class CleanupReviewer:
    """Check for overlaps in section assignments between pairs of Elves."""
    def __init__(self, assignment_pairs: list[str]):
        self.pairs = list(self._process_assignments(pairs=assignment_pairs))

    def _process_assignments(self, pairs: list[str]) -> Iterable[tuple[range, range]]:
        """Transform each pair-of-section-assignments-string into two section ranges."""
        for pair in pairs:
            string_1, string_2 = pair.split(",")
            sections_1 = self._assignment_to_range(string=string_1)
            sections_2 = self._assignment_to_range(string=string_2)
            yield sections_1, sections_2

    @staticmethod
    def _assignment_to_range(string: str) -> range:
        """Build a range of section IDs from the string representation of such range."""
        return (lambda a, b: range(int(a), int(b) + 1))(*string.split("-"))

    @property
    def count_full_overlaps(self) -> int:
        """Provide the count of pairs where one range fully contains the other."""
        return sum([(set(a) <= set(b) or set(b) <= set(a)) for a, b in self.pairs])

    @property
    def count_partial_overlaps(self) -> int:
        """Provide the count of pairs where one range partially contains the other."""
        return sum([bool((set(a) & set(b))) for a, b in self.pairs])
