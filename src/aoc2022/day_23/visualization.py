# coding=utf-8
"""Visualizations for the Day 23: Unstable Diffusion puzzle."""

# Third party imports:
from aoc_tools.visualizations.grid_blocks import CellND, Grid2DPlotter
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_23.tools import ElfGrove

# Set constants:
CELL_COLOURS = {"Empty": (255, 245, 245), "Elf": (255, 0, 0), "Planned": (100, 200, 255)}


def plot_grove(grove: ElfGrove) -> Figure:
    """Plot the tiles of an ElfGrove as 2D cells in a mosaic tessellation."""
    cells = _build_elf_cells(grove=grove)
    plotter = Grid2DPlotter(
        cells=cells, empty_value="Empty", palette=CELL_COLOURS,
        legend=True, title=False)
    fig = plotter.plot_xy()
    fig.tight_layout(pad=0.25)
    return fig


def _build_elf_cells(grove: ElfGrove) -> list[CellND]:
    """Create two cells for the current and planned positions of each Elf."""
    cells = []
    for elf in grove.elves:
        (xc, yc), (xp, yp) = elf.position, elf.planned_position
        cells.append(CellND(x=xp, y=yp, value="Planned"))
        cells.append(CellND(x=xc, y=yc, value="Elf"))
    return cells
