# coding=utf-8
"""Tools used for solving the Day 10: Cathode-Ray Tube puzzle."""

# Third party imports:
from aoc_tools.algorithms.pixel_parsing import PixelParser


class CPURegister:
    """Simple CPU storing a register of integer values and driven by a clock circuit."""
    def __init__(self, program: list[str]):
        self.xs = self._process_program(program=program)

    def _process_program(self, program: list[str]) -> list[int]:
        """Generate the cycle-series of X values by applying the provided program."""
        xs = [1, 1]
        for instruction in program:
            xs, current_x = xs[:-1], xs[-1]
            new_x = self._do_instruction(instruction=instruction, current_x=current_x)
            xs.extend(new_x)
        return xs

    def _do_instruction(self, instruction: str, current_x: int) -> list[int]:
        """Identify and execute the provided instruction."""
        if instruction == "noop":
            return self._do_noop(current_x=current_x)
        else:
            value = int(instruction.split(" ")[1])
            return self._do_addx(current_x=current_x, value=value)

    @staticmethod
    def _do_noop(current_x: int) -> list[int]:
        """Generate the results for executing a 'noop' instruction."""
        return [current_x, current_x]

    # noinspection SpellCheckingInspection
    @staticmethod
    def _do_addx(current_x: int, value: int) -> list[int]:
        """Generate the results for executing an 'addx' instruction."""
        return [current_x, current_x, current_x + value]

    @property
    def signal_strength(self) -> list[int]:
        """Provide the signal strength values for all cycles in the register."""
        return [i * x_value for i, x_value in enumerate(self.xs)]

    @property
    def significant_strength(self) -> int:
        """Provide the sum of signal strength values at the significant cycles."""
        s = self.signal_strength
        return s[20] + s[60] + s[100] + s[140] + s[180] + s[220]


class CRTScreen:
    """Cathode-ray-tube-like device system using rows of on/off pixels to show text."""
    _parser = PixelParser(on_pixel="#", off_pixel=".")

    def __init__(self, register: CPURegister):
        self.register = register
        self.pixels = self._process_lines()

    def _process_lines(self) -> list[str]:
        """Generate a 40x6 pixels image based on the X values of the CPURegister."""
        h, w = 6, 40
        xs_lines = [self.register.xs[1:-1][i:i + w] for i in range(0, h * w, w)]
        return [self._process_line(x_values=xs_line) for xs_line in xs_lines]

    @staticmethod
    def _process_line(x_values: list[int]) -> str:
        """Use provided X values to control a sprite and build a row of on/of pixels."""
        crt_row = ""
        for pos in range(len(x_values)):
            sprite_range = range(x_values[pos] - 1, x_values[pos] + 2)
            crt_row += "#" if pos in sprite_range else "."
        return crt_row

    @property
    def characters(self) -> str:
        """Provide the 8-character string formed by the pixels of this CRTScreen."""
        return self._parser.process(pixel_lines=self.pixels)
