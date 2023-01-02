# coding=utf-8
"""Tools used for solving the Day 18: Boiling Boulders puzzle."""

# Standard library imports:
from itertools import product

# Third party imports:
from aoc_tools.algorithms.full_search import FNode, full_search


class Cell(FNode):
    """Block of size 1x1x1 representing a discrete location in a 3D grid."""
    __slots__ = ["x", "y", "z", "_domain"]

    def __init__(self, x: int, y: int, z: int, domain: "Domain" = None):
        self.x, self.y, self.z = x, y, z
        self._domain = domain

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: "Cell") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    @property
    def id(self) -> str:
        """Provide a string identifier unique to this FNode."""
        return f"{self.x},{self.y},{self.z}"

    def get_successors(self) -> set["Cell"]:
        """Hypothetical cells that would be adjacent to each face of this Cell."""
        return self.adjacent_cells - self._domain.occupied

    @property
    def adjacent_cells(self) -> set["Cell"]:
        """Set of cells within the domain adjacent to any of this Cell's faces."""
        d_xyz = [1, -1, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0], [0, 0, 0, 0, 1, -1]
        cells = set()
        for dx, dy, dz in zip(*d_xyz):
            x, y, z = self.x + dx, self.y + dy, self.z + dz
            cell = Cell(x=x, y=y, z=z, domain=self._domain)
            if self._domain is not None and cell not in self._domain:
                continue
            cells.add(cell)
        return cells

    @classmethod
    def from_string(cls, string: str) -> "Cell":
        """Create a new Cell from its string representation."""
        return cls(*map(int, string.split(",")))


class Domain:
    """Define and limit the 3D surroundings of a set of cells."""
    __slots__ = ["_min_x", "_max_x", "_min_y", "_max_y", "_min_z", "_max_z", "occupied"]

    def __init__(self, occupied_cells: set[Cell]):
        x_values = sorted(cell.x for cell in occupied_cells)
        y_values = sorted(cell.y for cell in occupied_cells)
        z_values = sorted(cell.z for cell in occupied_cells)
        self._min_x, self._max_x = x_values[0], x_values[-1]
        self._min_y, self._max_y = y_values[0], y_values[-1]
        self._min_z, self._max_z = z_values[0], z_values[-1]
        self.occupied = occupied_cells

    def __contains__(self, cell: "Cell") -> bool:
        x_within = cell.x in self.x_range_ext
        y_within = cell.y in self.y_range_ext
        z_within = cell.z in self.z_range_ext
        return x_within and y_within and z_within

    @property
    def all_cells(self) -> set[Cell]:
        """Generate all cells within the limits of this Domain."""
        xyz_iter = product(self.x_range_ext, self.y_range_ext, self.z_range_ext)
        return {Cell(*xyz, domain=self) for xyz in xyz_iter}

    @property
    def extended_domain_origin(self) -> Cell:
        """Cell at the minimum coordinates of this Domain's limits."""
        x, y, z = self._min_x - 1, self._min_y - 1, self._min_z - 1
        return Cell(x=x, y=y, z=z, domain=self)

    @property
    def x_range_ext(self) -> range:
        """X range spanning from one location under min X to one location over max X."""
        return range(self._min_x - 1, self._max_x + 2)

    @property
    def y_range_ext(self) -> range:
        """Y range spanning from one location under min Y to one location over max Y."""
        return range(self._min_y - 1, self._max_y + 2)

    @property
    def z_range_ext(self) -> range:
        """Z range spanning from one location under min Z to one location over max Z."""
        return range(self._min_z - 1, self._max_z + 2)


class Droplet:
    """Blot of flying lava with a shape composed of cubic cells."""
    def __init__(self, cells: set[Cell]):
        self.region = Domain(occupied_cells=cells)
        self.lava = cells
        self.outside = full_search(start=self.region.extended_domain_origin)
        self.pockets = self.region.all_cells - self.outside - self.lava

    @property
    def surface_area(self) -> int:
        """Faces of lava cells on this Droplet not touching other lava cells."""
        return sum(len(cell.adjacent_cells - self.lava) for cell in self.lava)

    @property
    def external_surface_area(self) -> int:
        """Faces of lava cells on this Droplet touching the exterior air cells."""
        internal = self.lava | self.pockets
        return sum(len(cell.adjacent_cells - internal) for cell in self.lava)

    @classmethod
    def from_scan_output(cls, scan_output: list[str]) -> "Droplet":
        """Create a new Droplet from the string lines produced by your scanner."""
        return cls(cells={Cell.from_string(string=line) for line in scan_output})
