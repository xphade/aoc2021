#!/usr/bin/env python3

from typing import Dict, List


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Point):
            return False
        return (self.x, self.y) == (__o.x, __o.y)


class Line:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end

    def _get_range(self, start: int, end: int) -> range:
        step = 1 if start <= end else -1
        return range(start, end + step, step)

    def get_coordinates(self) -> List[Point]:
        assert (
            self.start.x == self.end.x
            or self.start.y == self.end.y
            or abs(self.start.x - self.end.x) == abs(self.start.y - self.end.y)
        )

        range_x = self._get_range(self.start.x, self.end.x)
        range_y = self._get_range(self.start.y, self.end.y)

        if self.start.x == self.end.x:
            return [Point(self.start.x, y) for y in range_y]
        elif self.start.y == self.end.y:
            return [Point(x, self.start.y) for x in range_x]
        else:
            return [Point(x, y) for x, y in zip(range_x, range_y)]


def extract_lines(input: List[str], include_diagonals: bool) -> List[Line]:
    lines: List[Line] = []

    for raw_line in input:
        raw_start, raw_end = raw_line.split(" -> ")
        start = [*map(int, raw_start.split(","))]
        end = [*map(int, raw_end.split(","))]

        # Continue if diagonals should not be included
        if not include_diagonals and (start[0] != end[0] and start[1] != end[1]):
            continue

        lines.append(Line(Point(start[0], start[1]), Point(end[0], end[1])))

    return lines


def generate_vent_map(lines: List[Line]) -> Dict[Point, int]:
    vent_map: Dict[Point, int] = {}

    # Flat list of all coordinates with a vent
    coordinates = [point for line in lines for point in line.get_coordinates()]

    for point in coordinates:
        if point in vent_map:
            vent_map[point] += 1
        else:
            vent_map[point] = 1

    return vent_map


if __name__ == "__main__":
    data_path = "./data/05_lines-of-vents.txt"
    with open(data_path, "r") as file:
        raw_lines = file.readlines()

    for include_diagonals in [False, True]:
        lines = extract_lines(raw_lines, include_diagonals)
        vent_map = generate_vent_map(lines)
        number_of_overlaps = sum([vents >= 2 for vents in vent_map.values()])

        mode = "including diagonals" if include_diagonals else "horizontal/vertical"
        print(f"Number of overlaps ({mode}): {number_of_overlaps}")
