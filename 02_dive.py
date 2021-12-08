#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import List, Tuple

CMD_FORWARD = "forward"
CMD_DOWN = "down"
CMD_UP = "up"
VALID_COMMANDS = {CMD_FORWARD, CMD_DOWN, CMD_UP}


class ControlInput:
    def __init__(self, input: str):
        cmd_val = input.split(" ")
        assert len(cmd_val) == 2
        assert cmd_val[0] in VALID_COMMANDS

        self.command = cmd_val[0]
        self.value = int(cmd_val[1])


def determine_location(inputs: List[ControlInput]) -> Tuple[int, int]:
    position = 0
    depth = 0

    for input in inputs:
        if input.command == CMD_FORWARD:
            position += input.value
        elif input.command == CMD_DOWN:
            depth += input.value
        elif input.command == CMD_UP:
            depth -= input.value

    return (position, depth)


def determine_location_aim(inputs: List[ControlInput]) -> Tuple[int, int]:
    aim = 0
    position = 0
    depth = 0

    for input in inputs:
        if input.command == CMD_DOWN:
            aim += input.value
        elif input.command == CMD_UP:
            aim -= input.value
        elif input.command == CMD_FORWARD:
            position += input.value
            depth += aim * input.value

    return (position, depth)


if __name__ == "__main__":
    data_path = get_input_path("Day 2: Dive!")
    with open(data_path, "r") as file:
        contents = file.readlines()
        control_inputs = [ControlInput(line) for line in contents]

    start = timer()

    location1 = determine_location(control_inputs)
    product1 = location1[0] * location1[1]

    location2 = determine_location_aim(control_inputs)
    product2 = location2[0] * location2[1]

    stop = timer()

    print(f"Final location: {location1}, h x d = {product1}")
    print(f"True final location (aim-method): {location2}, h x d = {product2}")
    print_elapsed_time(start, stop)
