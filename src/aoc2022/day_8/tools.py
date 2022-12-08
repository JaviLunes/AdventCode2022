# coding=utf-8
"""Tools used for solving the Day 8: Treetop Tree House puzzle."""

# Standard library imports:
from collections.abc import Callable
from functools import reduce

# Third party imports:
import numpy


class TreeGrid:
    """Patch of tall trees planted in a 2D regular grid by a previous expedition."""
    def __init__(self, height_strings: list[str]):
        self.array = self._process_height_strings(height_strings=height_strings)

    @staticmethod
    def _process_height_strings(height_strings: list[str]) -> numpy.ndarray:
        """Generate a 2D array of tree heights from a list of row strings."""
        m, n = len(height_strings), len(height_strings[0])
        flat_grid = numpy.fromiter(map(int, "".join(height_strings)), dtype=int)
        return flat_grid.reshape((m, n))

    @property
    def tree_visibility(self) -> numpy.ndarray:
        """Check which trees are visible from any direction from outside the TreeGrid."""
        return self._apply_reduce_views(func=self._is_visible, red_func=numpy.logical_or)

    @property
    def scenic_scores(self) -> numpy.ndarray:
        """Compute the product from all 4 directions of view distances for each tree."""
        return self._apply_reduce_views(func=self._view_distance, red_func=numpy.multiply)

    @staticmethod
    def _is_visible(array: numpy.ndarray) -> numpy.ndarray:
        """Check which trees are visible from the top side of the TreeGrid."""
        are_visible = numpy.zeros_like(array).astype(bool)
        are_visible[0, :] = True
        for i in range(1, are_visible.shape[0]):
            tallest_before = numpy.amax(array[:i, :], axis=0)
            are_visible[i, :] = tallest_before < array[i, :]
        return are_visible

    @staticmethod
    def _view_distance(array: numpy.ndarray) -> numpy.ndarray:
        """Count trees seen by each tree on the TreeGrid when looking towards top."""
        view_distance = numpy.zeros_like(array)
        view_distance[0, :] = 0
        for i in range(1, view_distance.shape[0]):
            for j in range(0, view_distance.shape[1]):
                v = 0
                for ii in range(i - 1, -1, -1):
                    v += 1
                    if array[i, j] <= array[ii, j]:
                        break
                view_distance[i, j] = v
        return view_distance

    def _apply_reduce_views(self, func: Callable, red_func: Callable) -> numpy.ndarray:
        """Apply a function to all 4 views of the heights array, then combine results."""
        v_1 = self._change_view(func=func, axis=0, reverse=False)
        v_2 = self._change_view(func=func, axis=0, reverse=True)
        v_3 = self._change_view(func=func, axis=1, reverse=False)
        v_4 = self._change_view(func=func, axis=1, reverse=True)
        return reduce(red_func, [v_1, v_2, v_3, v_4])

    def _change_view(self, func: Callable, axis: int, reverse: bool) -> numpy.ndarray:
        """Apply a function to the heights array, viewed from a particular side."""
        array = self.array
        # Transform array to 'top view':
        if axis == 1:
            array = array.T
        if reverse:
            array = numpy.flip(array, axis=0)
        # Compute output array:
        output = func(array=array)
        # Transform output array back to original view:
        if reverse:
            output = numpy.flip(output, axis=0)
        if axis == 1:
            output = output.T
        return output
