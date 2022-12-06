# coding=utf-8
"""Tests for the Day 6: Tuning Trouble puzzle."""

# Standard library imports:
import unittest

# Local application imports:
from aoc2022.day_6.tools import StreamDecoder


class ExampleTests(unittest.TestCase):
    # noinspection SpellCheckingInspection
    def setUp(self) -> None:
        """Define objects to be tested."""
        self.stream_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
        self.stream_2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
        self.stream_3 = "nppdvjthqldpwncqszvftbrmjlhg"
        self.stream_4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
        self.stream_5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"

    def test_characters_before_packet_1(self):
        """The first packet starts at character position 7."""
        decoder = StreamDecoder(datastream=self.stream_1)
        self.assertEqual(7, decoder.first_packet_start)

    def test_characters_before_packet_2(self):
        """The first packet starts at character position 5."""
        decoder = StreamDecoder(datastream=self.stream_2)
        self.assertEqual(5, decoder.first_packet_start)

    def test_characters_before_packet_3(self):
        """The first packet starts at character position 6."""
        decoder = StreamDecoder(datastream=self.stream_3)
        self.assertEqual(6, decoder.first_packet_start)

    def test_characters_before_packet_4(self):
        """The first packet starts at character position 10."""
        decoder = StreamDecoder(datastream=self.stream_4)
        self.assertEqual(10, decoder.first_packet_start)

    def test_characters_before_packet_5(self):
        """The first packet starts at character position 11."""
        decoder = StreamDecoder(datastream=self.stream_5)
        self.assertEqual(11, decoder.first_packet_start)

    def test_characters_before_message_1(self):
        """The first message starts at character position 19."""
        decoder = StreamDecoder(datastream=self.stream_1)
        self.assertEqual(19, decoder.first_message_start)

    def test_characters_before_message_2(self):
        """The first message starts at character position 23."""
        decoder = StreamDecoder(datastream=self.stream_2)
        self.assertEqual(23, decoder.first_message_start)

    def test_characters_before_message_3(self):
        """The first message starts at character position 23."""
        decoder = StreamDecoder(datastream=self.stream_3)
        self.assertEqual(23, decoder.first_message_start)

    def test_characters_before_message_4(self):
        """The first message starts at character position 29."""
        decoder = StreamDecoder(datastream=self.stream_4)
        self.assertEqual(29, decoder.first_message_start)

    def test_characters_before_message_5(self):
        """The first message starts at character position 26."""
        decoder = StreamDecoder(datastream=self.stream_5)
        self.assertEqual(26, decoder.first_message_start)
