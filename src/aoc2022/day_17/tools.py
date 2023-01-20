# coding=utf-8
"""Tools used for solving the Day 17: Pyroclastic Flow puzzle."""

# Standard library imports:
from collections.abc import Callable, Sequence

# Set constants:
ROCK_TYPES = ["HRock", "CrossRock", "LRock", "VRock", "SquareRock"]


class Rock:
    """Group of rock blocks fused together in a fixed shape."""
    __slots__ = ["blocks", "left", "right", "top", "bottom"]

    def __init__(self, rock_shape: str, left_edge: int, bottom_edge: int):
        building_func = self._select_building_function(rock_shape=rock_shape)
        self.blocks = building_func(x_origin=left_edge, y_origin=bottom_edge)
        self.left = min(x for x, _ in self.blocks)
        self.right = max(x for x, _ in self.blocks)
        self.top = max(y for _, y in self.blocks)
        self.bottom = min(y for _, y in self.blocks)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {(self.left, self.bottom)}"

    def _select_building_function(self, rock_shape: str) -> Callable:
        """Generate all blocks forming this Rock."""
        if rock_shape == "HRock":
            return self._build_h_blocks
        if rock_shape == "CrossRock":
            return self._build_cross_blocks
        if rock_shape == "LRock":
            return self._build_l_blocks
        if rock_shape == "VRock":
            return self._build_v_blocks
        if rock_shape == "SquareRock":
            return self._build_square_blocks

    @staticmethod
    def _build_h_blocks(x_origin: int, y_origin: int) -> set[tuple[int, int]]:
        """Generate blocks composing a 4x1 horizontal line pattern."""
        return {(x_origin + d, y_origin) for d in range(4)}

    @staticmethod
    def _build_v_blocks(x_origin: int, y_origin: int) -> set[tuple[int, int]]:
        """Generate blocks composing a 4x1 vertical line pattern."""
        return {(x_origin, y_origin + d) for d in range(4)}

    @staticmethod
    def _build_cross_blocks(x_origin: int, y_origin: int) -> set[tuple[int, int]]:
        """Generate blocks composing a 3x3 cross pattern."""
        h_blocks = [(x_origin + d, y_origin + 1) for d in range(3)]
        tb_blocks = [(x_origin + 1, y_origin + d) for d in [0, 2]]
        return set(h_blocks + tb_blocks)

    @staticmethod
    def _build_square_blocks(x_origin: int, y_origin: int) -> set[tuple[int, int]]:
        """Generate blocks composing a 2x2 square pattern."""
        b_blocks = [(x_origin + d, y_origin) for d in range(2)]
        t_blocks = [(x_origin + d, y_origin + 1) for d in range(2)]
        return set(b_blocks + t_blocks)

    @staticmethod
    def _build_l_blocks(x_origin: int, y_origin: int) -> set[tuple[int, int]]:
        """Generate blocks composing a 3x3 L pattern flipped along the Y axis."""
        h_blocks = [(x_origin + d, y_origin) for d in range(3)]
        v_blocks = [(x_origin + 2, y_origin + d) for d in range(1, 3)]
        return set(h_blocks + v_blocks)

    def move_down(self):
        """Move this Rock one unit down."""
        self.blocks = {(x, y - 1) for x, y in self.blocks}
        self.bottom -= 1
        self.top -= 1

    def move_down_inv(self):
        """Move this Rock one unit up."""
        self.blocks = {(x, y + 1) for x, y in self.blocks}
        self.bottom += 1
        self.top += 1

    def move_side(self, side: str):
        """Move this Rock one unit towards '<' (left) or '>' (right)."""
        d_x = 1 if side == ">" else -1
        self.blocks = {(x + d_x, y) for x, y in self.blocks}
        self.left += d_x
        self.right += d_x

    def move_side_inv(self, side: str):
        """Move this Rock one unit from-wards '<' (left) or '>' (right)."""
        self.move_side(side="<" if side == ">" else ">")


class Thrower:
    """Closed loop iterator providing each of its stored items one at a time."""
    def __init__(self, items: Sequence):
        self._items = items
        self._index = 0
        self._n_items = len(self._items)

    def __iter__(self):
        return self

    def __next__(self):
        item = self._items[self._index]
        self._index = (self._index + 1) % self._n_items
        return item


class RockPit:
    """Tall and narrow chamber where Rock objects keep falling and piling."""
    width = 7

    def __init__(self, jet_patterns: str):
        self.jets = Thrower(items=jet_patterns)
        self.shapes = Thrower(items=ROCK_TYPES)
        self.tower_height = 0
        self.resting_blocks = set()

    def drop_rocks(self, n_rocks: int):
        """Create and drop a given number of new Rock objects."""
        for _ in range(n_rocks):
            self._drop_rock()

    def _drop_rock(self):
        """Create a new Rock at the pit top and let it fall until it rests."""
        rock_shape, height = next(self.shapes), self.tower_height + 4
        rock: Rock = Rock(rock_shape=rock_shape, left_edge=3, bottom_edge=height)
        while True:
            # Try to push the falling rock sideways with a jet:
            jet = next(self.jets)
            rock.move_side(side=jet)
            if self._crashed_side(rock=rock):  # Reverse move.
                rock.move_side_inv(side=jet)
            # Try to drop the falling rock:
            rock.move_down()
            if self._crashed_down(rock=rock):  # Reverse move and let the rock rest.
                rock.move_down_inv()
                break
        self._register_rock(rock=rock)

    def _crashed_side(self, rock: Rock) -> bool:
        """Check if the provided Rock has moved sidewards to an illegal position."""
        if bool(rock.blocks & self.resting_blocks):
            return True  # The rock crashed into the tower of resting blocks.
        if rock.left <= 0:
            return True  # The rock crashed into the left wall.
        if rock.right >= self.width + 1:
            return True  # The rock crashed into the right wall.
        return False

    def _crashed_down(self, rock: Rock) -> bool:
        """Check if the provided Rock has moved downwards to an illegal position."""
        if bool(rock.blocks & self.resting_blocks):
            return True  # The rock crashed into the tower of resting blocks.
        if rock.bottom <= 0:
            return True  # The rock crashed into the pit floor.
        return False

    def _register_rock(self, rock: Rock):
        """Register a resting Rock's blocks on the block map."""
        self.resting_blocks |= rock.blocks
        self.tower_height = max(self.tower_height, rock.top)
