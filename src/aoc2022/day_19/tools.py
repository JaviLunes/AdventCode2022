# coding=utf-8
"""Tools used for solving the Day 19: Not Enough Minerals puzzle."""

# Standard library imports:
import math
import re

# Set constants:
INF = 99999
RESOURCES = ("ore", "clay", "obsidian", "geode")


class Pool:
    """4-slot counter for amounts related to ore, clay, obsidian and geode resources."""
    __slots__ = ["ore", "clay", "obsidian", "geode"]

    def __init__(self, ore: int = 0, clay: int = 0, obsidian: int = 0, geode: int = 0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __repr__(self) -> str:
        return f"({self.ore},{self.clay},{self.obsidian},{self.geode})"

    def __eq__(self, other: "Pool") -> bool:
        return self.ore == other.ore and self.clay == other.clay and \
            self.obsidian == other.obsidian and self.geode == other.geode

    def __add__(self, other: "Pool") -> "Pool":
        return Pool(
            ore=self.ore + other.ore, clay=self.clay + other.clay,
            obsidian=self.obsidian + other.obsidian, geode=self.geode + other.geode)

    def __sub__(self, other: "Pool") -> "Pool":
        return Pool(
            ore=self.ore - other.ore, clay=self.clay - other.clay,
            obsidian=self.obsidian - other.obsidian, geode=self.geode - other.geode)

    def __mul__(self, other: int) -> "Pool":
        return Pool(
            ore=self.ore * other, clay=self.clay * other,
            obsidian=self.obsidian * other, geode=self.geode * other)

    def __getitem__(self, resource: str) -> int:
        if resource == "ore":
            return self.ore
        if resource == "clay":
            return self.clay
        if resource == "obsidian":
            return self.obsidian
        if resource == "geode":
            return self.geode
        raise ValueError(f"Unknown '{resource}' resource.")

    @property
    def amounts(self) -> list[int]:
        """List the stored amount of each resource, in a fixed order."""
        return [self.ore, self.clay, self.obsidian, self.geode]

    def copy(self) -> "Pool":
        """Create a new Pool with a DEEP copy of the current Pool's internal state."""
        return Pool(ore=self.ore, clay=self.clay, obsidian=self.obsidian,
                    geode=self.geode)


class Stock:
    """3-slot counter of a Blueprint's resources, robots and remaining operation time."""
    __slots__ = ["resources", "robots", "time"]

    def __init__(self, resources: Pool, robots: Pool, time: int):
        self.resources = resources
        self.robots = robots
        self.time = time

    def __repr__(self) -> str:
        resources = f"Resources {self.resources}"
        robots = f"Robots {self.robots}"
        time = f"{self.time} min"
        return f"{resources} | {robots} | {time}"

    def copy(self) -> "Stock":
        """Create a new Stock with a DEEP copy of the current Stock's internal state."""
        return Stock(resources=self.resources.copy(), robots=self.robots.copy(),
                     time=self.time)


class Blueprint:
    """Recipe stating the amount of resources for building different robot types."""
    __slots__ = ["id", "costs", "max_costs", "geode_output"]

    def __init__(self, id_: int, costs: dict[str, Pool], operation_time: int):
        self.id = id_
        self.costs = costs
        self._precompute_max_costs()
        self._find_max_geode_production(operation_time=operation_time)

    def __repr__(self) -> str:
        costs = " | ".join(map(str, self.costs.values()))
        return f"#{self.id}. Costs: {costs}"

    def _precompute_max_costs(self):
        """Map each resource (except geodes) to its max amount to build any robot."""
        self.max_costs = {resource: max(self.costs[robot][resource]
                                        for robot in RESOURCES if robot != resource)
                          for resource in RESOURCES[:-1]}

    def _find_max_geode_production(self, operation_time: int):
        """Max amount of geodes the robots of this Factory can crack in n minutes."""
        start_stock = Stock(resources=Pool(), robots=Pool(ore=1), time=operation_time)
        pending_stocks = [start_stock]
        completed_stocks = []
        while pending_stocks:
            q_stock = pending_stocks.pop()
            for target_robot, used_rounds in self._get_viable_targets(stock=q_stock):
                s_stock = q_stock.copy()
                self._gather_resources(stock=s_stock, rounds=used_rounds)
                self._build_robot(stock=s_stock, robot_type=target_robot)
                s_stock.time -= used_rounds
                if s_stock.time < 1:
                    completed_stocks.append(s_stock)
                else:
                    pending_stocks.append(s_stock)
        self.geode_output = max(stock.resources.geode for stock in completed_stocks)

    def _get_viable_targets(self, stock: Stock) -> list[tuple[str | None, int]]:
        """Pick next robot to build (or None), with required gather + building rounds."""
        good_options = []
        # General rules:
        only_gathering_remains_option = None, stock.time
        if stock.time <= 1:
            return [only_gathering_remains_option]
        # Rules for non-geode resources:
        for option in RESOURCES[:-1]:
            required_rounds = self._get_rounds_for_building(stock=stock, robot=option)
            max_cost = self.max_costs[option]
            current_robots = stock.robots[option]
            current_resources = stock.resources[option]
            if required_rounds >= stock.time:
                continue  # Not enough rounds to build and use this robot type.
            if current_robots >= max_cost:
                continue  # Enough robots to build the most expensive robot type.
            if current_robots * stock.time + current_resources >= max_cost * stock.time:
                continue  # Enough robots to build most expensive one for remaining time.
            good_options.append((option, required_rounds))
        # Geode rules:
        geode_rounds = self._get_rounds_for_building(stock=stock, robot="geode")
        if geode_rounds < stock.time:
            good_options.append(("geode", geode_rounds))
        # If no good options are found, just keep gathering for the remaining time:
        if len(good_options) == 0:
            return [only_gathering_remains_option]
        return good_options

    def _get_rounds_for_building(self, stock: Stock, robot: str) -> int:
        """Rounds for stocking the target robot cost, plus one round for building it."""
        investment = self.costs[robot]
        remaining = investment - stock.resources
        rounds_per_resource = (
            0 if required < 1 else (INF if prod < 1 else math.ceil(required / prod))
            for required, prod in zip(remaining.amounts, stock.robots.amounts))
        return max(rounds_per_resource) + 1

    @staticmethod
    def _gather_resources(stock: Stock, rounds: int):
        """Make all available robots collect resources for an amount of rounds."""
        stock.resources += stock.robots * rounds

    def _build_robot(self, stock: Stock, robot_type: str | None):
        """Build the target robot and account for investment, if enough resources."""
        if robot_type is None:
            return
        stock.robots += Pool(**{robot_type: 1})
        stock.resources -= self.costs[robot_type]

    @property
    def quality_level(self) -> int:
        """Maximum amount of crackable geodes multiplied by this Factory's id."""
        return self.id * self.geode_output

    @classmethod
    def from_string(cls, string: str, operation_time: int) -> "Blueprint":
        """Create a new Blueprint from a single-line string describing it."""
        id_ = cls._parse_id(string=string)
        costs = cls._parse_robot_costs(string=string)
        return Blueprint(id_=id_, costs=costs, operation_time=operation_time)

    @staticmethod
    def _parse_id(string: str) -> int:
        """Extract the Blueprint id number from its string description."""
        rx = r"^Blueprint (?P<id>\d+): "
        return int(re.match(pattern=rx, string=string)["id"])

    @classmethod
    def _parse_robot_costs(cls, string: str) -> dict[str, Pool]:
        """Map the cost of each resource-gatherer robot type to its target resource."""
        return {r: cls._parse_cost(resource=r, string=string) for r in RESOURCES}

    @staticmethod
    def _parse_cost(resource: str, string: str) -> Pool:
        """Parse the building cost of a robot able to gather the target resource."""
        rx_costs = rf"Each {resource.lower()} robot costs (?P<cost>[\w ]+)."
        rx_resource = r"(?P<cost>\d+) (?P<resource>[a-z]+)"
        cost = re.search(pattern=rx_costs, string=string)["cost"]
        cost = {r: int(c) for c, r in re.findall(pattern=rx_resource, string=cost)}
        return Pool(**cost)


class Factory:
    """Packed device able to create robots for collecting each of the known resources."""
    def __init__(self, blueprints: list[Blueprint]):
        self.blueprints = blueprints

    @property
    def geode_product(self) -> int:
        """Product of the maximum number of geodes for all the simulated blueprints."""
        return math.prod(blueprint.geode_output for blueprint in self.blueprints)

    @property
    def total_quality_level(self) -> int:
        """Sum of quality levels for all the simulated blueprints."""
        return sum(blueprint.quality_level for blueprint in self.blueprints)

    @classmethod
    def from_strings(cls, strings: list[str], operation_time: int):
        """Create a new Factory from a list of blueprint-describing strings."""
        return cls(blueprints=[
            Blueprint.from_string(string=string, operation_time=operation_time)
            for string in strings])
