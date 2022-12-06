# coding=utf-8
"""Tools used for solving the Day 6: Tuning Trouble puzzle."""


class StreamDecoder:
    """Subroutine able to parse datastreams used in Elvish communication systems."""
    def __init__(self, datastream: str):
        self.data = datastream

    @property
    def first_packet_start(self) -> int:
        """Provide the number of characters before the first start-of-packet marker."""
        return self._search_for_marker(distinct_characters=4)

    @property
    def first_message_start(self) -> int:
        """Provide the number of characters before the first start-of-message marker."""
        return self._search_for_marker(distinct_characters=14)

    def _search_for_marker(self, distinct_characters: int) -> int:
        """Return the start position of the first sub-string with n different chars."""
        for i in range(len(self.data) - distinct_characters + 1):
            sub_stream = self.data[i:i + distinct_characters]
            if len(set(sub_stream)) == distinct_characters:
                return i + distinct_characters
        raise ValueError
