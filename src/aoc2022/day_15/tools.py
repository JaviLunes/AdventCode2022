# coding=utf-8
"""Tools used for solving the Day 15: Beacon Exclusion Zone puzzle."""

# Standard library imports:
from collections.abc import Iterable
from operator import itemgetter


class Point:
    """2D location in a discrete-grid-like network of subterranean tunnels."""
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

    def __eq__(self, other: "Point") -> bool:
        return self.xy == other.xy

    def __hash__(self) -> int:
        return hash(self.xy)

    def distance(self, other: "Point") -> int:
        """Compute the Manhattan distance between this and another Point."""
        return abs(other.x - self.x) + abs(other.y - self.y)

    @property
    def xy(self) -> tuple[int, int]:
        """Provide the XY coordinates of this Point as a tuple."""
        return self.x, self.y


class Beacon(Point):
    """Static device located at a given point, radiating a signal."""
    @property
    def tuning_freq(self) -> int:
        """Provide the tuning frequency value of this Beacon."""
        return self.x * 4000000 + self.y


class Sensor(Point):
    """Device linked to the nearest Beacon, defining an area without more beacons."""
    __slots__ = ["beacon"]

    def __init__(self, x: int, y: int, beacon_x: int, beacon_y: int):
        super().__init__(x=x, y=y)
        self.beacon = Beacon(x=beacon_x, y=beacon_y)

    @property
    def exclusion_radius(self) -> int:
        """Manhattan distance from this Sensor where only the linked beacon may be."""
        return self.distance(other=self.beacon)

    @property
    def perimeter_points(self) -> Iterable[Point]:
        """All locations exactly one exclusion radius plus one unit from this Sensor."""
        radius = self.exclusion_radius + 1
        for y in range(self.y - radius, self.y + radius + 1):
            y_dist = abs(y - self.y)
            yield Point(x=self.x + (radius - y_dist), y=y)
            if (radius - y_dist) != 0:
                yield Point(x=self.x - (radius - y_dist), y=y)

    def contains(self, point: Point) -> bool:
        """Check if the provided Point lays inside the exclusion range of this Sensor."""
        return self.distance(other=point) <= self.exclusion_radius

    def get_exclusion_row(self, y: int) -> range:
        """Get all X values along a given Y belonging to this Sensor's exclusion zone."""
        x_max_dist = self.exclusion_radius - abs(y - self.y)
        return range(self.x - x_max_dist, self.x + x_max_dist + 1)

    @classmethod
    def from_string(cls, string: str) -> "Sensor":
        """Create a new Sensor from a string stating its location and closest beacon."""
        string = string.replace("Sensor at ", "").replace(" closest beacon is at ", "")
        string = string.replace(" ", "").replace("x=", "").replace("y=", "")
        x, y, xb, yb = string.replace(":", ",").split(",")
        return cls(x=int(x), y=int(y), beacon_x=int(xb), beacon_y=int(yb))


class Constellation:
    """Group of autonomous Sensor objects originally built to locate lost Elves."""
    def __init__(self, sensors: list[Sensor]):
        self.sensor_map = {sensor.xy: sensor for sensor in sensors}

    @property
    def sensors(self) -> list[Sensor]:
        """Provide all Sensor objects included in this constellation."""
        return list(self.sensor_map.values())

    def count_excluded_points_at_row(self, y: int) -> int:
        """Find all locations along a given Y where an unknown Beacon may NOT be."""
        exclusion_ranges = self._row_ranges(y=y)
        zone_points = sum((len(r) for r in exclusion_ranges))
        known_beacons = len({s.beacon for s in self.sensors if s.beacon.y == y})
        return zone_points - known_beacons

    def _row_ranges(self, y: int) -> list[range]:
        """Get all non-overlapping ranges of excluded locations for a given Y."""
        ranges = list(filter(None, (s.get_exclusion_row(y=y) for s in self.sensors)))
        return list(merge_ranges(ranges=ranges))

    def find_distress_beacon(self, search_area_side: int) -> Beacon:
        """Retrieve the only possible non-detected Beacon within a search area."""
        target_point = self._find_non_excluded_point(search_area_side=search_area_side)
        return Beacon(x=target_point.x, y=target_point.y)

    def _find_non_excluded_point(self, search_area_side: int) -> Point:
        """Hop from perimeter to perimeter until a Point not seen by any Sensor."""
        sensors = [*self.sensors]
        for s, target_sensor in enumerate(sensors):
            other_sensors = sensors[:s] + sensors[s + 1:]
            for point in target_sensor.perimeter_points:
                if not self._is_within_area(point=point, area_side=search_area_side):
                    continue
                if self._is_within_sensor(point=point, sensors=other_sensors):
                    continue
                return point
        raise ValueError("No valid point was found.")

    @staticmethod
    def _is_within_area(point: Point, area_side: int) -> bool:
        """Check if a Point is within a given square-shaped area."""
        return point.x in range(area_side + 1) and point.y in range(area_side + 1)

    @staticmethod
    def _is_within_sensor(point: Point, sensors: list[Sensor]) -> bool:
        """Check if a Point is within any of provided sensors' exclusion zone."""
        return any(sensor.contains(point=point) for sensor in sensors)

    @classmethod
    def from_report(cls, report: list[str]) -> "Constellation":
        """Create a new Constellation from a group of Sensor-describing strings."""
        sensors = [Sensor.from_string(string=s) for s in report]
        return cls(sensors=sensors)


def merge_ranges(ranges: list[range]) -> list[range]:
    """Reduce a list of ranges by combining all overlapping ones."""
    sorted_ranges = sorted(ranges, key=itemgetter(0))
    low, high = sorted_ranges[0].start, sorted_ranges[0].stop
    for new_range in sorted_ranges[1:]:
        if new_range.start <= high:
            high = max(high, new_range.stop)
        else:
            yield range(low, high)
            low, high = new_range.start, new_range.stop
    yield range(low, high)
