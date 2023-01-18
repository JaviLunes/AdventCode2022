# coding=utf-8
"""Tools used for solving the Day 24: Blizzard Basin puzzle."""

# Standard library imports:
from typing import Iterable

# Third party imports:
from aoc_tools.algorithms.a_star_search import ASNode, a_star_search

# Set constants:
DELTA_MAP = {"^": (0, 1), ">": (1, 0), "v": (0, -1), "<": (-1, 0)}


class Cell:
    """2D discrete location inside the blizzard valley."""
    __slots__ = ["x", "y", "_id", "_hash"]

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y
        self._id = (x, y)
        self._hash = hash((x, y))

    def __repr__(self) -> str:
        return str(self._id)

    def __eq__(self, other: "Cell") -> bool:
        return self._id == other._id

    def __lt__(self, other: "Cell") -> bool:
        return self._id < other._id

    def __hash__(self) -> int:
        return self._hash

    def calc_distance(self, other: "Cell") -> int:
        """Compute the Manhattan distance between this Cell and another Cell."""
        return abs(other.x - self.x) + abs(other.y - self.y)


class Region:
    """Define the XY limits of a 2D rectangular region composed of discrete cells."""
    __slots__ = ["min_x", "max_x", "min_y", "max_y", "cells"]

    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int, other: set[Cell]):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.cells = self._get_region_cells() | other

    def _get_region_cells(self) -> set[Cell]:
        """Generate one Cell per location inside the XY limits of this Region."""
        x_range = range(self.min_x, self.max_x + 1)
        y_range = range(self.min_y, self.max_y + 1)
        return set(Cell(x=x, y=y) for x in x_range for y in y_range)

    def warp_location(self, x: int, y: int) -> tuple[int, int]:
        """If XY point is outside limits, warp it over the X/Y axes to a valid point."""
        if x < self.min_x:
            x = self.max_x
        elif self.max_x < x:
            x = self.min_x
        if y < self.min_y:
            y = self.max_y
        elif self.max_y < y:
            y = self.min_y
        return x, y


class Blizzard(Cell):
    """Snow-and-ice front blown by the strong winds inside the valley."""
    __slots__ = ["direction", "deltas"]

    def __init__(self, x: int, y: int, direction: str):
        super().__init__(x=x, y=y)
        self.direction = direction
        self.deltas = DELTA_MAP[direction]

    def __repr__(self) -> str:
        return f"{self._id} {self.direction}"

    def move(self, region: Region) -> "Blizzard":
        """New Blizzard located one Cell forward on the direction of this Blizzard."""
        dx, dy = self.deltas
        x, y = self.x + dx, self.y + dy
        x, y = region.warp_location(x=x, y=y)
        return Blizzard(x=x, y=y, direction=self.direction)


class SnowMap:
    """Tool for predicting the position of every blizzard blowing over the valley."""
    __slots__ = ["region", "_blizzard_log", "_calm_log"]

    def __init__(self, blizzards: list[Blizzard], region: Region):
        self.region = region
        self._blizzard_log = {0: [*blizzards]}
        self._calm_log = {}

    def forecast_calms(self, t: int) -> set[Cell]:
        """Compose a set of all cells without active blizzards at the target instant."""
        try:
            return self._calm_log[t]
        except KeyError:
            calm_cells = self.region.cells - set(self.forecast_blizzards(t=t))
            self._calm_log.update({t: calm_cells})
            return calm_cells

    def forecast_blizzards(self, t: int) -> list[Blizzard]:
        """List all active blizzards at the target instant."""
        try:
            return self._blizzard_log[t]
        except KeyError:
            self._update_blizzard_log(up_to_t=t)
            return self._blizzard_log[t]

    def _update_blizzard_log(self, up_to_t: int):
        """Simulate and log blizzards for new time instants up to t."""
        last_t = max(self._blizzard_log.keys())
        blizzards = self._blizzard_log[last_t]
        for t in range(last_t + 1, up_to_t + 1):
            blizzards = [blz.move(region=self.region) for blz in blizzards]
            self._blizzard_log[t] = blizzards

    @classmethod
    def from_strings(cls, strings: list[str], region: Region) -> "SnowMap":
        """Create a new SnowMap from strings describing valley's initial state."""
        blizzards = cls._parse_blizzards(strings=strings)
        return SnowMap(blizzards=blizzards, region=region)

    @staticmethod
    def _parse_blizzards(strings: list[str]) -> list[Blizzard]:
        """Build blizzard cells from strings describing the valley's initial state."""
        arrows = "^", ">", "v", "<"
        blizzards = []
        for y, string in enumerate(strings[::-1]):
            blizzards.extend(Blizzard(x=x, y=y, direction=value)
                             for x, value in enumerate(string) if value in arrows)
        return blizzards


class Expedition(ASNode):
    """Group of star-fruit-gatherers traversing the valley one cell at a time."""
    __slots__ = ["cell", "t", "goal", "snow_map"]

    def __init__(self, cell: Cell, t: int, goal: Cell, snow_map: SnowMap,
                 parent: "Expedition" = None):
        super().__init__(parent=parent)
        self.cell, self.t = cell, t
        self.goal, self.snow_map = goal, snow_map

    def __repr__(self) -> str:
        return f"{self.cell}: {len(self.reachable_cells)} moves ({self.t} min)"

    @property
    def id(self) -> str:
        """String identifier unique to this particular Expedition."""
        return f"{self.cell}{self.t}{sorted(self.reachable_cells)}"

    @property
    def g(self) -> int:
        """Compute the cost for reaching the current location from the start point."""
        return self.t

    @property
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from the current location."""
        return self.cell.calc_distance(other=self.goal)

    def get_successors(self) -> Iterable["Expedition"]:
        """List all the immediate paths this Expedition could take from its location."""
        t = self.t + 1
        calm_cells = self.snow_map.forecast_calms(t=t)
        for cell in self.reachable_cells & calm_cells:
            yield Expedition(cell=cell, t=t, goal=self.goal, snow_map=self.snow_map,
                             parent=self)

    @property
    def is_at_goal(self) -> bool:
        """Check if this Expedition is currently at the goal cell."""
        return self.cell == self.goal

    @property
    def reachable_cells(self) -> set[Cell]:
        """Set of all cells this Expedition could reach in one time step."""
        deltas = list(DELTA_MAP.values()) + [(0, 0)]
        return {Cell(x=self.cell.x + dx, y=self.cell.y + dy) for dx, dy in deltas}


class Valley:
    """Mountain-walled, blizzard-swept rectangular area with only two exit points."""
    def __init__(self, region: Region, snow_map: SnowMap, start: "Cell", goal: "Cell"):
        self.region, self.snow_map = region, snow_map
        self.start, self.goal = start, goal

    def plan_travel_to_goal(self, t: int) -> Expedition:
        """Find the shortest path through the blizzards from the start to the goal."""
        start = Expedition(cell=self.start, t=t, goal=self.goal, snow_map=self.snow_map)
        goal = a_star_search(start=start, goal_func=lambda node: node.is_at_goal)
        return goal

    def plan_travel_to_start(self, t: int) -> Expedition:
        """Find the shortest path through the blizzards from the goal to the start."""
        start = Expedition(cell=self.goal, t=t, goal=self.start, snow_map=self.snow_map)
        goal = a_star_search(start=start, goal_func=lambda node: node.is_at_goal)
        return goal

    @property
    def mountains(self) -> set[Cell]:
        """Cells defining the mountains that wall the Valley."""
        length = self.region.max_y - self.region.min_y + 3
        width = self.region.max_x - self.region.min_x + 3
        bottom_wall = {Cell(x=x, y=0) for x in range(width)}
        top_wall = {Cell(x=x, y=length - 1) for x in range(width)}
        left_wall = {Cell(x=0, y=y) for y in range(1, length - 1)}
        right_wall = {Cell(x=width - 1, y=y) for y in range(1, length - 1)}
        return top_wall | bottom_wall | left_wall | right_wall - {self.start, self.goal}

    @classmethod
    def from_strings(cls, strings: list[str]) -> "Valley":
        """Create a new Valley from the strings describing its initial state."""
        length, width = len(strings), len(strings[0])
        start = Cell(x=strings[0].index("."), y=length - 1)
        goal = Cell(x=strings[-1].index("."), y=0)
        region = Region(
            min_x=1, max_x=width - 2, min_y=1, max_y=length - 2, other={start, goal})
        snow_map = SnowMap.from_strings(strings=strings, region=region)
        return Valley(region=region, start=start, goal=goal, snow_map=snow_map)
