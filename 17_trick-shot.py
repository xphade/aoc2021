#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
import re
from timeit import default_timer as timer
from typing import Iterable, List, Tuple


def extract_ranges(raw_content: str) -> Tuple[Iterable[int], Iterable[int]]:
    """Extract the x and y target ranges from the raw string"""
    numbers = [*map(int, re.findall(r"-?\d+", raw_content))]
    assert len(numbers) == 4

    range_x = range(numbers[0], numbers[1] + 1)
    range_y = range(numbers[2], numbers[3] + 1)
    return (range_x, range_y)


def calculate_maximum_position(velocity: int) -> int:
    """Calculate the maximum position if `velocity` decreases by one after each step"""
    final_position = (velocity * (velocity + 1)) // 2  # Gauss summation strikes again
    return final_position


def calculate_maximum_height(target: Iterable[int]):
    """Calculate the maximum achievable height given the `target` range"""

    # Maximum velocity such that the probe doesn't overshoot the target on the way down
    max_velocity = abs(min(target)) - 1
    return calculate_maximum_position(max_velocity)


def get_velocity_range_x(target: Iterable[int]) -> Iterable[int]:
    """Get the x-velocity range to reach the `target`"""
    min_velocity = 0
    while calculate_maximum_position(min_velocity) < min(target):
        min_velocity += 1
    max_velocity = max(target)
    return range(min_velocity, max_velocity + 1)


def get_velocity_range_y(target: Iterable[int]) -> Iterable[int]:
    """Get the y-velocity range to reach the `target`"""
    target_minimum = min(target)
    min_velocity = target_minimum
    max_velocity = abs(target_minimum) - 1
    return range(min_velocity, max_velocity + 1)


def is_valid_initial_velocity(
    x_velocity: int, y_velocity: int, x_target: Iterable[int], y_target: Iterable[int]
) -> bool:
    """Check if the probe will hit the target with the given initial velocity"""
    x_position = 0
    y_position = 0
    x_max = max(x_target)
    y_min = min(y_target)

    while x_position <= x_max and y_position >= y_min:
        x_position += x_velocity
        y_position += y_velocity
        x_velocity = max(0, x_velocity - 1)
        y_velocity -= 1

        if x_position in x_target and y_position in y_target:
            return True

    return False


def calculate_valid_initial_velocities(
    x_target: Iterable[int], y_target: Iterable[int]
) -> List[Tuple[int, int]]:
    """Calculate all valid initial velocities"""
    x_velocities = get_velocity_range_x(x_target)
    y_velocities = get_velocity_range_y(y_target)

    valid_velocities: List[Tuple[int, int]] = []

    # For every velocity combination, check if it is valid
    for x_vel in x_velocities:
        for y_vel in y_velocities:
            if is_valid_initial_velocity(x_vel, y_vel, x_target, y_target):
                valid_velocities.append((x_vel, y_vel))
    return valid_velocities


def main():
    data_path = get_input_path("Day 17: Trick Shot")
    with open(data_path, "r") as file:
        content = file.read()
        target_x, target_y = extract_ranges(content)

    start = timer()
    max_height = calculate_maximum_height(target_y)
    valid_velocities = calculate_valid_initial_velocities(target_x, target_y)
    stop = timer()

    print("Maximum reachable height:", max_height)
    print("Number of valid initial velocities:", len(valid_velocities))
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
