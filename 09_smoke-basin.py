#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from math import prod
from timeit import default_timer as timer
from typing import List, Set, Tuple

Position = Tuple[int, int]
MapSize = Tuple[int, int]


def outside_of_map(coordinate: Position, row_size: int, col_size: int) -> bool:
    """Check if the given `coordinate` is outside of the map"""
    row, col = coordinate
    return (row < 0) or (row >= row_size) or (col < 0) or (col >= col_size)


def adjacent_points(coordinate: Position) -> List[Position]:
    """Return adjacent points of the given `coordinate`"""
    row, col = coordinate
    return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


def is_low_point(heightmap: List[List[int]], point: Position, size: MapSize) -> bool:
    """Test if a given `point` is a local low point"""
    row, col = point[0], point[1]
    height = heightmap[row][col]

    for r, c in adjacent_points((row, col)):
        if outside_of_map((r, c), size[0], size[1]):
            continue

        if heightmap[r][c] <= height:
            return False

    return True


def find_low_points(heightmap: List[List[int]], size: MapSize) -> List[Position]:
    """Find all low points in the `heightmap`"""
    low_points: List[Position] = []
    for row in range(len(heightmap)):
        for col in range(len(heightmap[row])):
            if is_low_point(heightmap, (row, col), size):
                low_points.append((row, col))
    return low_points


def build_basin(
    heightmap: List[List[int]], low_point: Position, size: MapSize
) -> List[Position]:
    """Build the basin corresponding to the given `low_point`"""
    points_to_visit: Set[Position] = {low_point}
    points_visited: Set[Position] = set()

    while len(points_to_visit) > 0:
        row, col = points_to_visit.pop()
        points_visited.add((row, col))

        for r, c in adjacent_points((row, col)):
            if outside_of_map((r, c), size[0], size[1]):
                continue

            if (r, c) in points_visited:
                # Been there already
                continue

            if heightmap[r][c] == 9:
                # High point
                continue

            points_to_visit.add((r, c))

    return [*points_visited]


def find_largest_basins(
    heightmap: List[List[int]], low_points: List[Position], size: MapSize, n: int
) -> List[List[Position]]:
    """Find the `n` largest basins in the `heightmap`"""
    basins: List[List[Position]] = []
    for point in low_points:
        basin = build_basin(heightmap, point, size)
        basins.append(basin)
    basins.sort(key=lambda b: len(b), reverse=True)
    return basins[:n]


if __name__ == "__main__":
    data_path = get_input_path("Day 9: Smoke Basin")
    with open(data_path, "r") as file:
        heightmap = [[int(c) for c in line] for line in file.read().splitlines()]

    start = timer()

    assert len(heightmap) >= 1
    map_size = (len(heightmap), len(heightmap[0]))

    points = find_low_points(heightmap, map_size)
    sum_of_risk_levels = sum([(1 + heightmap[r][c]) for r, c in points])

    basins = find_largest_basins(heightmap, points, map_size, 3)
    product_of_largest_basins = prod([len(basin) for basin in basins])

    stop = timer()

    print("Sum of risk levels of low points:", sum_of_risk_levels)
    print("Product of three largest basins:", product_of_largest_basins)
    print_elapsed_time(start, stop)
