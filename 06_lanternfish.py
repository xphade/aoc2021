#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Dict, List

REPRODUCTION_TIME: int = 6
INITIAL_REPRODUCTION_TIME: int = 8


def set_up_population(initial_population: List[int]) -> Dict[int, int]:
    # Model population as a dictionary mapping reproduction time to number of fish
    population = {
        time: initial_population.count(time)
        for time in range(INITIAL_REPRODUCTION_TIME + 1)
    }
    return population


def update_population(population: Dict[int, int]) -> None:
    number_of_reproductions = population[0]

    # Update population times (shift left)
    for time in range(1, INITIAL_REPRODUCTION_TIME + 1):
        population[time - 1] = population[time]

    # Handle special case (reproduction) separately
    population[REPRODUCTION_TIME] += number_of_reproductions
    population[INITIAL_REPRODUCTION_TIME] = number_of_reproductions


def simulate(population: Dict[int, int], days: int) -> None:
    for _ in range(days):
        update_population(population)


if __name__ == "__main__":
    data_path = get_input_path("Day 6: Lanternfish")
    with open(data_path, "r") as file:
        initial_population = [*map(int, file.read().split(","))]

    start = timer()

    result: Dict[int, int] = {}
    for days in {80, 256}:
        population = set_up_population(initial_population)
        simulate(population, days)
        result[days] = sum(population.values())

    stop = timer()

    print(f"Population after 80 days: {result[80]}")
    print(f"Population after 256 days: {result[256]}")
    print_elapsed_time(start, stop)
