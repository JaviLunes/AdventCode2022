# coding=utf-8
"""Tools used for solving the Day 21: Monkey Math puzzle."""

# Standard library imports:
import abc
import re


class Monkey(metaclass=abc.ABCMeta):
    """Ex-stuff-slinging simian, now charged with yelling pieces of math riddles."""
    __slots__ = ["name"]

    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def calc_value(self, gang_map: dict[str, int]) -> int:
        """Solve the math operation assigned to this Monkey."""
        raise NotImplementedError

    @classmethod
    def from_str(cls, string: str):
        """Create a new Monkey from its description string."""
        try:
            return ValueMonkey.from_str(string=string)
        except AttributeError:
            return OperationMonkey.from_str(string=string)


class ValueMonkey(Monkey):
    """Monkey charged with yelling a specific integer value."""
    __slots__ = ["_value"]

    def __init__(self, name: str, value: int):
        super().__init__(name=name)
        self._value = value

    def __repr__(self) -> str:
        return f"{self.name}: {self._value}"

    def calc_value(self, gang_map: dict[str, int]) -> int:
        """Solve the math operation assigned to this Monkey."""
        return self._value

    @classmethod
    def from_str(cls, string: str):
        """Create a new ValueMonkey from its description string."""
        rx = r"^(?P<name>\w{4}): (?P<value>\d+)$"
        match_dict = re.match(pattern=rx, string=string).groupdict()
        return cls(name=match_dict["name"], value=int(match_dict["value"]))


class OperationMonkey(Monkey):
    """Monkey charged with yelling the result of a binary math operation."""
    __slots__ = ["ref_1", "ref_2", "_operator"]

    def __init__(self, name: str, ref_1: str, ref_2: str, operator: str):
        super().__init__(name=name)
        self.ref_1 = ref_1
        self.ref_2 = ref_2
        self._operator = operator

    def __repr__(self) -> str:
        return f"{self.name}: {self.ref_1}{self._operator}{self.ref_2}"

    def calc_value(self, gang_map: dict[str, int]) -> int:
        """Yell the result of the math operation assigned to this Monkey."""
        operator_map = {"+": lambda x, y: x + y, "-": lambda x, y: x - y,
                        "*": lambda x, y: x * y, "/": lambda x, y: x / y}
        operator_func = operator_map[self._operator]
        return operator_func(int(gang_map[self.ref_1]), int(gang_map[self.ref_2]))

    @classmethod
    def from_str(cls, string: str):
        """Create a new OperationMonkey from its description string."""
        rx = r"^(?P<name>\w{4}): (?P<r1>\w{4}) (?P<op>\S) (?P<r2>\w{4})$"
        match = re.match(pattern=rx, string=string)
        name, ref_1, operator, ref_2 = match.groups()
        return cls(name=name, ref_1=ref_1, ref_2=ref_2, operator=operator)


class MonkeyGang:
    """Group of monkeys who may guide you to the star fruit grove."""
    def __init__(self, monkeys: list[Monkey], target_monkey_name: str):
        self._target = target_monkey_name
        self._monkey_values = self._compute_monkey_values(monkeys=monkeys)

    def _compute_monkey_values(self, monkeys: list[Monkey]) -> dict[str, int]:
        """Register the target Monkey's value and all its dependencies."""
        monkey_values = {}
        monkey_list = self._find_relevant_monkeys(monkeys=monkeys)
        for monkey in monkey_list[::-1]:
            value = monkey.calc_value(gang_map=monkey_values)
            monkey_values.update({monkey.name: value})
        return monkey_values

    def _find_relevant_monkeys(self, monkeys: list[Monkey]) -> list[Monkey]:
        """List all recursive monkey dependencies of the target Monkey."""
        monkey_map = {monkey.name: monkey for monkey in monkeys}
        pending_monkeys = [monkey_map[self._target]]
        relevant_monkeys = []
        while pending_monkeys:
            monkey = pending_monkeys.pop(0)
            relevant_monkeys.append(monkey)
            if isinstance(monkey, OperationMonkey):
                pending_monkeys.append(monkey_map[monkey.ref_1])
                pending_monkeys.append(monkey_map[monkey.ref_2])
        return relevant_monkeys

    def __getitem__(self, monkey_name: str) -> int:
        return self._monkey_values[monkey_name]

    @classmethod
    def from_strings(cls, strings: list[str], target_monkey_name: str) -> "MonkeyGang":
        """Create a new MonkeyGang from a list of monkey-describing strings."""
        monkeys = [Monkey.from_str(string=string) for string in strings]
        return cls(monkeys=monkeys, target_monkey_name=target_monkey_name)
