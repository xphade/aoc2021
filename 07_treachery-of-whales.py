#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Callable, List, Optional, Tuple

Position = int
Fuel = int


def cost_part1(x: Position, y: Position) -> Fuel:
    return abs(x - y)


def cost_part2(x: Position, y: Position) -> Fuel:
    diff = abs(x - y)
    # Gauss summation (sum of numbers from 1 to diff)
    return Fuel(diff * (diff + 1) / 2)


def find_optimal_position(
    positions: List[Position], cost_func: Callable[[Position, Position], Fuel]
) -> Tuple[Position, Fuel]:

    best_position: Optional[Position] = None
    best_cost: Optional[Fuel] = None

    for location in range(min(positions), max(positions) + 1):
        cost = sum([cost_func(p, location) for p in positions])
        if not best_cost or cost < best_cost:
            best_position = location
            best_cost = cost

    assert best_position and best_cost
    return (best_position, best_cost)


if __name__ == "__main__":
    data_path = get_input_path("Day 7: The Treachery of Whales")
    with open(data_path, "r") as file:
        crab_positions = [*map(Position, file.read().split(","))]

    start = timer()
    position1, fuel1 = find_optimal_position(crab_positions, cost_part1)
    position2, fuel2 = find_optimal_position(crab_positions, cost_part2)
    stop = timer()

    print(f"Position and fuel consumption (1st part): {position1}, {fuel1}")
    print(f"Position and fuel consumption (2nd part): {position2}, {fuel2}")
    print_elapsed_time(start, stop)
