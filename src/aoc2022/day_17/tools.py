# coding=utf-8
"""Tools used for solving the Day 17: Pyroclastic Flow puzzle."""

# Standard library imports:
import abc
from collections.abc import Sequence


class Rock(metaclass=abc.ABCMeta):
    """Group of rock blocks fused together in a fixed shape."""
    __slots__ = ["origin"]

    def __init__(self, left_edge: int, bottom_edge: int):
        self.origin = (left_edge, bottom_edge)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.origin}"

    @abc.abstractmethod
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        raise NotImplementedError

    @property
    def blocks(self) -> set[tuple[int, int]]:
        """Provide all blocks forming this Rock."""
        return self._build_blocks()

    @property
    def top(self) -> int:
        """Provide the Y coord of the highest block in this Rock."""
        return max(block[1] for block in self.blocks)

    def any_at_y(self, y: int) -> bool:
        """Check if any of this Rock's blocks is at the given Y coordinate."""
        return any(block[1] == y for block in self.blocks)

    def any_at_x(self, x: int) -> bool:
        """Check if any of this Rock's blocks is at the given X coordinate."""
        return any(block[0] == x for block in self.blocks)

    def move_down(self):
        """Move this Rock one unit down."""
        self.origin = (self.origin[0], self.origin[1] - 1)

    def move_down_inv(self):
        """Move this Rock one unit up."""
        self.origin = (self.origin[0], self.origin[1] + 1)

    def move_side(self, side: str):
        """Move this Rock one unit towards '<' (left) or '>' (right)."""
        d_x = 1 if side == ">" else -1
        self.origin = (self.origin[0] + d_x, self.origin[1])

    def move_side_inv(self, side: str):
        """Move this Rock one unit from-wards '<' (left) or '>' (right)."""
        self.move_side(side="<" if side == ">" else ">")


class HRock(Rock):
    """Rock composing a 4x1 horizontal line pattern."""
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        return {(self.origin[0] + d, self.origin[1]) for d in range(4)}


class VRock(Rock):
    """Rock composing a 4x1 vertical line pattern."""
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        return {(self.origin[0], self.origin[1] + d) for d in range(4)}


class CrossRock(Rock):
    """Rock composing a 3x3 cross pattern."""
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        h_blocks = [(self.origin[0] + d, self.origin[1] + 1) for d in range(3)]
        tb_blocks = [(self.origin[0] + 1, self.origin[1] + d) for d in [0, 2]]
        return set(h_blocks + tb_blocks)


class SquareRock(Rock):
    """Rock composing a 2x2 square pattern."""
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        b_blocks = [(self.origin[0] + d, self.origin[1]) for d in range(2)]
        t_blocks = [(self.origin[0] + d, self.origin[1] + 1) for d in range(2)]
        return set(b_blocks + t_blocks)


class LRock(Rock):
    """Rock composing a 3x3 L pattern flipped along the Y axis."""
    def _build_blocks(self) -> set[tuple[int, int]]:
        """Generate all blocks forming this Rock."""
        h_blocks = [(self.origin[0] + d, self.origin[1]) for d in range(3)]
        v_blocks = [(self.origin[0] + 2, self.origin[1] + d) for d in range(1, 3)]
        return set(h_blocks + v_blocks)


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
        self.shapes = Thrower(items=[HRock, CrossRock, LRock, VRock, SquareRock])
        self.tower_height = 0
        self.block_map = self._get_empty_block_rows()

    def _get_empty_block_rows(self, y_start: int = 1) -> dict[tuple[int, int], bool]:
        """Generate a dictionary of (width x 12) blocks marked as empty."""
        xs, ys = range(1, self.width + 1), range(y_start, y_start + 12)
        return {(x, y): False for y in ys for x in xs}

    def drop_rocks(self, n_rocks: int):
        """Create and drop a given number of new Rock objects."""
        for _ in range(n_rocks):
            self._drop_rock()

    def _drop_rock(self):
        """Create a new Rock at the pit top and let it fall until it rests."""
        shape_cls = next(self.shapes)
        rock: Rock = shape_cls(left_edge=3, bottom_edge=self.tower_height + 4)
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
        if rock.any_at_x(x=0):  # The rock crashed into the left wall.
            return True
        if rock.any_at_x(x=self.width + 1):  # The rock crashed into the right wall.
            return True
        if self._crashed_tower(rock=rock):
            return True
        return False

    def _crashed_down(self, rock: Rock) -> bool:
        """Check if the provided Rock has moved downwards to an illegal position."""
        if rock.any_at_y(y=0):  # The rock crashed into the floor.
            return True
        if self._crashed_tower(rock=rock):
            return True
        return False

    def _crashed_tower(self, rock: Rock) -> bool:
        """Check if the provided Rock has moved into any other Rock resting."""
        return any(self.block_map.get(block, False) for block in rock.blocks)

    def _register_rock(self, rock: Rock):
        """Register a resting Rock's blocks on the block map."""
        new_blocks = rock.blocks
        # Add new empty rows to map if needed:
        top_new_y = max(y for _, y in new_blocks)
        top_old_y = list(self.block_map.keys())[-1][1]
        if top_old_y < top_new_y:
            empty_blocks = self._get_empty_block_rows(y_start=top_old_y + 1)
            self.block_map.update(empty_blocks)
        # Mark new blocks:
        self.block_map.update({block: True for block in new_blocks})
        # Update tower height:
        self.tower_height = max(self.tower_height, top_new_y)
