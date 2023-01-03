# coding=utf-8
"""Tools used for solving the Day 21: Monkey Math puzzle."""

# Standard library imports:
from collections import deque
from collections.abc import Callable
from operator import add, sub, mul, truediv

# Set constants:
OPERATOR_MAP = {"+": add, "-": sub, "*": mul, "/": truediv}
MonkeyMap = dict[str, int]


class Monkey:
    """Ex-stuff-slinging simian, now charged with yelling pieces of math riddles."""
    __slots__ = ["name", "_expression", "_value"]

    def __init__(self, name: str, expression: str):
        self.name = name
        self._expression = self._parse_expression(expression=expression)
        self._value = None if isinstance(self._expression, tuple) else self._expression

    @staticmethod
    def _parse_expression(expression: str) -> int | tuple[str, str, Callable]:
        """Decompose the string describing the job of this Monkey."""
        if expression.isdecimal():
            return int(expression)
        dep_1, op, dep_2 = expression.split(" ")
        return dep_1, dep_2, OPERATOR_MAP[op]

    def __repr__(self) -> str:
        if self._value is not None:
            return f"{self.name}: {self._value}"
        return f"{self.name}: ({', '.join(self._expression[:2])})"

    @property
    def direct_dependencies(self) -> tuple[str, str] | None:
        """Closest monkeys whose values must be known for solving this Monkey's job."""
        if isinstance(self._expression, int):
            return None
        return self._expression[:2]

    def solve(self, value_map: MonkeyMap) -> int:
        """Compute the result of the math operation assigned to this Monkey."""
        if self._value is None:
            dep_1, dep_2, operator = self._expression
            return operator(value_map[dep_1], value_map[dep_2])
        return self._value

    @classmethod
    def from_str(cls, string: str):
        """Create a new Monkey from its description string."""
        name, expression = string.split(": ")
        return cls(name=name, expression=expression)


class MonkeyGang:
    """Group of monkeys who may guide you to the star fruit grove."""
    def __init__(self, monkeys: list[Monkey]):
        self.monkeys_map = {monkey.name: monkey for monkey in monkeys}
        self.value_map = {}
        self._solve_monkeys()

    def _solve_monkeys(self):
        """Solve all stored monkeys and register their values in the value map."""
        constant_monkeys, variable_monkeys = self._split_by_dependency()
        self._solve_constant_monkeys(monkeys=constant_monkeys)
        self._solve_variable_monkeys(monkeys=variable_monkeys)

    def _split_by_dependency(self) -> tuple[list[Monkey], list[Monkey]]:
        """Separate the stored monkeys without dependencies from those with them."""
        constants, variables = [], []
        for monkey in self.monkeys_map.values():
            if monkey.direct_dependencies is None:
                constants.append(monkey)
            else:
                variables.append(monkey)
        return constants, variables

    def _solve_constant_monkeys(self, monkeys: list[Monkey]):
        """Register all non-dependency monkeys in the monkey map in an optimized way."""
        constant_map = {m.name: m.solve(value_map=self.value_map) for m in monkeys}
        self.value_map.update(constant_map)

    def _solve_variable_monkeys(self, monkeys: list[Monkey]):
        """Try to solve and register each monkey with dependencies iteratively."""
        monkeys = deque(monkeys)
        while monkeys:
            monkey = monkeys.popleft()
            try:
                monkey.solve(value_map=self.value_map)
            except KeyError:
                monkeys.append(monkey)
            else:
                value = monkey.solve(value_map=self.value_map)
                self.value_map.update({monkey.name: value})

    def __getitem__(self, monkey_name: str) -> int:
        return self.value_map[monkey_name]

    @classmethod
    def from_strings(cls, strings: list[str]) -> "MonkeyGang":
        """Create a new MonkeyGang from a list of monkey-describing strings."""
        monkeys = [Monkey.from_str(string=s) for s in strings]
        return cls(monkeys=monkeys)


class FixedMonkeyGang(MonkeyGang):
    """Group of monkeys with jobs fixed according to a new translation."""
    def _solve_monkeys(self):
        """Solve all stored monkeys and register their values in the value map."""
        self._replace_root()
        constant_monkeys, variable_monkeys = self._split_by_dependency()
        self._solve_constant_monkeys(monkeys=constant_monkeys)
        base_map = {**self.value_map}
        binary_search(
            func=self._test_humn, target_value=0, high=int(1e20), low=0,
            monkeys=variable_monkeys, base_map=base_map)

    def _replace_root(self):
        """Change the root Monkey job according to the fixed translation."""
        root = self.monkeys_map["root"]
        d1, d2 = root.direct_dependencies[:2]
        root_dependency_trees = self._get_dependency_trees(monkey=root)
        humn_on_left = "humn" in root_dependency_trees[0]
        new_expression = f"{d2} - {d1}" if humn_on_left else f"{d1} - {d2}"
        new_root = Monkey(name="root", expression=new_expression)
        self.monkeys_map["root"] = new_root

    def _get_dependency_trees(self, monkey: Monkey) -> tuple[list[str], list[str]]:
        """List all recursive monkey dependencies at left and right of a Monkey."""
        left_tree, right_tree = [], []
        left = self.monkeys_map[monkey.direct_dependencies[0]]
        right = self.monkeys_map[monkey.direct_dependencies[1]]
        left_tree.append(left.name)
        if left.direct_dependencies is not None:
            child_tree_left, child_tree_right = self._get_dependency_trees(monkey=left)
            left_tree.extend(child_tree_left + child_tree_right)
        right_tree.append(right.name)
        if right.direct_dependencies is not None:
            child_tree_left, child_tree_right = self._get_dependency_trees(monkey=right)
            right_tree.extend(child_tree_left + child_tree_right)
        return left_tree, right_tree

    def _test_humn(self, value: int, monkeys: list[Monkey], base_map: MonkeyMap) -> int:
        """Solve all variable monkeys for a given value of the humn monkey."""
        self.value_map = {**base_map, "humn": value}
        self._solve_variable_monkeys(monkeys=monkeys)
        return self.value_map["root"]


def binary_search(func: Callable, target_value: int, high: int, low: int = 0,
                  **other_func_kwargs) -> int:
    """Find the argument of a given function that makes it return the target value."""
    while low <= high:
        candidate = (high + low) // 2
        output = func(candidate, **other_func_kwargs)
        if output == target_value:
            return candidate
        elif output < target_value:
            low = candidate + 1
        else:
            high = candidate - 1
    raise ValueError("The target value couldn't be reached.")
