#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from collections import defaultdict
from heapq import heappop, heappush
from sys import maxsize as MAXIMUM_DISTANCE
from timeit import default_timer as timer
from typing import DefaultDict, Iterator, List, Optional, Set, Tuple


Coordinate = Tuple[int, int]


def in_bounds(coordinate: Coordinate, size: int) -> bool:
    """Check if the given `coordinate` is in bounds"""
    r, c = coordinate
    return (r >= 0) and (r < size) and (c >= 0) and (c < size)


def adjacent_coordinates(coordinate: Coordinate, size: int) -> Iterator[Coordinate]:
    """Return coordinates of adjacent points of the given `coordinate`"""
    r, c = coordinate
    adjacent_coordinates = [
        (r - 1, c),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c),
    ]
    return filter(lambda c: in_bounds(c, size), adjacent_coordinates)


def wrap_around(number: int, start: int, limit: int) -> int:
    """Returns the given number, wrapped around in range `[start, limit[`"""
    return start + ((number - start) % (limit - start))


def extend_map(risk_levels: List[List[int]]) -> List[List[int]]:
    """Extend the `risk_levels` five times in each dimension"""
    original_map = risk_levels.copy()
    for i in range(1, 5):
        for line in original_map:
            risk_levels.append([wrap_around(int(risk) + i, 1, 10) for risk in line])

    for line in risk_levels:
        orinal_line = line.copy()
        for i in range(1, 5):
            line += [wrap_around(int(risk) + i, 1, 10) for risk in orinal_line]

    return risk_levels


def lowest_path_cost(risk_levels: List[List[int]]) -> Optional[int]:
    """Calculate the lowest-cost path in the `risk_levels` map"""
    distances: DefaultDict[Coordinate, int] = defaultdict(
        lambda: MAXIMUM_DISTANCE, {(0, 0): 0}
    )
    visited: Set[Coordinate] = set()
    heap: List[Tuple[int, Coordinate]] = [(0, (0, 0))]

    # Assuming we have a square map
    size = len(risk_levels)

    # Destination is defined as the lower-right corner
    destination_node: Coordinate = (size - 1, size - 1)
    destination_distance: Optional[int] = None

    while len(heap) > 0:
        distance, node = heappop(heap)

        if node == destination_node:
            destination_distance = distance
            break

        for coord in adjacent_coordinates(node, size):
            if coord in visited:
                continue

            row, col = coord
            new_distance = distance + risk_levels[row][col]

            if new_distance < distances[coord]:
                distances[coord] = new_distance
                heappush(heap, (new_distance, coord))

        visited.add(node)

    return destination_distance


def main():
    data_path = get_input_path("Day 15: Chiton")
    with open(data_path, "r") as file:
        risk_levels: List[List[int]] = []
        for line in file.read().splitlines():
            risk_levels.append([int(risk) for risk in line])

    start = timer()

    # Part 1: Calculate the lowest path cost in the original map
    small_map_risk = lowest_path_cost(risk_levels)

    # Part 2: Extend the map (25x bigger) and calculate the lowest path cost again
    risk_levels = extend_map(risk_levels)
    full_map_risk = lowest_path_cost(risk_levels)

    stop = timer()

    assert small_map_risk != None
    assert full_map_risk != None

    print("Lowest total risk in small map:", small_map_risk)
    print("Lowest total risk in full map:", full_map_risk)
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
