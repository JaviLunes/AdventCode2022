# coding=utf-8
"""Visualizations for the Day 24: Blizzard Basin puzzle."""

# Standard library imports:
from collections import Counter

# Third party imports:
from aoc_tools.visualizations.grid_blocks import CellND, Grid2DPlotter
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_24.tools import Expedition, Valley

# Set constants:
ARROW_MAP = {"^": "↑", ">": "→", "v": "↓", "<": "←"}
CELL_COLOURS = {
    "Open": (200, 245, 255), "Blizzard": (0, 176, 240), "Mountain": (100, 0, 0),
    "Start": (0, 255, 0), "Goal": (0, 0, 255), "Expedition": (255, 0, 0)}

# Define custom types:
CellMap = dict[tuple[int, int], CellND]


def plot_expedition(valley: Valley, expedition: Expedition, t: int) -> Figure:
    """Plot the location of the Expedition on the Valley at a given instant."""
    cell_map = _build_valley_cells(valley=valley, t=t)
    _add_expedition(cell_map=cell_map, expedition=expedition, t=t)
    return _make_plot(cell_map=cell_map)


def _build_valley_cells(valley: Valley, t: int) -> CellMap:
    """Create one cell for each location in the valley, and map it to its coordinates."""
    # Map mountains:
    cells_map = {(wall.x, wall.y): CellND(x=wall.x, y=wall.y, value="Mountain")
                 for wall in valley.mountains}
    # Add start and goal points:
    x_s, y_s = valley.start.x, valley.start.y
    x_g, y_g = valley.goal.x, valley.goal.y
    cells_map.update({(x_s, y_s): CellND(x=x_s, y=y_s, value="Start", annotation="S")})
    cells_map.update({(x_g, y_g): CellND(x=x_g, y=y_g, value="Goal", annotation="G")})
    # Add blizzards:
    for blz, count in Counter(valley.snow_map.forecast_blizzards(t=t)).items():
        text = str(count) if count > 1 else ARROW_MAP[blz.direction]
        cell = CellND(x=blz.x, y=blz.y, value="Blizzard", annotation=text)
        cells_map.update({(blz.x, blz.y): cell})
    return cells_map


def _add_expedition(cell_map: CellMap, expedition: Expedition, t: int):
    """Add one cell representing the Expedition's location to the cell map."""
    cell = expedition.lineage[::-1][t].cell
    x, y = cell.x, cell.y
    cell_map.update({(x, y): CellND(x=x, y=y, value="Expedition", annotation="E")})


def _make_plot(cell_map: CellMap) -> Figure:
    """Use a plotter tool to create the plot, and customize it."""
    plotter = Grid2DPlotter(
        cells=cell_map.values(), empty_value="Open", palette=CELL_COLOURS,
        legend=False, title=False, annotations_kwargs=dict(
            size=32, color="black", weight="bold", ha="center", va="center"))
    fig = plotter.plot_xy()
    fig.tight_layout(pad=0.25)
    return fig
