# coding=utf-8
"""Tools used for solving the Day 17: Pyroclastic Flow puzzle."""

# Standard library imports:
from collections import Counter
from collections.abc import Callable, Sequence

# Define custom types:
Block = tuple[int, int]

# Set constants:
ROCK_TYPES = ["HRock", "CrossRock", "LRock", "VRock", "SquareRock"]


class Rock:
    """Group of rock blocks fused together in a fixed shape."""
    __slots__ = ["blocks", "shape", "left", "right", "top", "bottom"]

    def __init__(self, rock_shape: str, left_edge: int, bottom_edge: int):
        building_func = self._select_building_function(rock_shape=rock_shape)
        self.blocks = building_func(x_origin=left_edge, y_origin=bottom_edge)
        self.shape = rock_shape
        self.left = min(x for x, _ in self.blocks)
        self.right = max(x for x, _ in self.blocks)
        self.top = max(y for _, y in self.blocks)
        self.bottom = min(y for _, y in self.blocks)

    def __repr__(self) -> str:
        return f"{self.shape}: {(self.left, self.bottom)}"

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
    def _build_h_blocks(x_origin: int, y_origin: int) -> set[Block]:
        """Generate blocks composing a 4x1 horizontal line pattern."""
        return {(x_origin + d, y_origin) for d in range(4)}

    @staticmethod
    def _build_v_blocks(x_origin: int, y_origin: int) -> set[Block]:
        """Generate blocks composing a 4x1 vertical line pattern."""
        return {(x_origin, y_origin + d) for d in range(4)}

    @staticmethod
    def _build_cross_blocks(x_origin: int, y_origin: int) -> set[Block]:
        """Generate blocks composing a 3x3 cross pattern."""
        h_blocks = [(x_origin + d, y_origin + 1) for d in range(3)]
        tb_blocks = [(x_origin + 1, y_origin + d) for d in [0, 2]]
        return set(h_blocks + tb_blocks)

    @staticmethod
    def _build_square_blocks(x_origin: int, y_origin: int) -> set[Block]:
        """Generate blocks composing a 2x2 square pattern."""
        b_blocks = [(x_origin + d, y_origin) for d in range(2)]
        t_blocks = [(x_origin + d, y_origin + 1) for d in range(2)]
        return set(b_blocks + t_blocks)

    @staticmethod
    def _build_l_blocks(x_origin: int, y_origin: int) -> set[Block]:
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

    def __repr__(self) -> str:
        return repr(self._items[self._index])

    def __iter__(self):
        return self

    def __next__(self):
        item = self._items[self._index]
        self._index = (self._index + 1) % self._n_items
        return item

    @property
    def last_index(self) -> int:
        """Index of this Thrower previous to the currently active one."""
        return (self._index - 1) % self._n_items


class RockPit:
    """Tall and narrow chamber where Rock objects keep falling and piling."""
    _width = 7
    _col_range = range(1, _width + 1)

    def __init__(self, jet_patterns: str):
        self._set_initial_state(jet_patterns=jet_patterns)
        self._find_cyclic_state()
        self._set_initial_state(jet_patterns=jet_patterns)

    def __repr__(self) -> str:
        return f"Tower height: {self.tower_height}"

    def _set_initial_state(self, jet_patterns: str):
        """Configure the internal state of this RockPit before any rock is dropped."""
        self.jets = Thrower(items=jet_patterns)
        self.shapes = Thrower(items=ROCK_TYPES)
        self.resting_blocks = set()
        self._top_blocks = {x: 0 for x in self._col_range}
        self._height_relative = 0
        self._height_absolute = 0

    def _find_cyclic_state(self):
        """Find those internal state values that repeat after a given number of rocks."""
        dropped_rocks = 0
        state_counter = Counter()
        height_log = {}
        # Drop rocks until one state is repeated 3 times:
        while True:
            self._drop_rock()
            dropped_rocks += 1
            state_counter[self.current_state] += 1
            height_log.update({dropped_rocks: self._height_absolute})
            if state_counter.most_common(n=1)[0][1] == 3:
                # Register cycle-related attributes:
                count_values = state_counter.values()
                self.warmup_rounds = sum(filter(lambda c: c == 1, count_values)) + 1
                self.cycle_length = len(state_counter) - self.warmup_rounds + 1
                current_height = height_log[dropped_rocks]
                previous_cycle_height = height_log[dropped_rocks - self.cycle_length]
                self.cycle_blocks = self.current_state[2]
                self.cycle_height_delta = current_height - previous_cycle_height
                break

    def drop_rocks(self, remaining_rocks: int):
        """Create and drop a given number of new Rock objects."""
        # Short-circuit for small amounts of rocks:
        if remaining_rocks < self.warmup_rounds + 2 * self.cycle_length:
            [self._drop_rock() for _ in range(remaining_rocks)]
            return
        # Warm-up rounds:
        [self._drop_rock() for _ in range(self.warmup_rounds)]
        remaining_rocks -= self.warmup_rounds
        # Full-cycle rounds:
        avoided_cycles, remaining_rocks = divmod(remaining_rocks, self.cycle_length)
        self._height_absolute += self.cycle_height_delta * avoided_cycles
        # Leftover rounds:
        [self._drop_rock() for _ in range(remaining_rocks)]

    def _drop_rock(self):
        """Create a new Rock at the pit top and let it fall until it rests."""
        rock_shape, height = next(self.shapes), self._height_relative + 4
        rock = Rock(rock_shape=rock_shape, left_edge=3, bottom_edge=height)
        # Move the Rock until it rests:
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
        # Register resting rock:
        self._register_rock(rock=rock)
        # Consolidate block tower (if possible):
        if self.can_consolidate:
            self._consolidate_tower()

    def _crashed_side(self, rock: Rock) -> bool:
        """Check if the provided Rock has moved sidewards to an illegal position."""
        if bool(rock.blocks & self.resting_blocks):
            return True  # The rock crashed into the tower of resting blocks.
        if rock.left <= 0:
            return True  # The rock crashed into the left wall.
        if rock.right >= self._width + 1:
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
        delta_height = max(0, rock.top - self._height_relative)
        self._height_relative += delta_height
        self._height_absolute += delta_height
        for x, y in rock.blocks:
            self._top_blocks[x] = max(self._top_blocks[x], y)

    def _consolidate_tower(self):
        """Drop all blocks below a minimum, unreachable depth in this RockPit."""
        floor = min(self._top_blocks.values())
        remaining_blocks = set(filter(lambda r: r[1] > floor, self.resting_blocks))
        self._top_blocks = {x: y - floor for x, y in self._top_blocks.items()}
        self.resting_blocks = {(x, y - floor) for x, y in remaining_blocks}
        self._height_relative -= floor

    @property
    def can_consolidate(self) -> bool:
        """Check if all columns in the pit have at least one block."""
        return all(self._top_blocks[x] > 0 for x in self._col_range)

    @property
    def current_state(self) -> tuple[int, int, tuple[Block]]:
        """Tuple of jets' and shapes' last active index and current resting blocks."""
        # noinspection PyTypeChecker
        return self.shapes.last_index, self.jets.last_index, tuple(self.resting_blocks)

    @property
    def tower_height(self) -> int:
        """Absolute height in blocks of the tower of resting blocks inside the pit."""
        return self._height_absolute
