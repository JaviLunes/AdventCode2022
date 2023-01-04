# coding=utf-8
"""Visualizations for the Day 22: Monkey Map puzzle."""

# Third party imports:
from aoc_tools.visualizations.grid_blocks import CellND, Grid2DPlotter
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_22.tools import MonkeyBoard

# Set constants:
TILE_COLOURS = {"Off-map": (0, 30, 50), "Open": (255, 245, 245), "Wall": (150, 75, 40)}
TILE_NAMES = {" ": "Off-map", ".": "Open", "#": "Wall"}


def plot_board(board: MonkeyBoard) -> Figure:
    """Plot the tiles of a MonkeyBoard as 2D cells in a mosaic tessellation."""
    # Create tessellation:
    cells = list(_build_board_cells(board=board).values())
    plotter = Grid2DPlotter(cells=cells, empty_value="Undefined", palette=TILE_COLOURS)
    fig = plotter.plot_xy()
    # Tweak figure:
    fig.axes[0].title.set_visible(False)
    fig.axes[0].invert_yaxis()
    fig.tight_layout(pad=0.25)
    return fig


def _build_board_cells(board: MonkeyBoard) -> dict[tuple[int, int], CellND]:
    """Create one cell for each tile in the board, and map it to its row and column."""
    rows, columns = board.shape
    return {(row, col): CellND(x=col, y=row, value=TILE_NAMES[board.rows[row][col]])
            for col in range(columns) for row in range(rows)}
