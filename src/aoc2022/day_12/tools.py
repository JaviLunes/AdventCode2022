# coding=utf-8
"""Tools used for solving the Day 12: Hill Climbing Algorithm puzzle."""

# Standard library imports:
from collections.abc import Iterable
from string import ascii_lowercase

# Third party imports:
from aoc_tools.algorithms.a_star_search import Node, a_star_search


class TrailStage(Node):
    """Each discrete location visited during the ascension from the start point."""
    __slots__ = ["x", "y", "z", "n", "_heights_map"]

    def __init__(self, x: int, y: int, n: int, heights_map: dict[tuple[int, int], int],
                 parent: "TrailStage" = None):
        super().__init__(parent=parent)
        self.x, self.y = x, y
        self.n = n
        self.z = heights_map[(x, y)]
        self._heights_map = heights_map

    @property
    def id(self) -> str:
        """Provide a string identifier unique to this TrailStage."""
        return f"{self.x},{self.y}"

    @property
    def g(self) -> int:
        """Compute the cost for reaching this TrailStage from the search start point."""
        return self.n

    @property
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from this TrailStage."""
        return 0

    @property
    def xy(self) -> tuple[int, int]:
        """Provide a tuple with the XY coordinates of this TrailStage."""
        return self.x, self.y

    def get_successors(self) -> Iterable["TrailStage"]:
        """List all nodes to search that are directly reachable from this TrailStage."""
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            x, y = self.x + dx, self.y + dy
            s_z = self._heights_map.get((x, y), None)
            if self._is_valid_z(z=s_z):
                yield self.__class__(
                    x=x, y=y, n=self.n + 1, heights_map=self._heights_map, parent=self)

    def _is_valid_z(self, z: int | None) -> bool:
        """Check if the height of the successor node is valid."""
        return z is not None and z - self.z <= 1


class DescentStage(TrailStage):
    """Each discrete location visited during the descent from the best signal point."""

    def _is_valid_z(self, z: int | None) -> bool:
        """Check if the height of the successor node is valid."""
        return z is not None and self.z - z <= 1


class ElvesMaps:
    """App for computing optimized hiking paths, now without Numpy!"""
    def __init__(self, height_map: list[str]):
        self._start = self._find_start_location(heights=height_map)
        self._goal = self._find_goal_location(heights=height_map)
        self._heights_map = self._process_heights(heights=height_map)

    @staticmethod
    def _find_start_location(heights: list[str]) -> tuple[int, int]:
        """Retrieve the XY coordinates of the start position in the hill ascension."""
        idx = "".join(heights).index("S")
        return idx % len(heights[0]), idx // len(heights[0])

    @staticmethod
    def _find_goal_location(heights: list[str]) -> tuple[int, int]:
        """Retrieve the XY coordinates of the target position in the hill ascension."""
        idx = "".join(heights).index("E")
        return idx % len(heights[0]), idx // len(heights[0])

    @staticmethod
    def _process_heights(heights: list[str]) -> dict[tuple[int, int], int]:
        """Transform the provided heights string map into a group of locations."""
        level_map = {char: i for i, char in enumerate(ascii_lowercase)}
        level_map.update({"S": level_map["a"], "E": level_map["z"]})
        x_range, y_range = range(len(heights[0])), range(len(heights))
        return {(x, y): level_map[heights[y][x]] for x in x_range for y in y_range}

    def build_route_from_start(self) -> list[Node]:
        """Find the shortest node-path from given start to the end using A* search."""
        start = TrailStage(*self._start, n=0, heights_map=self._heights_map, parent=None)
        goal_node = a_star_search(
            start=start, goal_func=lambda node: node.xy == self._goal)
        return goal_node.lineage[::-1]

    def build_scenic_route(self) -> list[Node]:
        """Find the shortest node-path from any 'a' node to the end using A* search."""
        target_height = self._heights_map[self._start]
        start = DescentStage(
            *self._goal, n=0, heights_map=self._heights_map, parent=None)
        goal_node = a_star_search(
            start=start, goal_func=lambda node: node.z == target_height)
        return goal_node.lineage

    def min_steps_for_ascension_route(self) -> int:
        """Count the min number of steps for reaching the goal from the start."""
        stages = self.build_route_from_start()
        return len(stages) - 1

    def min_steps_for_scenic_route(self) -> int:
        """Count the min number of steps for reaching the goal from any 'a' location."""
        stages = self.build_scenic_route()
        return len(stages) - 1
