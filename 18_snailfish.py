#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from math import ceil, floor
import re
from timeit import default_timer as timer
from typing import List

RE_LAST_NUMBER = re.compile(r"(\d+)(?!.*\d)")
RE_NUMBER = re.compile(r"\d+")
RE_PAIR = re.compile(r"\[\d+,\d+\]")
RE_NUMBER_GT_10 = re.compile(r"[\d]{2,}")

SnailfishNumber = str


def add_without_reduce(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    """Add the two snailfish numbers` a and b without reducing them"""
    return "[" + a + "," + b + "]"


def insert(s: str, startpos: int, endpos: int, value: str) -> str:
    """Insert `value` into string `s` at the specified position"""
    return s[:startpos] + value + s[endpos:]


def explode(number: SnailfishNumber) -> SnailfishNumber:
    """Perform a single explode operation on the given snailfish `number`"""
    level = 0
    for idx, char in enumerate(number):
        if char == "[":
            level += 1
        elif char == "]":
            level -= 1

        if level == 5:
            pair_match = RE_PAIR.search(number, pos=idx)
            assert pair_match != None

            pair = [*map(int, pair_match.group()[1:-1].split(","))]
            number = insert(number, pair_match.start(), pair_match.end(), "0")

            left = RE_LAST_NUMBER.search(number, endpos=idx)
            right = RE_NUMBER.search(number, pos=idx + 2)

            if right != None:
                updated_value = int(right.group()) + pair[1]
                number = insert(number, right.start(), right.end(), str(updated_value))

            if left != None:
                updated_value = int(left.group()) + pair[0]
                number = insert(number, left.start(), left.end(), str(updated_value))

            # Updated the number, break out of the loop
            break

    return number


def split(number: SnailfishNumber) -> SnailfishNumber:
    """Perform a single split operation on the given snailfish `number`"""
    big_value_match = RE_NUMBER_GT_10.search(number)
    if big_value_match == None:
        return number

    value = int(big_value_match.group())
    left = floor(value / 2)
    right = ceil(value / 2)
    new_pair = add_without_reduce(str(left), str(right))

    return insert(number, big_value_match.start(), big_value_match.end(), new_pair)


def reduce(number: SnailfishNumber) -> SnailfishNumber:
    """Reduce (explode and split) the given snailfish `number`"""
    while True:
        updated_number = explode(number)
        if updated_number != number:
            number = updated_number
            continue

        updated_number = split(number)
        if updated_number != number:
            number = updated_number
            continue

        # Both explore and split did not change the number, so we're finished
        return updated_number


def add_numbers(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    """Add the two snailfish numbers `a` and `b`"""
    unreduced = add_without_reduce(a, b)
    return reduce(unreduced)


def calculate_magnitude(number: SnailfishNumber) -> int:
    """Calculate the magnitude of the given `number`"""
    while (pair_match := RE_PAIR.search(number)) != None:
        pair = [*map(int, pair_match.group()[1:-1].split(","))]
        result = (3 * pair[0]) + (2 * pair[1])
        number = insert(number, pair_match.start(), pair_match.end(), str(result))
    return int(number)


def calculate_largest_magnitude(numbers: List[SnailfishNumber]) -> int:
    """Calculate the largest magnitude of the sum of any two `numbers`"""
    current_max: int = 0
    for idx, a in enumerate(numbers):
        for b in numbers[idx:]:
            current_max = max(current_max, calculate_magnitude(add_numbers(a, b)))
            current_max = max(current_max, calculate_magnitude(add_numbers(b, a)))
    return current_max


def main():
    data_path = get_input_path("Day 18: Snailfish")
    with open(data_path, "r") as file:
        input_numbers: List[SnailfishNumber] = file.read().splitlines()

    start = timer()

    final_sum = input_numbers[0]
    for number in input_numbers[1:]:
        final_sum = add_numbers(final_sum, number)

    final_sum_magnitude = calculate_magnitude(final_sum)
    largest_magnitude = calculate_largest_magnitude(input_numbers)

    stop = timer()

    print("Magnitude of the final sum:", final_sum_magnitude)
    print("Largest magnitude of two numbers:", largest_magnitude)
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
