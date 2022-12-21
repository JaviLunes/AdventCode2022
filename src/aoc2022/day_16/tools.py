# coding=utf-8
"""Tools used for solving the Day 16: Proboscidea Volcanium puzzle."""

# Standard library imports:
import itertools
import re
from typing import Iterable

# Third party imports:
from aoc_tools.algorithms.a_star_search import Node, a_star_search


class Room(Node):
    """Location within the volcano's tunnel network with a single Valve."""
    __slots__ = ["_name", "_neighbours_map"]

    def __init__(self, name: str, neighbours_map: dict[str, list[str]],
                 parent: "Room" = None):
        super().__init__(parent=parent)
        self._name = name
        self._neighbours_map = neighbours_map

    @property
    def id(self) -> str:
        """Provide a string identifier unique to this Room."""
        return self._name

    @property
    def g(self) -> int:
        """Compute the cost for reaching this Room from the search start point."""
        return 0 if self._parent is None else self.parent.g + 1

    @property
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from this Room."""
        return 0

    def get_successors(self) -> Iterable["Room"]:
        """List all nodes to search that are directly reachable from this Room."""
        adjacent_rooms = self._neighbours_map[self._name]
        for s_name in adjacent_rooms:
            yield Room(
                name=s_name, parent=self, neighbours_map=self._neighbours_map)


class TunnelNetwork:
    """Interconnected locations inside a volcano, each hosting a single valve."""
    __slots__ = ["_neighbours_map", "_flow_rates_map", "_travel_map"]

    def __init__(self, neighbours_map: dict[str, list[str]],
                 flow_rates_map: dict[str, int]):
        self._neighbours_map = neighbours_map
        self._flow_rates_map = flow_rates_map
        self._travel_map = self._build_travel_map(locations=list(neighbours_map.keys()))

    def _build_travel_map(self, locations: list[str]) -> dict[str, dict[str, int]]:
        """Register the lowest travel time between all pairs of locations."""
        times_map = {from_: {to_: None for to_ in locations} for from_ in locations}
        for from_ in locations:
            for to_ in locations:
                if from_ == to_:
                    # No travel required:
                    times_map[from_][to_] = 0
                elif times_map[from_][to_] is None and times_map[to_][from_] is None:
                    # Compute the travel time for an unseen pair:
                    travel_time = self._find_shortest_travel(from_=from_, to_=to_)
                    times_map[from_][to_] = travel_time
                    times_map[to_][from_] = travel_time
                else:
                    # Update the travel time for an already seen pair:
                    travel_time = times_map[from_][to_] or times_map[to_][from_]
                    times_map[from_][to_] = travel_time
                    times_map[to_][from_] = travel_time
        return times_map

    def _find_shortest_travel(self, from_: str, to_: str) -> int:
        """Find the shortest travel time between locations using A* search."""
        start = Room(name=from_, parent=None, neighbours_map=self._neighbours_map)
        goal_room = a_star_search(start=start, goal_func=lambda node: node.id == to_)
        return goal_room.g

    @property
    def relevant_locations(self) -> list[str]:
        """List all locations known by this TunnelNetwork with non-damaged valves."""
        return list(loc for loc, fr in self._flow_rates_map.items() if fr > 0)

    def get_travel(self, from_: str, to_: str) -> int:
        """Time to reach one location, starting at another location."""
        return self._travel_map[from_][to_]

    def get_flow(self, location: str) -> int:
        """Provide the flow rate of the pressure-release valve at a given location."""
        return self._flow_rates_map[location]

    @classmethod
    def from_scan_report(cls, scan_report: list[str]) -> "TunnelNetwork":
        """Create a new TunnelNetwork from a scan report of valves and tunnels."""
        rx = r"^.+(?P<name>[A-Z]{2}) .+=(?P<fr>\d+); .+valves? (?P<neighbours>.+)$"
        neighbours_map = {}
        flow_rates_map = {}
        for scan_line in scan_report:
            name, flow_rate, neighbours = re.match(pattern=rx, string=scan_line).groups()
            neighbours_map.update({name: neighbours.split(", ")})
            flow_rates_map.update({name: int(flow_rate)})
        return cls(neighbours_map=neighbours_map, flow_rates_map=flow_rates_map)


class Valve(Node):
    """Mechanical device able to release pressure from the volcano's pipe network."""
    __slots__ = ["_name", "_open_time", "_network", "output"]

    def __init__(self, name: str, open_time: int, network: TunnelNetwork,
                 parent: "Valve" = None):
        super().__init__(parent=parent)
        self._name = name
        self._open_time = max(0, open_time)
        self._network = network
        self.output = self._open_time * network.get_flow(location=name)

    @property
    def id(self) -> str:
        """Provide a string identifier unique to this Valve."""
        return self._name

    @property
    def g(self) -> int:
        """Compute the cost for reaching this Valve from the search start point."""
        return (0 if self._parent is None else self.parent.g) - self.output

    @property
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from this Valve."""
        total = 0
        for location in self._remaining_locations():
            travel_time = self._network.get_travel(from_=self._name, to_=location)
            open_time = max(0, self._open_time - travel_time - 1)
            flow_rate = self._network.get_flow(location=location)
            total -= open_time * flow_rate
        return total

    def get_successors(self) -> Iterable["Node"]:
        """List all nodes to search that are directly reachable from this Valve."""
        for s_name in self._remaining_locations():
            travel_time = self._network.get_travel(from_=self._name, to_=s_name)
            s_valve = Valve(
                name=s_name, open_time=self._open_time - travel_time - 1,
                parent=self, network=self._network)
            if s_valve.output > 0:
                yield s_valve

    def _remaining_locations(self) -> list[str]:
        """List all locations not included in this Valve's lineage."""
        all_locations = self._network.relevant_locations
        lineage_locations = [step.id for step in self.lineage]
        return [n for n in all_locations if n not in lineage_locations]


class DoubleValve(Node):
    """Pair of Valve devices operated by you and one of the elephants."""
    __slots__ = ["_name_1", "_name_2", "_open_time_1", "_open_time_2",
                 "_network", "output"]

    def __init__(self, name_1: str, name_2: str, open_time_1: int, open_time_2: int,
                 network: TunnelNetwork, parent: "DoubleValve" = None):
        super().__init__(parent=parent)
        self._name_1 = name_1
        self._name_2 = name_2
        self._open_time_1 = max(0, open_time_1)
        self._open_time_2 = max(0, open_time_2)
        self._network = network
        output_1 = self._open_time_1 * network.get_flow(location=name_1)
        output_2 = self._open_time_2 * network.get_flow(location=name_2)
        self.output = output_1 + output_2

    @property
    def id(self) -> str:
        """Provide a string identifier unique to this DoubleValve."""
        return "-".join([self._name_1, self._name_2])

    @property
    def g(self) -> int:
        """Compute the cost for reaching this DoubleValve from the search start point."""
        return (0 if self._parent is None else self._parent.g) - self.output

    @property
    def h(self) -> int:
        """Estimate the cost for reaching the search goal from this DoubleValve."""
        total = 0
        for location in self._remaining_locations():
            travel_time_1 = self._network.get_travel(from_=self._name_1, to_=location)
            travel_time_2 = self._network.get_travel(from_=self._name_2, to_=location)
            open_time_1 = max(0, self._open_time_1 - travel_time_1 - 1)
            open_time_2 = max(0, self._open_time_2 - travel_time_2 - 1)
            flow_rate = self._network.get_flow(location=location)
            open_time = max(open_time_1, open_time_2)
            total -= open_time * flow_rate
        return total

    def get_successors(self) -> Iterable["Node"]:
        """List all nodes to search that are directly reachable from this DoubleValve."""
        remaining_loc = self._remaining_locations()
        for s_name_1, s_name_2 in itertools.product(remaining_loc, remaining_loc):
            if s_name_1 == s_name_2:
                continue
            travel_time_1 = self._network.get_travel(from_=self._name_1, to_=s_name_1)
            travel_time_2 = self._network.get_travel(from_=self._name_2, to_=s_name_2)
            s_double_valve = DoubleValve(
                name_1=s_name_1, open_time_1=self._open_time_1 - travel_time_1 - 1,
                name_2=s_name_2, open_time_2=self._open_time_2 - travel_time_2 - 1,
                parent=self, network=self._network)
            if s_double_valve.output > 0:
                yield s_double_valve

    def _remaining_locations(self) -> list[str]:
        """List all locations not included in this DoubleValve's lineage."""
        all_locations = self._network.relevant_locations
        ids = [step.id for step in self.lineage]
        lineage_locations = list(itertools.chain(*[id_.split("-") for id_ in ids]))
        return [n for n in all_locations if n not in lineage_locations]


class ValveSim:
    """App able to find the best valve-opening strategy for maximum pressure release."""
    def __init__(self, network: TunnelNetwork, total_time: int):
        self._network = network
        self._total_time = total_time

    def find_max_release(self) -> int:
        """Compute the total pressure released by applying an optimized opening plan."""
        start = Valve(
            name="AA", open_time=self._total_time, parent=None, network=self._network)
        goal_valve = a_star_search(
            start=start, goal_func=lambda node: len(list(node.get_successors())) == 0)
        return -goal_valve.g

    def find_max_release_with_help(self) -> int:
        """Compute the total pressure released if you have help from one elephant."""
        start = DoubleValve(
            name_1="AA", open_time_1=self._total_time, parent=None,
            name_2="AA", open_time_2=self._total_time, network=self._network)
        goal_valve = a_star_search(
            start=start, goal_func=lambda node: len(list(node.get_successors())) == 0)
        return -goal_valve.g

    @classmethod
    def from_scan_report(cls, scan_report: list[str], total_time: int) -> "ValveSim":
        """Create a new ValveSim from a scan report of valves and tunnels."""
        network = TunnelNetwork.from_scan_report(scan_report=scan_report)
        rx = r"^.+(?P<name>[A-Z]{2}) .+=(?P<fr>\d+); .+valves? .+$"
        flows_map = {}
        for scan_line in scan_report:
            name, flow_rate = re.match(pattern=rx, string=scan_line).groups()
            flows_map.update({name: int(flow_rate)})
        return cls(network=network, total_time=total_time)
