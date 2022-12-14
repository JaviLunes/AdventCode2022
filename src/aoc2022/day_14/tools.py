# coding=utf-8
"""Tools used for solving the Day 14: Regolith Reservoir puzzle."""

# Standard library imports:
from collections.abc import Iterable


class Cell:
    """2D space defining one discrete location inside the AbyssCave."""
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __hash__(self) -> int:
        return hash(self.xy)

    def __repr__(self) -> str:
        return f"{self.xy}"

    @property
    def xy(self) -> tuple[int, int]:
        """Provide the X and Y coordinates of this Cell as a tuple."""
        return self.x, self.y

    def cells_between(self, other: "Cell") -> list["Cell"]:
        """Build a 2D Cell path from this Cell (included) to another (not included)."""
        dist_x, dist_y = other.x - self.x, other.y - self.y
        assert not (dist_x != 0 and dist_y != 0)
        if dist_x != 0:  # Horizontal path.
            sign = int(dist_x / abs(dist_x))
            return [Cell(x=self.x + sign * d, y=self.y) for d in range(abs(dist_x))]
        else:  # Vertical path.
            sign = int(dist_y / abs(dist_y))
            return [Cell(x=self.x, y=self.y + sign * d) for d in range(abs(dist_y))]

    @classmethod
    def from_str(cls, string: str) -> "Cell":
        """Create a new Cell from a comma-separated-coordinates string."""
        x, y = string.split(",")
        return cls(x=int(x), y=int(y))


class RockBlock(Cell):
    """Cell filled with unmovable rock, part of a larger 2D structure."""


class SandBlock(Cell):
    """Cell filled with semi-fluid sand, able to fall downwards due to gravity."""
    def copy(self) -> "SandBlock":
        """Create an exact replica of this SandBlock, but without shared state."""
        return SandBlock(x=self.x, y=self.y + 1)

    @property
    def possible_moves(self) -> list[Cell]:
        """List the cells this SandBlock could move to, sorted by descending priority."""
        x, y = self.xy
        downwards = Cell(x=x, y=y + 1)
        diagonal_left = Cell(x=x - 1, y=y + 1)
        diagonal_right = Cell(x=x + 1, y=y + 1)
        return [downwards, diagonal_left, diagonal_right]

    def move(self, new_cell: Cell):
        """Register the new coordinates of this SandBlock's position."""
        self.x, self.y = new_cell.x, new_cell.y


class AbyssError(AssertionError):
    """Error raised when a SandBlock starts falling towards the abyss."""
    def __init__(self, block: SandBlock):
        self._block = block

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}: The {self._block} will forever fall into the abyss :("


class SourceError(AssertionError):
    """Error raised when a SandBlock rests at the location of the sand source."""
    def __init__(self, block: SandBlock):
        self._block = block

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}: The {self._block} blocks the sand source."


class AbyssCave:
    """HUGE cave system behind a waterfall with unstable sand masses on its ceiling."""
    def __init__(self, rock_paths: list[str]):
        rock_blocks = self._generate_rock_blocks(rock_paths=rock_paths)
        self._cell_map = {block.xy: block for block in rock_blocks}
        self._find_abyss_depth_line()
        self._sand_source = Cell(x=500, y=0)

    def _generate_rock_blocks(self, rock_paths: list[str]) -> Iterable[RockBlock]:
        """Parse paths of rock structures to generate their RockBlock constituents."""
        for path in rock_paths:
            for cell in self._parse_path(path=path):
                yield RockBlock(x=cell.x, y=cell.y)

    @staticmethod
    def _parse_path(path: str) -> Iterable[Cell]:
        """Decompose a 2D cartesian path in the discrete cells it crosses."""
        cells = [Cell.from_str(string=point) for point in path.split(" -> ")]
        for start, stop in zip(cells[:-1], cells[1:]):
            yield from start.cells_between(other=stop)
        yield cells[-1]

    def _find_abyss_depth_line(self):
        """Define the deepest vertical level of solid rock in this AbyssCave."""
        self._abyss_depth = max(xy[1] for xy in self._cell_map.keys())

    def pour_times(self, times: int):
        """Pour a SandBlock from the sand source a given number of times."""
        for _ in range(times):
            self._pour_sand()

    def pour_while_possible(self, raise_error: bool = False):
        """Keep pouring sand until it falls into the abyss or the source is blocked."""
        while True:
            try:
                self._pour_sand()
            except (AbyssError, SourceError) as e:
                if raise_error:
                    raise e
                else:
                    break

    def _pour_sand(self):
        """Move a SandBlock from the sand source until it rests or disappears."""
        sand = SandBlock(*self._sand_source.xy)
        while True:
            valid_moves = self._filter_blocked_moves(moves=sand.possible_moves)
            if not valid_moves:  # The sand block has come to rest.
                self._cell_map.update({sand.xy: sand})
                break
            sand.move(new_cell=valid_moves[0])
            if sand.y == self._abyss_depth:
                raise AbyssError(block=sand)  # Forever into the abyss :(
        if sand.xy == self._sand_source.xy:
            raise SourceError(block=sand)  # The sand source is now blocked by sand.

    def _filter_blocked_moves(self, moves: list[Cell]) -> list[Cell]:
        """Remove moves that would leave a SandBlock in an already occupied Cell."""
        return [m for m in moves if m.xy not in self._cell_map.keys()]

    @property
    def rock_cells(self) -> list[RockBlock]:
        """Provide a list of all RockBlock objects in this AbyssCave."""
        return list(filter(lambda b: isinstance(b, RockBlock), self._cell_map.values()))

    @property
    def sand_cells(self) -> list[SandBlock]:
        """Provide a list of all RockBlock objects in this AbyssCave."""
        return list(filter(lambda b: isinstance(b, SandBlock), self._cell_map.values()))


class FloorCave(AbyssCave):
    """AbyssCave where the abyss is replaced by a horizontal infinite floor of rock."""
    def __init__(self, rock_paths: list[str]):
        super().__init__(rock_paths=rock_paths)
        self._floor_depth = self._abyss_depth + 2
        self._abyss_depth += 3

    def _filter_blocked_moves(self, moves: list[Cell]) -> list[Cell]:
        """Remove moves that would leave a SandBlock in an already occupied Cell."""
        occupied_cell_moves = [m for m in moves if m.xy in self._cell_map.keys()]
        floor_moves = [m for m in moves if m.y == self._floor_depth]
        return [m for m in moves if m not in occupied_cell_moves + floor_moves]
