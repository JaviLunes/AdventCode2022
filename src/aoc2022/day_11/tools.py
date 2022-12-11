# coding=utf-8
"""Tools used for solving the Day 11: Monkey in the Middle puzzle."""

# Standard library imports:
from collections.abc import Iterable
import math


class Monkey:
    """Stuff-slinging simian skilled at sensing your worry level."""
    def __init__(self, monkey_id: int, items: list[int], operator: str,
                 operation_value: int | str, test_divisible: int,
                 throw_to_when_true: int, throw_to_when_false: int):
        self.id = monkey_id
        self.items = items
        self._operator = operator
        self._new_value = operation_value
        self.test_value = test_divisible
        self._id_true = throw_to_when_true
        self._id_false = throw_to_when_false
        self.inspected_items = 0

    def __repr__(self) -> str:
        return f"Monkey {self.id}: {self.inspected_items} total inspected items."

    def __hash__(self) -> int:
        return hash(self.id)

    def take_turn(self) -> Iterable[tuple[int, int]]:
        """Make this Monkey inspect and throw all the items it currently hoards."""
        while self.items:
            item = self.items.pop(0)
            self.inspected_items += 1
            inspected_item, test_result = self._inspect_and_test(item=item)
            receiver_id = self._choose_receiver(test_result=test_result)
            yield inspected_item, receiver_id

    def _inspect_and_test(self, item: int) -> tuple[int, bool]:
        """Update the worry level of an item and choose an id to send the item to."""
        new_value = item if self._new_value == "old" else int(self._new_value)
        item = self._apply_operator(item=item, new_value=new_value)
        item = self._reduce_worry_level(item=item)
        test = self._test_item(inspected_item=item)
        return item, test

    @classmethod
    def _reduce_worry_level(cls, item: int) -> int:
        """Thank God the monkey's inspection didn't break the item!"""
        return math.floor(item / 3)

    def _apply_operator(self, item: int, new_value: int) -> int:
        """Apply the stored operator to combine the two provided values."""
        if self._operator == "+":
            return item + new_value
        if self._operator == "*":
            return item * new_value
        else:
            raise ValueError(f"Unrecognized '{self._operator}' operator.")

    def _test_item(self, inspected_item: int) -> bool:
        """Apply the test operation to the worry level of an inspected item."""
        return (inspected_item % self.test_value) == 0

    def _choose_receiver(self, test_result: bool) -> int:
        """Select the id of the Monkey to send this item to based on the test."""
        return self._id_true if test_result else self._id_false

    def receive(self, item: int):
        """Make this Monkey receive a new item."""
        self.items.append(item)

    @classmethod
    def from_notes(cls, notes: list[str]) -> "Monkey":
        """Create a new Monkey from the notes you took on its items and behaviour."""
        monkey_id = int(notes[0].removesuffix(":")[-1])
        items = [int(v) for v in notes[1].removeprefix("  Starting items: ").split(", ")]
        operation = notes[2].removeprefix("  Operation: new = old ").split(" ")
        operator, operation_value = operation
        test = int(notes[3].removeprefix("  Test: divisible by "))
        throw_true = int(notes[4].removeprefix("    If true: throw to monkey "))
        throw_false = int(notes[5].removeprefix("    If false: throw to monkey "))
        return cls(
            monkey_id=monkey_id, items=items, operator=operator,
            test_divisible=test, operation_value=operation_value,
            throw_to_when_true=throw_true, throw_to_when_false=throw_false)


class InfuriatingMonkey(Monkey):
    """Monkey that forces you to find another way to cope with your stress."""
    _worry_reducer = 1

    @classmethod
    def _reduce_worry_level(cls, item: int) -> int:
        """This is getting nowhere!"""
        # Note 0: The key here is to realize that you don't care about the actual worry
        #   level values of your items. You only care about accurately tracking the
        #   number of items each Monkey inspects (which is equal to accurately track
        #   how many items a Monkey receive from other Monkeys at each round).
        # Note 1: When aiming to track which items will a Monkey toss to other Monkeys
        #   (and hence, how many items the other Monkeys will receive), you only need
        #   to worry about the 'divisible by X' test done by the tossing Monkey.
        # Note 2: If you do nothing to reduce the worry level after each item is
        #   inspected by one Monkey, the values of the items keep increasing until
        #   errors due to operating with huge numbers start to happen.
        # Note 3: If, before checking if an item is divisible by 'X' (the Monkey's test),
        #   you apply 'item % Y', where 'Y' is ANY multiple of the 'X' test value, then
        #   the result of the test will not be altered, and your item's value will be
        #   more manageable for future Monkeys.
        # Note 4: So, if you choose 'Y' to be the least common multiple of the 'X'
        #   values of all Monkeys, then the tests of all Monkeys will remain unaffected,
        #   but the worry levels of your items will be kept small for all the rounds
        #   played by these simians.
        return item % cls._worry_reducer


class MonkeyGang:
    """Group of monkeys having a good time playing Keep Away with your items."""
    def __init__(self, monkeys: list[Monkey]):
        self._monkeys = {monkey.id: monkey for monkey in monkeys}

    def do_rounds(self, rounds: int):
        """Make the MonkeyGang play with your stuff for a given amount of rounds."""
        for _ in range(rounds):
            self._do_one_round()

    def _do_one_round(self):
        """Make each Monkey member take one turn inspecting and tossing held items."""
        for monkey in self.monkeys:
            for item, receiver_id in monkey.take_turn():
                self._monkeys[receiver_id].receive(item=item)

    @property
    def monkeys(self) -> list[Monkey]:
        """Provide all Monkey members in the gang."""
        return list(self._monkeys.values())

    @property
    def monkeys_per_activity_level(self) -> list[Monkey]:
        """Return a list of Monkey members, sorted by decreasing # of inspected items."""
        return sorted(self.monkeys, key=lambda m: m.inspected_items, reverse=True)

    @property
    def monkey_business(self) -> int:
        """Multiply the # of items inspected by the two more busy Monkey members."""
        monkeys = self.monkeys_per_activity_level
        return monkeys[0].inspected_items * monkeys[1].inspected_items

    @classmethod
    def from_notes(cls, notes: list[str], infuriating: bool) -> "MonkeyGang":
        """Create a new MonkeyGang from the notes you took on each Monkey in the gang."""
        notes = "|".join(notes).split("||")
        monkey_cls = InfuriatingMonkey if infuriating else Monkey
        monkeys = [monkey_cls.from_notes(notes=m_notes.split("|")) for m_notes in notes]
        if infuriating:
            test_value_lcm = cls._get_worry_reducer(monkeys=monkeys)
            InfuriatingMonkey._worry_reducer = test_value_lcm
        return MonkeyGang(monkeys=monkeys)

    @staticmethod
    def _get_worry_reducer(monkeys: list[Monkey]) -> int:
        """Compute the least common multiple of the test values for a Monkey group."""
        return math.lcm(*[monkey.test_value for monkey in monkeys])
