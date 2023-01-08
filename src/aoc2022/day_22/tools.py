# coding=utf-8
"""Tools used for solving the Day 22: Monkey Map puzzle."""

# Set constants:
ARROWS = ["→", "↓", "←", "↑"]
ARROW_INVERSES = {"→": "←", "↓": "↑", "←": "→", "↑": "↓"}
ARROW_DELTAS = {"→": (0, 1), "←": (0, -1), "↓": (1, 0), "↑": (-1, 0)}
ARROW_VALUES = {"→": 0, "↓": 1, "←": 2, "↑": 3}
VALUE_ARROWS = {v: k for k, v in ARROW_VALUES.items()}

# Define type aliases:
Tile = tuple[int, int]
TilePair = list[tuple[Tile, Tile]]
Position = tuple[int, int, str]
Stripe = list[tuple[Position, str]]


class Traveller:
    """Symbolic figure walking across one Board."""
    def __init__(self, row: int, column: int, facing: str):
        self._positions = [(row, column, facing)]

    def __repr__(self) -> str:
        row, column, facing = self.position
        return f"({row},{column}) {facing}"

    def move(self, walked_positions: list[Position]):
        """Register new positions this Traveller has walked over."""
        self._positions.extend(walked_positions)

    def rotate(self, direction: str):
        """Rotate the current facing 90° clockwise (R) or anti-clockwise (L)."""
        change = 1 if direction == "R" else -1
        row, column, current_facing = self.position
        new_facing = VALUE_ARROWS[(ARROW_VALUES[current_facing] + change) % 4]
        self._positions.append((row, column, new_facing))

    @property
    def all_positions(self) -> list[Position]:
        """List all (row, column, facing) position this Traveller has been at."""
        return self._positions

    @property
    def position(self) -> Position:
        """Provide a tuple with the current row, column and facing of this Traveller."""
        return self._positions[-1]

    @property
    def pass_code(self) -> int:
        """Compose a numeric password from the current row, column and facing."""
        row, column, facing = self.position
        return (row + 1) * 1000 + (column + 1) * 4 + ARROW_VALUES[facing]


class Edge:
    """Line separating adjacent tiles belonging in different areas of a board."""
    __slots__ = ["_map_12", "_map_21", "_area_1", "_area_2", "_arrow"]

    def __init__(self, area_1: "Area", area_2: "Area", direction_12: str):
        self._area_1, self._area_2 = area_1.area_tile, area_2.area_tile
        self._arrow = direction_12
        paired_tiles = self._pair_borders(area_1=area_1, area_2=area_2)
        open_tiles = self._filter_walls(tiles=paired_tiles, area_1=area_1, area_2=area_2)
        self._map_12 = {t1: t2 for t1, t2 in open_tiles}
        self._map_21 = {t2: t1 for t1, t2 in open_tiles}

    def _pair_borders(self, area_1: "Area", area_2: "Area") -> TilePair:
        """Zip pairs of tiles across the shared border of the two areas."""
        border_1 = area_1.get_border_tiles(side=self._arrow)
        border_2 = area_2.get_border_tiles(side=ARROW_INVERSES[self._arrow])
        return [(tile_1, tile_2) for tile_1, tile_2 in zip(border_1, border_2)]

    @staticmethod
    def _filter_walls(tiles: TilePair, area_1: "Area", area_2: "Area") -> TilePair:
        """Remove tile pairs where one or both tiles are walls."""
        tiles = filter(lambda tp: area_1[tp[0]] != "#" and area_2[tp[1]] != "#", tiles)
        return list(tiles)

    def __repr__(self) -> str:
        return f"{self._area_1} {self._arrow} {self._area_2}"

    def warp_over(self, position: Position) -> Position:
        """For a known Position, return its corresponding warp Position."""
        row, col, facing = position
        if facing not in [self._arrow, ARROW_INVERSES[self._arrow]]:
            raise WarpError(position=position)
        warp_map = self._map_12 if facing == self._arrow else self._map_21
        try:
            row, col = warp_map[(row, col)]
        except KeyError:
            raise WarpError(position=position)
        return row, col, facing


class WarpError(KeyError):
    """Raised when warping over an Edge an unregistered position."""
    def __init__(self, position: Position):
        self.position = position

    def __str__(self) -> str:
        return f"The {self.position} position can't warp over this Edge."


class Area:
    """Each of 6 regular nxn subdomains in which a board can be decomposed."""
    def __init__(self, tile_rows: list[str], area_row: int, area_col: int):
        self._size = len(tile_rows)
        self._area_row, self._area_col = area_row, area_col
        top_row, left_col = area_row * self._size, area_col * self._size
        self._tiles_map = self._build_map(
            tile_rows=tile_rows, top_row=top_row, left_col=left_col)
        self._register_borders()
        self.edges = {k: None for k in ARROWS}

    def _build_map(self, tile_rows: list[str], top_row: int, left_col: int) \
            -> dict[Tile, str]:
        """Map the row and column of each provided tile to its value."""
        return {(top_row + (i // self._size), left_col + (i % self._size)): value
                for i, value in enumerate("".join(tile_rows))}

    def _register_borders(self):
        """Store the top|bottom rows and the left|right columns on this Area."""
        self._top = min(r for r, c in self._tiles_map.keys())
        self._bottom = max(r for r, c in self._tiles_map.keys())
        self._left = min(c for r, c in self._tiles_map.keys())
        self._right = max(c for r, c in self._tiles_map.keys())

    def __contains__(self, tile: Tile) -> bool:
        return tile in self._tiles_map.keys()

    def __getitem__(self, tile: Tile) -> str:
        return self._tiles_map[tile]

    def __repr__(self) -> str:
        return f"{self.area_tile}: {list(self._tiles_map.values())}"

    def get_border_tiles(self, side: str) -> list[Tile]:
        """List all tiles in this Area at its target side."""
        if side == "→":
            return [tile for tile in self._tiles_map.keys() if tile[1] == self.right]
        if side == "↓":
            return [tile for tile in self._tiles_map.keys() if tile[0] == self.bottom]
        if side == "←":
            return [tile for tile in self._tiles_map.keys() if tile[1] == self.left]
        if side == "↑":
            return [tile for tile in self._tiles_map.keys() if tile[0] == self.top]
        raise ValueError(f"Unknown '{side}' side.")

    def register_edge(self, side: str, edge: Edge):
        """Store the provided Edge at the given side of this Area."""
        assert side in ARROWS
        self.edges.update({side: edge})

    def walk_over(self, start: Position, n_steps: int) -> tuple[list[Position], int]:
        """From a start Position, walk a straight line until a wall or an Area edge."""
        row, col, facing = start
        d_row, d_col = ARROW_DELTAS[facing]
        walked_positions = []
        steps_to_edge = self._get_steps_to_edge(position=start)
        while n_steps:
            if len(walked_positions) == steps_to_edge:
                break  # About to warp over an Edge.
            n_steps -= 1
            row, col = row + d_row, col + d_col
            if self[(row, col)] == "#":
                return walked_positions, 0  # Facing a wall, no more walk to do.
            walked_positions.append((row, col, facing))
        return walked_positions, n_steps

    def _get_steps_to_edge(self, position: Position) -> int:
        """Get max line steps to the edge of this Area from the given Position."""
        row, col, facing = position
        if facing == "↓":
            return self.bottom - row
        if facing == "↑":
            return row - self.top
        if facing == "→":
            return self.right - col
        if facing == "←":
            return col - self.left

    @property
    def top(self) -> int:
        """Provide the top-most row inside this Area."""
        return self._top

    @property
    def bottom(self) -> int:
        """Provide the bottom-most row inside this Area."""
        return self._bottom

    @property
    def left(self) -> int:
        """Provide the left-most column inside this Area."""
        return self._left

    @property
    def right(self) -> int:
        """Provide the right-most column inside this Area."""
        return self._right

    @property
    def area_tile(self) -> Tile:
        """Provide the area row and column of this Area in the main Board."""
        return self._area_row, self._area_col

    @property
    def tiles(self) -> list[tuple[Tile, str]]:
        """Row and column tuple, and value, of each tile in this Area."""
        return [((r, c), v) for (r, c), v in self._tiles_map.items()]

    @property
    def is_void(self) -> bool:
        """Check if all tiles in this Area are off-map tiles."""
        return all(tile == " " for tile in self._tiles_map.values())

    @property
    def missing_edges(self) -> list[str]:
        """List those sides of this Area without a defined Edge."""
        return [side for side, edge in self.edges.items() if edge is None]


class Board:
    """Strangely-shaped board of open, walled and off-limits 2D tiles."""
    def __init__(self, board_rows: list[str], area_size: int):
        self._area_size = area_size
        self._areas_map = self._build_areas(rows=board_rows)
        self._register_borders()
        self._register_edges()

    def _build_areas(self, rows: list[str]) -> dict[Tile, "Area"]:
        """Assign each tile in this Board to one Area."""
        areas, size = {}, self._area_size
        for r in range(len(rows) // size):
            area_rows = rows[r * size:(r + 1) * size]
            for c in range(len(rows[0]) // size):
                area_tiles = [row[c * size: (c + 1) * size] for row in area_rows]
                area = Area(tile_rows=area_tiles, area_row=r, area_col=c)
                areas.update({(r, c): area})
        return areas

    def _register_borders(self):
        """Store the top|bottom rows and the left|right columns on this Area."""
        self._top = min(r for r, c in self._areas_map.keys())
        self._bottom = max(r for r, c in self._areas_map.keys())
        self._left = min(c for r, c in self._areas_map.keys())
        self._right = max(c for r, c in self._areas_map.keys())

    def _register_edges(self):
        """Register the Edge at the border of each stored Area with the rest of areas."""
        remaining_areas = [area for area in self.areas if not area.is_void]
        while remaining_areas:
            area = remaining_areas.pop(0)
            while area.missing_edges:
                side = area.missing_edges.pop(0)
                area_side = self._get_adjacent_area(area=area, side=side)
                edge = Edge(area_1=area, area_2=area_side, direction_12=side)
                area.register_edge(side=side, edge=edge)

    def _get_adjacent_area(self, area: Area, side: str) -> Area:
        """Get the first non-void Area located at the given side of the target Area."""
        area_row, area_col = area.area_tile
        d_row, d_col = ARROW_DELTAS[side]
        area_row, area_col = area_row + d_row, area_col + d_col
        side_area = self[(area_row, area_col)]
        if side_area.is_void:
            return self._get_adjacent_area(area=side_area, side=side)
        return side_area

    def __getitem__(self, area_tile: Tile) -> Area:
        row, col = self._adjust_tile(tile=area_tile)
        return self._areas_map[(row, col)]

    def _adjust_tile(self, tile: Tile) -> Tile:
        """Allow the Board area map to behave as a 2D cyclic map of tiles."""
        row, col = tile
        if row < self.top:
            row = self.bottom
        elif self.bottom < row:
            row = self.top
        if col < self.left:
            col = self.right
        elif self.right < col:
            col = self.left
        return row, col

    def spawn_traveller(self) -> "Traveller":
        """Create a new Traveller at the starting tile."""
        area = next(filter(lambda a: not a.is_void, self._areas_map.values()))
        return Traveller(row=area.top, column=area.left, facing="→")

    def simulate_walk(self, start: Position, n_steps: int) -> list[Position]:
        """New positions crossed when walking a straight line from a starting point."""
        row, col, facing = start
        current_area, total_walked = self._get_current_area(tile=(row, col)), []
        while n_steps:
            area_walked, n_steps = current_area.walk_over(
                start=(row, col, facing), n_steps=n_steps)
            total_walked.extend(area_walked)
            # If after walking an Area, any steps remain, an Edge must be reached.
            if n_steps and n_steps > 0:
                n_steps -= 1
                row, col, facing = total_walked[-1] if total_walked else start
                edge = current_area.edges[facing]
                try:
                    row, col, facing = edge.warp_over(position=(row, col, facing))
                except WarpError:  # Tried to warp onto a wall (or something went wrong).
                    return total_walked
                else:
                    current_area = self._get_current_area(tile=(row, col))
                    total_walked.append((row, col, facing))
        return total_walked

    def _get_current_area(self, tile: Tile) -> Area:
        """Find the Area containing the provided tile location."""
        for area in self._areas_map.values():
            if tile in area:
                return area
        raise KeyError(f"The {tile} tile doesn't belong to any known Area.")

    @property
    def areas(self) -> list[Area]:
        """List the areas of this Board."""
        return list(self._areas_map.values())

    @property
    def top(self) -> int:
        """Provide the top-most row inside this Area."""
        return self._top

    @property
    def bottom(self) -> int:
        """Provide the bottom-most row inside this Area."""
        return self._bottom

    @property
    def left(self) -> int:
        """Provide the left-most column inside this Area."""
        return self._left

    @property
    def right(self) -> int:
        """Provide the right-most column inside this Area."""
        return self._right

    @classmethod
    def from_notes(cls, monkey_notes: list[str], area_size: int) -> "Board":
        """Crate a new Board from the lines of notes handed by the monkeys."""
        board_notes = monkey_notes[:-2]
        m, n = len(board_notes), max(len(line) for line in board_notes)
        board_rows = [row + " " * (n - len(row)) for row in board_notes]
        return cls(board_rows=board_rows, area_size=area_size)


class WalkPlan:
    """Required walk and rotate actions for a Traveller to cross a Board."""
    def __init__(self, plan_stages: list[str]):
        self.stages = plan_stages

    def execute_plan(self, traveller: Traveller, board: "Board"):
        """Make a Traveller do each action in this WalkPlan sequentially."""
        for stage in self.stages:
            if stage.isdecimal():
                walked_positions = board.simulate_walk(
                    start=traveller.position, n_steps=int(stage))
                traveller.move(walked_positions=walked_positions)
            else:
                traveller.rotate(direction=stage)

    @classmethod
    def from_monkey_notes(cls, notes: list[str]) -> "WalkPlan":
        """Create a new WalkPlan from the lines of notes handed by the monkeys."""
        plan = notes[-1].replace("R", "|R|").replace("L", "|L|").replace("||", "|")
        return cls(plan_stages=plan.split("|"))
