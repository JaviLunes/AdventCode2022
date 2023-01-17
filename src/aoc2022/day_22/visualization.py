# coding=utf-8
"""Visualizations for the Day 22: Monkey Map puzzle."""

# Third party imports:
from aoc_tools.visualizations.grid_blocks import CellND, Grid2DPlotter
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_22.tools import Traveller, Board

# Set constants:
CELL_COLOURS = {
    "Open_A": (255, 200, 200), "Wall_A": (255, 0, 0),
    "Open_B": (255, 255, 200), "Wall_B": (255, 255, 0),
    "Open_C": (200, 255, 225), "Wall_C": (0, 176, 80),
    "Open_D": (200, 245, 255), "Wall_D": (0, 176, 240),
    "Open_E": (235, 220, 245), "Wall_E": (112, 48, 160),
    "Open_F": (255, 235, 180), "Wall_F": (255, 192, 0),
    "Traveller": (50, 50, 50), "Trail": (200, 200, 200), "Off-map": (0, 30, 50)}
TILE_NAMES = {" ": "Off-map", ".": "Open", "#": "Wall"}


def plot_board(board: Board) -> Figure:
    """Plot the tiles of a Board as 2D cells in a mosaic tessellation."""
    cells = _build_board_cells(board=board).values()
    plotter = Grid2DPlotter(
        cells=cells, empty_value="Off-map", palette=CELL_COLOURS,
        legend=False, title=False)
    fig = plotter.plot_xy()
    fig.axes[0].invert_yaxis()
    fig.tight_layout(pad=0.25)
    return fig


def plot_traveller(traveller: Traveller, board: Board) -> Figure:
    """Plot the current location of a BoardTraveller at its Board."""
    cells = _build_board_cells(board=board)
    cells.update(_build_traveller_cells(traveller=traveller))
    plotter = Grid2DPlotter(
        cells=cells.values(), palette=CELL_COLOURS, empty_value="Off-map",
        legend=False, title=False, annotations_kwargs=dict(
            size=24, color="white", weight="bold", ha="center", va="center"))
    fig = plotter.plot_xy()
    fig.axes[0].invert_yaxis()
    fig.tight_layout(pad=0.25)
    return fig


def _build_board_cells(board: Board) -> dict[tuple[int, int], CellND]:
    """Create one cell for each tile in the board, and map it to its row and column."""
    cells_map, area_names = {}, iter("ABCDEF")
    for area in board.areas:
        suffix = f"_{next(area_names)}"
        items = ((row, col, TILE_NAMES[v] + suffix) for (row, col), v in area.tiles)
        cells_map.update({(r, c): CellND(x=c, y=r, value=v) for r, c, v in items})
    return cells_map


def _build_traveller_cells(traveller: Traveller) -> dict[tuple[int, int], CellND]:
    """Create cells holding the traveller's current and past positions in the board."""
    current = len(traveller.all_positions) - 1
    return {(row, col): CellND(
        x=col, y=row, annotation=str(facing),
        value="Traveller" if i == current else "Trail")
            for i, ((row, col), facing) in enumerate(traveller.all_positions)}
