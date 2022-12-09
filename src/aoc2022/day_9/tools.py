# coding=utf-8
"""Tools used for solving the Day 9: Rope Bridge puzzle."""


class Point:
    """Representation of a location in a 2D discrete region."""
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __add__(self, other: "Point") -> "Point":
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __eq__(self, other: "Point") -> bool:
        return self.coordinates == other.coordinates

    def __hash__(self) -> int:
        return hash(self.coordinates)

    @property
    def coordinates(self) -> tuple[int, int]:
        """Provide the XY coordinates of this Point as a tuple."""
        return self.x, self.y

    def copy(self) -> "Point":
        """Provide a perfect replica of this Point."""
        return Point(x=self.x, y=self.y)


class Rope:
    """Simulation of the knots of one of the ropes forming a rope bridge."""
    def __init__(self, nodes: int):
        start = Point(x=0, y=0)
        self.nodes = [start.copy() for _ in range(nodes)]
        self._tail_history = []
        self._register_positions()

    @property
    def tail_positions(self) -> list[Point]:
        """Provide each Point the tail has visited up to now."""
        return [*self._tail_history]

    def apply_motions(self, motions: list[str]):
        """Do a series of individual motions."""
        for motion in motions:
            self._move(motion=motion)

    def _move(self, motion: str):
        """Change the location of the first node of this Rope and update other nodes."""
        direction, steps = motion.split(" ")
        for _ in range(int(steps)):
            self._move_head(direction=direction)
            self._move_nodes()
            self._register_positions()

    def _move_head(self, direction: str):
        """Move the head of this Rope ONE step along one of the 2D cartesian axes."""
        if direction == "U":
            self.nodes[0].y += 1
        elif direction == "D":
            self.nodes[0].y -= 1
        elif direction == "L":
            self.nodes[0].x -= 1
        elif direction == "R":
            self.nodes[0].x += 1
        else:
            raise ValueError(f"Invalid '{direction}' direction.")

    def _move_nodes(self):
        """Move each non-head node of this Rope ONE step towards its previous node."""
        for n in range(1, len(self.nodes)):
            dx = self.nodes[n - 1].x - self.nodes[n].x
            dy = self.nodes[n - 1].y - self.nodes[n].y
            if max(abs(dx), abs(dy)) > 1:
                if abs(dx) == 2 and dy == 0:
                    self.nodes[n].x += int(dx / abs(dx))
                elif dx == 0 and abs(dy) == 2:
                    self.nodes[n].y += int(dy / abs(dy))
                elif dx != 0 and dy != 0:
                    self.nodes[n].x += int(dx / abs(dx))
                    self.nodes[n].y += int(dy / abs(dy))

    def _register_positions(self):
        """Register the current location of the last node in this Rope."""
        self._tail_history.append(self.nodes[-1].copy())
