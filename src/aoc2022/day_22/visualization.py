# coding=utf-8
"""Visualizations for the Day 22: Monkey Map puzzle."""

# Third party imports:
from aoc_tools.visualizations.grid_blocks import CellND, Grid2DPlotter
from matplotlib.figure import Figure

# Local application imports:
from aoc2022.day_22.tools import BoardTraveller, MonkeyBoard

# Set constants:
CELL_COLOURS = {"Open": (255, 245, 245), "Traveller": (255, 0, 0),
                "Trail": (100, 200, 255), "Wall": (150, 75, 40), "Off-map": (0, 30, 50)}
TILE_NAMES = {" ": "Off-map", ".": "Open", "#": "Wall"}

CellMap = dict[tuple[int, int], CellND]


def plot_board(board: MonkeyBoard) -> Figure:
    """Plot the tiles of a MonkeyBoard as 2D cells in a mosaic tessellation."""
    cells = _build_board_cells(board=board).values()
    plotter = Grid2DPlotter(
        cells=cells, empty_value="Undefined", palette=CELL_COLOURS,
        legend=True, title=False)
    fig = plotter.plot_xy()
    fig.axes[0].invert_yaxis()
    fig.tight_layout(pad=0.25)
    return fig


def plot_traveller(traveller: BoardTraveller) -> Figure:
    """Plot the current location of a BoardTraveller at its MonkeyBoard."""
    cells = _build_board_cells(board=traveller.board)
    cells.update(_build_traveller_cells(traveller=traveller))
    plotter = Grid2DPlotter(
        cells=cells.values(), palette=CELL_COLOURS, empty_value="Undefined",
        legend=True, title=False, annotations_kwargs=dict(
            size=24, color="white", weight="bold", ha="center", va="center"))
    fig = plotter.plot_xy()
    fig.axes[0].invert_yaxis()
    fig.tight_layout(pad=0.25)
    return fig


def _build_board_cells(board: MonkeyBoard) -> CellMap:
    """Create one cell for each tile in the board, and map it to its row and column."""
    rows, columns = board.shape
    return {(row, col): CellND(x=col, y=row, value=TILE_NAMES[board.rows[row][col]])
            for col in range(columns) for row in range(rows)}


def _build_traveller_cells(traveller: BoardTraveller) -> CellMap:
    """Create cells holding the traveller's current and past positions in the board."""
    current = len(traveller.all_coordinates) - 1
    return {(row, col): CellND(
        x=col, y=row, value="Traveller" if i == current else "Trail", annotation=facing)
        for i, (row, col, facing) in enumerate(traveller.all_coordinates)}
