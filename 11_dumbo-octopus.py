#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Iterator, List, Optional, Tuple

MATRIX_SIZE = 10
Position = Tuple[int, int]


def inside_matrix(coordinate: Position) -> bool:
    """Check if the given `coordinate` is inside the states matrix"""
    r, c = coordinate
    return (r >= 0) and (r < MATRIX_SIZE) and (c >= 0) and (c < MATRIX_SIZE)


def get_adjacent_positions(coordinate: Position) -> Iterator[Position]:
    """Return adjacent points of the given `coordinate`"""
    r, c = coordinate
    adjacent_positions = [
        (r - 1, c - 1),
        (r - 1, c),
        (r - 1, c + 1),
        (r, c - 1),
        (r, c + 1),
        (r + 1, c - 1),
        (r + 1, c),
        (r + 1, c + 1),
    ]
    return filter(inside_matrix, adjacent_positions)


def traverse_matrix(size: int) -> Iterator[Position]:
    """Helper function for traversing the nested list"""
    for r in range(size):
        for c in range(size):
            yield (r, c)


def take_step(energy_levels: List[List[int]]) -> int:
    """Update the energy levels and return the total number of flashes"""

    # First part: Increment energy levels, store flash positions
    flashes: List[Position] = []
    for coordinate in traverse_matrix(MATRIX_SIZE):
        r, c = coordinate
        energy_levels[r][c] += 1
        if energy_levels[r][c] == 10:
            flashes.append(coordinate)

    # Second part: Continuously update positions affected by flashes
    while len(flashes) > 0:
        flash_position = flashes.pop(0)
        for position in get_adjacent_positions(flash_position):
            r, c = position
            energy_levels[r][c] += 1
            if energy_levels[r][c] == 10:
                flashes.append((r, c))

    # Finally: Count the number of flashes and reset the respective positions
    number_of_flashes = 0
    for coordinate in traverse_matrix(MATRIX_SIZE):
        r, c = coordinate
        if energy_levels[r][c] >= 10:
            number_of_flashes += 1
            energy_levels[r][c] = 0

    return number_of_flashes


if __name__ == "__main__":
    data_path = get_input_path("Day 11: Dumbo Octopus")
    with open(data_path, "r") as file:
        energy_levels = [[*map(int, line)] for line in file.read().splitlines()]

    start = timer()

    steps = 0
    required_steps = 100

    result_part1 = 0
    result_part2: Optional[int] = None

    while result_part2 == None:
        number_of_flashes = take_step(energy_levels)
        steps += 1

        if steps <= required_steps:
            result_part1 += number_of_flashes

        if number_of_flashes == MATRIX_SIZE * MATRIX_SIZE:
            result_part2 = steps

    stop = timer()

    print(f"Total number of flashes after {required_steps} steps: {result_part1}")
    print(f"First step during which all octopuses flash: {result_part2}")
    print_elapsed_time(start, stop)
