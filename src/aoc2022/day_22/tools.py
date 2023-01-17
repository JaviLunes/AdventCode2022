# coding=utf-8
"""Tools used for solving the Day 22: Monkey Map puzzle."""

# Standard library imports:
from enum import Enum
from itertools import count
from string import ascii_lowercase

# Define type aliases:
Tile = tuple[int, int]
Cell = tuple[Tile, str]
TilePair = tuple[Tile, Tile]


class Arrow(Enum):
    """Linear movement in an orthogonal direction."""
    RIGHT = "→", (0, 1)
    DOWN = "↓", (1, 0)
    LEFT = "←", (0, -1)
    UP = "↑", (-1, 0)

    def __new__(cls, arrow: str, deltas: tuple[int, int]) -> "Arrow":
        order = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = order
        obj._arrow = arrow
        obj._order = order
        obj._deltas = deltas
        return obj

    def __repr__(self) -> str:
        return self._arrow

    def __str__(self) -> str:
        return self._arrow
        
    def rotate(self, clockwise: bool) -> "Arrow":
        """Get the next (clockwise) or previous (anti-clockwise) defined Arrow."""
        return Arrow((self._order + (1 if clockwise else -1)) % len(Arrow))

    @property
    def code(self) -> int:
        """Value assigned to this Arrow for pass-code-computing purposes."""
        return self._order

    @property
    def deltas(self) -> Tile:
        """Row and column changes of a one-tile movement in this Arrow's direction."""
        return self._deltas

    @property
    def inverse(self) -> "Arrow":
        """Arrow pointing in the opposite direction of this Arrow."""
        return Arrow((self._order + 2) % len(Arrow))

    @classmethod
    def from_str_arrow(cls, arrow_str: str) -> "Arrow":
        """Find the Arrow with the arrow string representation matching the given one."""
        for arrow in cls:
            if arrow._arrow == arrow_str:
                return arrow
        raise ValueError(f"No Arrow has the provided {arrow_str} arrow string.")


class Traveller:
    """Symbolic figure walking across one Board."""
    def __init__(self, row: int, column: int, facing: Arrow):
        self._positions = [((row, column), facing)]
        self.steps_to_walk = 0

    def __repr__(self) -> str:
        (row, column), facing = self.position
        if self.steps_to_walk:
            return f"({row},{column}) {facing} [{self.steps_to_walk} steps remain]"
        return f"({row},{column}) {facing}"

    def move(self, walked_positions: list[tuple[Tile, Arrow]]):
        """Register new positions this Traveller has walked over."""
        self._positions.extend(walked_positions)
        self.steps_to_walk -= len(walked_positions)

    def rotate(self, direction: str):
        """Rotate the current facing 90° clockwise (R) or anti-clockwise (L)."""
        tile, current_facing = self.position
        new_facing = current_facing.rotate(clockwise=direction == "R")
        self._positions.append((tile, new_facing))

    @property
    def all_positions(self) -> list[tuple[Tile, Arrow]]:
        """List all ((row, column), facing) positions this Traveller has been at."""
        return self._positions

    @property
    def position(self) -> tuple[Tile, Arrow]:
        """Provide the current row, column and facing of this Traveller."""
        return self._positions[-1]

    @property
    def pass_code(self) -> int:
        """Compose a numeric password from the current row, column and facing."""
        (row, column), facing = self.position
        return (row + 1) * 1000 + (column + 1) * 4 + facing.code


class Edge:
    """Line separating adjacent tiles belonging in different areas of a board."""
    __slots__ = ["cells_in", "cells_out", "facing_in", "facing_out",
                 "area_in", "area_out", "map", "id_"]

    def __init__(self, id_: str, cells_in: list[Cell], cells_out: list[Cell],
                 facing_in: Arrow, facing_out: Arrow, area_tile_in: Tile,
                 area_tile_out: Tile):
        self.id_ = id_
        self.cells_in, self.cells_out = self._filter_walls(
            cells_in=cells_in, cells_out=cells_out)
        self.facing_in, self.facing_out = facing_in, facing_out
        self.area_in, self.area_out = area_tile_in, area_tile_out
        paired_tiles = self._pair_borders()
        self.map = {tl1: tl2 for tl1, tl2 in paired_tiles}

    @staticmethod
    def _filter_walls(cells_in: list[Cell], cells_out: list[Cell]) \
            -> tuple[list[Cell], list[Cell]]:
        """Remove cell pairs where any member is a wall cell."""
        zipped = zip(cells_in, cells_out)
        cells_in, cells_out = zip(*[
            (c1, c2) for c1, c2 in zipped if c1[1] != "#" and c2[1] != "#"])
        return cells_in, cells_out

    def _pair_borders(self) -> list[TilePair]:
        """Zip pairs of tiles across the shared border of the two areas."""
        return [((r1, c1), (r2, c2)) for ((r1, c1), v1), ((r2, c2), v2)
                in zip(self.cells_in, self.cells_out) if v1 != "#" and v2 != "#"]

    def __repr__(self) -> str:
        return f"E{self.id_} {self.facing_in}"

    def warp_over(self, traveller: Traveller) -> Tile:
        """For a known row, column and facing, move to its linked warp position."""
        tile, facing = traveller.position
        if facing != self.facing_in:
            raise WarpError(traveller=traveller)
        try:
            tile = self.map[tile]
        except KeyError:
            raise WarpError(traveller=traveller)
        traveller.move(walked_positions=[(tile, self.facing_out)])
        return self.area_out

    @property
    def inverse(self) -> "Edge":
        """New Edge linking the same two area borders, with inverted in/out roles."""
        return Edge(
            id_=self.id_, cells_in=self.cells_out, cells_out=self.cells_in,
            facing_in=self.facing_out.inverse, facing_out=self.facing_in.inverse,
            area_tile_in=self.area_out, area_tile_out=self.area_in)


class WarpError(KeyError):
    """Raised when warping over an Edge an unregistered position."""
    def __init__(self, traveller: Traveller):
        self.traveller = traveller

    def __str__(self) -> str:
        return f"The {self.traveller} traveller can't warp over this Edge."


class Area:
    """Each of 6 regular nxn subdomains in which a board can be decomposed."""
    def __init__(self, rows: list[str], area_row: int, area_col: int):
        self._size = len(rows)
        self._area_row, self._area_col = area_row, area_col
        self._register_borders()
        self._map = self._build_map(tile_rows=rows)
        self.edges = {direction: None for direction in Arrow}

    def _build_map(self, tile_rows: list[str]) -> dict[Tile, str]:
        """Map the row and column of each provided tile to its value."""
        return {(self._top + (i // self._size), self._left + (i % self._size)): value
                for i, value in enumerate("".join(tile_rows))}

    def _register_borders(self):
        """Store the top|bottom rows and the left|right columns on this Area."""
        self._top = self._area_row * self._size
        self._bottom = self._top + self._size - 1
        self._left = self._area_col * self._size
        self._right = self._left + self._size - 1

    def __repr__(self) -> str:
        edges = [repr(self.edges[direction]) for direction in Arrow]
        return f"{self.area_tile}: {edges}"

    def get_border_tiles(self, side: Arrow) -> list[tuple[Tile, str]]:
        """List all tiles (with their tile value) in this Area at its target side."""
        if side is Arrow.RIGHT:
            return [((r, c), v) for (r, c), v in self._map.items() if c == self._right]
        if side is Arrow.DOWN:
            return [((r, c), v) for (r, c), v in self._map.items() if r == self._bottom]
        if side is Arrow.LEFT:
            return [((r, c), v) for (r, c), v in self._map.items() if c == self._left]
        if side is Arrow.UP:
            return [((r, c), v) for (r, c), v in self._map.items() if r == self._top]
        raise ValueError(f"Unknown '{side}' side.")

    def register_edge(self, side: Arrow, edge: Edge):
        """Store the provided Edge at the given side of this Area."""
        self.edges.update({side: edge})

    def walk_over(self, traveller: Traveller):
        """Walk a straight line until the Traveller hits a wall or reaches an Edge."""
        (row, col), facing = traveller.position
        d_row, d_col = facing.deltas
        walked_tiles, walked_into_wall = [], False
        steps_to_edge = self._get_steps_to_edge(traveller=traveller)
        while len(walked_tiles) < traveller.steps_to_walk:
            if len(walked_tiles) == steps_to_edge:  # About to warp over an Edge.
                break
            row, col = row + d_row, col + d_col
            if self._map[(row, col)] == "#":  # Facing a wall, no more walk to do.
                walked_into_wall = True
                break
            walked_tiles.append((row, col))
        walked_positions = [((row, col), facing) for row, col in walked_tiles]
        traveller.move(walked_positions=walked_positions)
        if walked_into_wall:
            traveller.steps_to_walk = 0

    def _get_steps_to_edge(self, traveller: Traveller) -> int:
        """Get the max steps from the Traveller to the faced edge of this Area."""
        (row, col), facing = traveller.position
        if facing is Arrow.RIGHT:
            return self._right - col
        if facing is Arrow.DOWN:
            return self._bottom - row
        if facing is Arrow.LEFT:
            return col - self._left
        if facing is Arrow.UP:
            return row - self._top
        raise ValueError(f"Unknown '{facing}' facing.")

    @property
    def top(self) -> int:
        """Provide the top-most row inside this Area."""
        return self._top

    @property
    def left(self) -> int:
        """Provide the left-most column inside this Area."""
        return self._left

    @property
    def area_tile(self) -> Tile:
        """Provide the area row and column of this Area in the main Board."""
        return self._area_row, self._area_col

    @property
    def tiles(self) -> list[tuple[Tile, str]]:
        """Row and column tuple, and value, of each tile in this Area."""
        return [((r, c), v) for (r, c), v in self._map.items()]

    @property
    def is_void(self) -> bool:
        """Check if all tiles in this Area are off-map tiles."""
        return all(tile == " " for tile in self._map.values())

    @property
    def missing_edges(self) -> list[Arrow]:
        """List those sides of this Area without a defined Edge."""
        return [side for side, edge in self.edges.items() if edge is None]


class Board:
    """Strangely-shaped board of open, walled and off-limits 2D tiles."""
    def __init__(self, rows: list[str], area_size: int, cube_mode: bool,
                 hardcoded_edges: dict = None):
        self._edge_count = count(0)
        self._sizes = len(rows) // area_size, len(rows[0]) // area_size
        self._area_size = area_size
        self._register_borders()
        self._register_areas(rows=rows)
        self._register_edges(cube_mode=cube_mode, hardcoded_edges=hardcoded_edges)
        self._current_area = None

    def _register_areas(self, rows: list[str]):
        """Assign each tile in this Board to one Area."""
        areas, size = {}, self._area_size
        for r in range(self._sizes[0]):
            area_rows = rows[r * size:(r + 1) * size]
            for c in range(self._sizes[1]):
                area_tiles = [row[c * size: (c + 1) * size] for row in area_rows]
                area = Area(rows=area_tiles, area_row=r, area_col=c)
                if area.is_void:
                    continue
                areas.update({(r, c): area})
        self._map = areas

    def _register_borders(self):
        """Store the top|bottom rows and the left|right columns on this Area."""
        self._top, self._left = 0, 0
        self._bottom, self._right = self._sizes[0] - 1, self._sizes[1] - 1

    def _register_edges(self, cube_mode: bool, hardcoded_edges: dict):
        """Register the Edge at the border of each stored Area with the rest of areas."""
        if cube_mode:
            self._register_cube_edges(hardcoded_edges=hardcoded_edges)
        else:
            self._register_plane_edges()

    def _register_cube_edges(self, hardcoded_edges: dict):
        """Build edges for this Board assuming each Area is a face in a 3D cube."""
        for aaa, bbb in hardcoded_edges.items():
            # Extract hardcoded data:
            area_tile_in, facing_in = aaa
            area_tile_out, facing_out, inverted_out = bbb.values()
            # Parse hardcoded data:
            area_in, area_out = self._map[area_tile_in], self._map[area_tile_out]
            facing_in = Arrow.from_str_arrow(arrow_str=facing_in)
            facing_out = Arrow.from_str_arrow(arrow_str=facing_out)
            cells_in = area_in.get_border_tiles(side=facing_in)
            cells_out = area_out.get_border_tiles(side=facing_out.inverse)
            if inverted_out:
                cells_out = cells_out[::-1]
            # Build and register edge:
            id_ = ascii_lowercase[next(self._edge_count)]
            edge = Edge(
                id_=id_, cells_in=cells_in, cells_out=cells_out,
                facing_in=facing_in, facing_out=facing_out,
                area_tile_in=area_tile_in, area_tile_out=area_tile_out)
            area_in.register_edge(side=facing_in, edge=edge)
            area_out.register_edge(side=facing_out.inverse, edge=edge.inverse)

    def _register_plane_edges(self):
        """Build edges for this Board assuming all areas are in the same 2D plane."""
        remaining_areas = self.areas
        while remaining_areas:
            area = remaining_areas.pop(0)
            while area.missing_edges:
                side = area.missing_edges.pop(0)
                area_side = self._get_adjacent_plane_area(area=area, side=side)
                id_ = ascii_lowercase[next(self._edge_count)]
                edge = Edge(
                    id_=id_, cells_in=area.get_border_tiles(side=side),
                    cells_out=area_side.get_border_tiles(side=side.inverse),
                    facing_in=side, facing_out=side,
                    area_tile_in=area.area_tile, area_tile_out=area_side.area_tile)
                area.register_edge(side=side, edge=edge)
                area_side.register_edge(side=side.inverse, edge=edge.inverse)

    def _get_adjacent_plane_area(self, area: Area, side: Arrow) -> Area:
        """Get the first non-void Area located at the given side of the target Area."""
        area_row, area_col = area.area_tile
        while True:
            area_row, area_col = area_row + side.deltas[0], area_col + side.deltas[1]
            area_row, area_col = self._adjust_tile(tile=(area_row, area_col))
            try:
                return self._map[(area_row, area_col)]
            except KeyError:
                continue

    def _adjust_tile(self, tile: Tile) -> Tile:
        """Allow the Board area map to behave as a 2D cyclic map of tiles."""
        row, col = tile
        if row < self._top:
            row = self._bottom
        elif self._bottom < row:
            row = self._top
        if col < self._left:
            col = self._right
        elif self._right < col:
            col = self._left
        return row, col

    def spawn_traveller(self) -> "Traveller":
        """Create a new Traveller at the starting tile."""
        area = next(filter(lambda a: not a.is_void, self._map.values()))
        self._current_area = area
        return Traveller(row=area.top, column=area.left, facing=Arrow.RIGHT)

    def walk_over(self, traveller: Traveller):
        """Move the Traveller a straight line until it has no more steps to walk."""
        while traveller.steps_to_walk:
            self._current_area.walk_over(traveller=traveller)
            # If after walking an Area, any steps remain, an Edge must be reached.
            if traveller.steps_to_walk:
                _, facing = traveller.position
                edge = self._current_area.edges[facing]
                try:
                    new_area_tile = edge.warp_over(traveller=traveller)
                    new_area = self._map[new_area_tile]
                except WarpError:  # Tried to warp onto a wall (or something went wrong).
                    break
                else:
                    self._current_area = new_area

    @property
    def areas(self) -> list[Area]:
        """List the areas of this Board."""
        return list(self._map.values())

    @classmethod
    def from_notes(cls, notes: list[str], area_size: int, cube_mode: bool,
                   hardcoded_edges: dict = None) -> "Board":
        """Crate a new Board from the lines of notes handed by the monkeys."""
        board_notes = notes[:-2]
        m, n = len(board_notes), max(len(line) for line in board_notes)
        board_rows = [row + " " * (n - len(row)) for row in board_notes]
        return cls(rows=board_rows, area_size=area_size, cube_mode=cube_mode,
                   hardcoded_edges=hardcoded_edges)


class WalkPlan:
    """Required walk and rotate actions for a Traveller to cross a Board."""
    def __init__(self, plan_stages: list[str]):
        self.stages = plan_stages

    def execute_plan(self, traveller: Traveller, board: "Board"):
        """Make a Traveller do each action in this WalkPlan sequentially."""
        for stage in self.stages:
            if stage.isdecimal():
                traveller.steps_to_walk = int(stage)
                board.walk_over(traveller=traveller)
            else:
                traveller.rotate(direction=stage)

    @classmethod
    def from_monkey_notes(cls, notes: list[str]) -> "WalkPlan":
        """Create a new WalkPlan from the lines of notes handed by the monkeys."""
        plan = notes[-1].replace("R", "|R|").replace("L", "|L|").replace("||", "|")
        return cls(plan_stages=plan.split("|"))
