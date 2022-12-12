# coding=utf-8
"""Tools used for solving the Day 12: Hill Climbing Algorithm puzzle."""

# Standard library imports:
from collections.abc import Callable, Iterable
import heapq
from string import ascii_lowercase


class Point:
    """Location in a 2D map with an additional Z (height) coordinate."""
    __slots__ = ["x", "y", "z"]

    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = x, y, z

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"

    def can_reach(self, other: "Point") -> bool:
        """Check if a hiker could reach another (different) Point from this Point."""
        is_close_z = other.z - self.z <= 1
        return self._is_adjacent(other=other) and is_close_z

    def can_be_reached(self, other: "Point") -> bool:
        """Check if a hiker could reach this Point from another (different) Point."""
        is_close_z = self.z - other.z <= 1
        return self._is_adjacent(other=other) and is_close_z

    def _is_adjacent(self, other: "Point") -> bool:
        """Check if this Point exactly ONE unit away from another Point."""
        d_x, d_y = abs(self.x - other.x), abs(self.y - other.y)
        return d_x + d_y == 1

    @property
    def xy(self) -> tuple[int, int]:
        """Provide a tuple with the X and Y coordinates of this Point."""
        return self.x, self.y


class Node(Point):
    """Point able to behave as a node in an A* search algorithm."""
    __slots__ = ["g", "parent"]

    def __init__(self, x: int, y: int, z: int, g: int, parent: "Node" = None):
        super().__init__(x=x, y=y, z=z)
        self.g = g
        self.parent = parent

    def __hash__(self) -> int:
        return hash(self.xy)

    def __lt__(self, other: "Node") -> bool:
        return self.g < other.g

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z}): {self.g}"

    @property
    def lineage(self) -> list["Node"]:
        """Provide a list with this node and its recursive parents (if any)."""
        return [self] + self.parent.lineage if self.parent else []

    @classmethod
    def from_point(cls, point: Point, g: int, parent: "Node" = None) -> "Node":
        """Create a new Node from a regular Point."""
        return cls(x=point.x, y=point.y, z=point.z, g=g, parent=parent)


class ElvesMaps:
    """App for computing optimized hiking paths, now without Numpy!."""
    def __init__(self, height_map: list[str]):
        self._z_map = self._get_z_map()
        self._points = set(self._process_heights(heights=height_map))

    @staticmethod
    def _get_z_map() -> dict[str, int]:
        """Return a dictionary mapping string marks to z heights."""
        z_map = {char: i for i, char in enumerate(ascii_lowercase)}
        z_map.update({"S": z_map["a"], "E": z_map["z"]})
        return z_map

    def _process_heights(self, heights: list[str]) -> Iterable[Point]:
        """Transform the provided heights string map into a group of Point objects."""
        for j, height_row in enumerate(heights):
            for i, height_str in enumerate(height_row):
                point = Point(x=i, y=j, z=self._z_map[height_str])
                if height_str == "S":
                    self._start = point
                elif height_str == "E":
                    self._end = point
                yield point

    def build_route_from_start(self) -> list[Node]:
        """Find the shortest node-path from given start to the end using A* search."""
        start_node = Node.from_point(point=self._start, g=0)
        heirs_func = self._get_reachable_nodes
        goal_rule = self._is_goal_node
        goal_node = self._a_star_search(
            start=start_node, heirs_func=heirs_func, goal_rule=goal_rule)
        return goal_node.lineage[::-1]

    def build_scenic_route(self) -> list[Node]:
        """Find the shortest node-path from any 'a' node to the end using A* search."""
        start_node = Node.from_point(point=self._end, g=0)
        heirs_func = self._get_reaching_nodes
        goal_rule = self._is_low_height_node
        goal_node = self._a_star_search(
            start=start_node, heirs_func=heirs_func, goal_rule=goal_rule)
        return goal_node.lineage

    def _a_star_search(
            self, start: Node, heirs_func: Callable, goal_rule: Callable) -> Node:
        """Use the A* search algorithm to find the best path from start to goal."""
        # Build lists / queues / min heaps / sets / cost maps:
        pending_nodes = [start]
        visited_nodes = set()
        best_g_costs = {point.xy: 99999 for point in self._points}
        best_g_costs[start.xy] = start.g
        # Check each pending node one at a time, from lowest to greatest g cost:
        while pending_nodes:
            q_node = heapq.heappop(pending_nodes)
            # Stop if the goal is reached:
            if goal_rule(q_node):
                return q_node
            if q_node in visited_nodes:
                continue  # Skip node if its location was already visited.
            # For each possible neighbour node:
            for s_node in heirs_func(q_node):
                if s_node in visited_nodes:
                    continue  # Skip successor if its location was already visited:
                if s_node.g >= best_g_costs[s_node.xy]:
                    continue  # Skip successor if worse than its location's best cost.
                # Register successor node for future checking:
                heapq.heappush(pending_nodes, s_node)
                best_g_costs[s_node.xy] = s_node.g
            # Register the parent node's location as already seen:
            visited_nodes.add(q_node)
        # If code reaches this point, the goal was never reached:
        raise ValueError("The search could not reach the end Point.")

    def _get_reachable_nodes(self, node: Node) -> Iterable[Node]:
        """Return every stored node that can be reached by the provided node."""
        for point in self._points:
            if node.can_reach(other=point):
                yield Node.from_point(point=point, g=node.g + 1, parent=node)

    def _get_reaching_nodes(self, node: Node) -> Iterable[Node]:
        """Return every stored node that can reach the provided node."""
        for point in self._points:
            if node.can_be_reached(other=point):
                yield Node.from_point(point=point, g=node.g + 1, parent=node)

    def _is_goal_node(self, node: Node) -> bool:
        """Check if the provided node is the end 'E' node."""
        return node.xy == self._end.xy

    def _is_low_height_node(self, node: Node) -> bool:
        """Check if the provided node is an 'a'-height node."""
        return node.z == self._z_map["a"]
