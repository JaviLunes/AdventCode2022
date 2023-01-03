# coding=utf-8
"""Tools used for solving the Day 21: Monkey Math puzzle."""

# Standard library imports:
from collections import deque
from collections.abc import Callable
from operator import add, sub, mul, truediv

# Set constants:
OPERATOR_MAP = {"+": add, "-": sub, "*": mul, "/": truediv}


class Monkey:
    """Ex-stuff-slinging simian, now charged with yelling pieces of math riddles."""
    __slots__ = ["name", "map", "_expression", "value"]

    def __init__(self, name: str, expression: str, monkey_map: dict[str, int]):
        self.name = name
        self.map = monkey_map
        self._expression = self._parse_expression(expression=expression)
        self.value = None if isinstance(self._expression, tuple) else self._expression

    @staticmethod
    def _parse_expression(expression: str) -> int | tuple[str, str, Callable]:
        """Decompose the string describing the job of this Monkey."""
        if expression.isdecimal():
            return int(expression)
        dep_1, op, dep_2 = expression.split(" ")
        return dep_1, dep_2, OPERATOR_MAP[op]

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.name}: {self.value}"
        return f"{self.name}: ({', '.join(self._expression[:2])})"

    @property
    def dependencies(self) -> tuple[str, str] | None:
        """All monkeys' names whose values must be known for doing this Monkey's job."""
        if isinstance(self._expression, int):
            return None
        return self._expression[:2]

    def solve(self):
        """Register the result of the math operation assigned to this Monkey."""
        if self.value is None:
            dep_1, dep_2, operator = self._expression
            self.value = int(operator(self.map[dep_1], self.map[dep_2]))

    @classmethod
    def from_str(cls, string: str, monkey_map: dict[str, int]):
        """Create a new Monkey from its description string."""
        name, expression = string.split(": ")
        return cls(name=name, expression=expression, monkey_map=monkey_map)


class MonkeyGang:
    """Group of monkeys who may guide you to the star fruit grove."""
    def __init__(self, monkeys: list[Monkey], monkey_map: dict[str, int]):
        self.monkey_map = monkey_map
        constant_monkeys, variable_monkeys = self._split_by_dependency(monkeys=monkeys)
        self._solve_constant_monkeys(monkeys=constant_monkeys)
        self._solve_variable_monkeys(monkeys=variable_monkeys)

    def _solve_constant_monkeys(self, monkeys: list[Monkey]):
        """Register all non-dependency monkeys in the monkey map in an optimized way."""
        self.monkey_map.update({m.name: m.value for m in monkeys})

    def _solve_variable_monkeys(self, monkeys: list[Monkey]):
        """Try to solve and register each monkey with dependencies iteratively."""
        monkeys = deque(monkeys)
        while monkeys:
            monkey = monkeys.popleft()
            try:
                monkey.solve()
            except KeyError:
                monkeys.append(monkey)
            else:
                self.monkey_map.update({monkey.name: monkey.value})

    @staticmethod
    def _split_by_dependency(monkeys: list[Monkey]) -> tuple[list[Monkey], list[Monkey]]:
        """Divide the list of monkeys according to their dependencies."""
        constants, variables = [], []
        for monkey in monkeys:
            if monkey.dependencies is None:
                constants.append(monkey)
            else:
                variables.append(monkey)
        return constants, variables

    def __getitem__(self, monkey_name: str) -> int:
        return self.monkey_map[monkey_name]

    @classmethod
    def from_strings(cls, strings: list[str]) -> "MonkeyGang":
        """Create a new MonkeyGang from a list of monkey-describing strings."""
        monkey_map = {}
        monkeys = [Monkey.from_str(string=s, monkey_map=monkey_map) for s in strings]
        return cls(monkeys=monkeys, monkey_map=monkey_map)
