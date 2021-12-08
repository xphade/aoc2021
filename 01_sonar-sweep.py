#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import List


def count_increases(measurements: List[int]) -> int:
    increases = [cur > prev for prev, cur in zip(measurements[:-1], measurements[1:])]
    return sum(increases)


def count_window_increases(measurements: List[int], window_size: int = 3) -> int:
    window_sums: List[int] = []
    for i in range(len(measurements) - window_size + 1):
        window_sum = sum([measurements[j] for j in range(i, i + window_size)])
        window_sums.append(window_sum)

    window_increases = [
        cur > prev for prev, cur in zip(window_sums[:-1], window_sums[1:])
    ]

    return sum(window_increases)


if __name__ == "__main__":
    data_path = get_input_path("Day 1: Sonar Sweep")
    with open(data_path, "r") as file:
        contents = file.readlines()
        measurements = [int(line) for line in contents]

    start = timer()
    num_increases = count_increases(measurements)
    num_window_increases = count_window_increases(measurements)
    stop = timer()

    print("Number of increasing measurements:", num_increases)
    print(
        "Number of increasing measurements (sliding-window approach):",
        num_window_increases,
    )
    print_elapsed_time(start, stop)
