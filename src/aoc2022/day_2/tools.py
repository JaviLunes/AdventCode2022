# coding=utf-8
"""Tools used for solving the Day 2: Day 2: Rock Paper Scissors puzzle."""

# Standard library imports:
from collections.abc import Iterable


class Round:
    """Simulation of a rock-paper-scissors game round between you and a foe."""
    def __init__(self, your_draw: str, foe_draw: str):
        self.you = your_draw
        self.foe = foe_draw

    @classmethod
    def from_foe_and_target(cls, result: str, foe_draw: str):
        """Create a Round from your foe's draw and the desired result for the Round."""
        if result == "X":  # You should lose.
            your_draw = cls._get_counter(draw=cls._get_counter(draw=foe_draw))
        elif result == "Y":  # You should draw.
            your_draw = foe_draw
        else:  # You should win.
            your_draw = cls._get_counter(draw=foe_draw)
        return Round(your_draw=your_draw, foe_draw=foe_draw)

    @property
    def score(self) -> int:
        """Provide your score for this Round."""
        counter_to_foe = self._get_counter(draw=self.foe)
        win_score = 3 if self.foe == self.you else 6 * int(self.you == counter_to_foe)
        shape_score = dict(A=1, B=2, C=3)[self.you]
        return shape_score + win_score

    @staticmethod
    def _get_counter(draw: str) -> str:
        """Return the movement that wins against the provided draw."""
        counter_map = dict(A="B", B="C", C="A")
        return counter_map[draw]


class Tournament:
    """Simulation of multiple rock-paper-scissors game rounds between you and a foe."""
    def __init__(self, strategy: list[str], tells_your_draw: bool):
        if tells_your_draw:
            self.rounds = list(self._parse_draw_strategy(strategy=strategy))
        else:
            self.rounds = list(self._parse_result_guide(strategy=strategy))

    @staticmethod
    def _parse_draw_strategy(strategy: list[str]) -> Iterable[Round]:
        """Simulate all game rounds included in the strategy guide."""
        your_draw_translator = dict(X="A", Y="B", Z="C")
        for game_round in strategy:
            foe_draw, your_draw = game_round.split(" ")
            yield Round(your_draw=your_draw_translator[your_draw], foe_draw=foe_draw)

    @staticmethod
    def _parse_result_guide(strategy: list[str]) -> Iterable[Round]:
        """Simulate all game rounds included in the strategy guide."""
        for game_round in strategy:
            foe_draw, result = game_round.split(" ")
            yield Round.from_foe_and_target(result=result, foe_draw=foe_draw)

    @property
    def total_score(self) -> int:
        """Provide the sum of your scores for all rounds."""
        return sum([game_round.score for game_round in self.rounds])
