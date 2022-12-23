# coding=utf-8
"""Tools used for solving the Day 18: Boiling Boulders puzzle."""


class Cell:
    """Block of size 1x1x1 representing a discrete location in a 3D grid."""
    __slots__ = ["x", "y", "z"]

    def __init__(self, x: int, y: int, z: int):
        self.x, self.y, self.z = x, y, z

    def __eq__(self, other: "Cell") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    @property
    def neighbour_cells(self) -> set["Cell"]:
        """Hypothetical cells that would be adjacent to each face of this Cell."""
        x, y, z = self.x, self.y, self.z
        d_xyz = [1, -1, 0, 0, 0, 0], [0, 0, 1, -1, 0, 0], [0, 0, 0, 0, 1, -1]
        return {Cell(x=x + dx, y=y + dy, z=z + dz) for dx, dy, dz in zip(*d_xyz)}

    @classmethod
    def from_string(cls, string: str) -> "Cell":
        """Create a new Cell from its string representation."""
        return cls(*map(int, string.split(",")))


class Droplet:
    """Blot of flying lava with a shape composed of cubic cells."""
    def __init__(self, cells: list[Cell]):
        self.cells = {*cells}

    @property
    def surface_area(self) -> int:
        """Sum of cells' faces on this Droplet not touching other cells."""
        return sum(len(cell.neighbour_cells - self.cells) for cell in self.cells)

    @classmethod
    def from_scan_output(cls, scan_output: list[str]) -> "Droplet":
        """Create a new Droplet from the string lines produced by your scanner."""
        return cls(cells=[Cell.from_string(string=line) for line in scan_output])
