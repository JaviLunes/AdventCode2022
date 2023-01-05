# coding=utf-8
"""Tools used for solving the Day 22: Monkey Map puzzle."""

# Standard library imports:
from itertools import cycle, islice
from math import inf

# Set constants:
FACING_VALUES = {"→": 0, "↓": 1, "←": 2, "↑": 3}
FACING_ARROWS = {v: k for k, v in FACING_VALUES.items()}


Position = tuple[int, int, str]
Stripe = list[tuple[Position, str]]


class MonkeyBoard:
    """Strangely-shaped board of open, walled and off-limits 2D tiles."""
    def __init__(self, board_rows: list[str]):
        self.rows = board_rows

    def get_walk_path(self, traveller: "BoardTraveller", steps: int) -> list[Position]:
        """Traveller's row, column and facing after each step in a straight walk."""
        stripe = self._cut_walk_stripe(*traveller.coordinates)
        stripe = self._filter_off_tiles(stripe=stripe)
        indices, tiles = zip(*stripe)
        steps = min(steps, tiles.index("#") if "#" in tiles else inf)
        return list(islice(cycle(indices), steps)) if steps > 0 else indices[-1:]

    def _cut_walk_stripe(self, row: int, col: int, facing: str) -> Stripe:
        """All open, walled and off-map tiles ahead from the given position."""
        assert facing in ["→", "←", "↓", "↑"], f"Invalid '{facing}' facing."
        if facing in ["→", "←"]:
            tiles = self.rows[row]
            positions = [(row, c, facing) for c in range(len(tiles))]
        else:
            tiles = "".join([row[col] for row in self.rows])
            positions = [(r, col, facing) for r in range(len(tiles))]
        start = positions.index((row, col, facing))
        stripe = list(zip(positions, tiles))
        if facing in ["→", "↓"]:
            return stripe[start + 1:] + stripe[:start + 1]
        else:
            return stripe[:start][::-1] + stripe[start:][::-1]

    @staticmethod
    def _filter_off_tiles(stripe: Stripe) -> Stripe:
        """Remove off-map tile entries from a Stripe."""
        return [(i, tile) for i, tile in stripe if tile != " "]

    @property
    def shape(self) -> tuple[int, int]:
        """Tuple with the number of rows and columns of this MonkeyBoard."""
        return len(self.rows), len(self.rows[0])

    @property
    def starting_point(self) -> tuple[int, int]:
        """Row and column coordinates for the leftmost open tile at the topmost row."""
        return 0, self.rows[0].index(".")

    @classmethod
    def from_notes(cls, monkey_notes: list[str]) -> "MonkeyBoard":
        """Crate a new MonkeyBoard from the lines of notes handed by the monkeys."""
        board_notes = monkey_notes[:-2]
        m, n = len(board_notes), max(len(line) for line in board_notes)
        board_rows = [row + " " * (n - len(row)) for row in board_notes]
        return cls(board_rows=board_rows)


class BoardTraveller:
    """Symbolic figure walking across the MonkeyBoard."""
    def __init__(self, board: "MonkeyBoard", walk_plan: list[str]):
        self.board = board
        self.walk_plan = walk_plan
        self.row, self.column = board.starting_point
        self.facing = "→"

    def __repr__(self) -> str:
        return f"({self.row},{self.column}) {self.facing}"

    def travel(self):
        """Make this Traveller execute the entire walk plan."""
        for action in self.walk_plan:
            if action.isdecimal():
                self._move(n_tiles=int(action))
            else:
                self._rotate(direction=action)

    def _move(self, n_tiles: int):
        """Move a number of tiles (or until hitting a wall) over a Stripe."""
        positions = self.board.get_walk_path(traveller=self, steps=n_tiles)
        if self.facing in ["→", "←"]:
            self.column = positions[-1][1]
        else:
            self.row = positions[-1][0]

    def _rotate(self, direction: str):
        """Rotate the current facing 90° clockwise (R) or anti-clockwise (L)."""
        change = 1 if direction == "R" else -1
        new_facing_value = (FACING_VALUES[self.facing] + change) % 4
        self.facing = FACING_ARROWS[new_facing_value]

    @property
    def coordinates(self) -> Position:
        """Provide a tuple with the current row, column and facing of this Traveller."""
        return self.row, self.column, self.facing

    @property
    def pass_code(self) -> int:
        """Compose a numeric password from the current row, column and facing."""
        return (self.row + 1) * 1000 + (self.column + 1) * 4 + FACING_VALUES[self.facing]

    @classmethod
    def from_notes(cls, monkey_notes: list[str]) -> "BoardTraveller":
        """Create a new Traveller from the lines of notes handed by the monkeys."""
        board = MonkeyBoard.from_notes(monkey_notes=monkey_notes)
        walk_plan = monkey_notes[-1]
        walk_plan = walk_plan.replace("R", "|R|").replace("L", "|L|").replace("||", "|")
        walk_plan = walk_plan.split("|")
        return cls(board=board, walk_plan=walk_plan)
