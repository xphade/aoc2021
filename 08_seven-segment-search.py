#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Callable, Dict, List

# Mapping signal patterns (sorted) to digits
PatternMap = Dict[str, int]


class NoteEntry:
    def __init__(self, raw_entry: str) -> None:
        patterns_and_output = raw_entry.split(" | ")
        assert len(patterns_and_output) == 2

        self.signal_patterns = patterns_and_output[0].split()
        self.output_value = patterns_and_output[1].split()
        assert len(self.signal_patterns) == 10 and len(self.output_value) == 4


def sorted_str(s: str) -> str:
    """Sort `s` alphabetically and return it"""
    return "".join(sorted(s))


def find_pattern(patterns: List[str], filter_func: Callable[[str], bool]) -> str:
    """Find the pattern defined by `filter_func` in the list of `patterns`"""
    find_result = [*filter(filter_func, patterns)]
    assert len(find_result) == 1
    return find_result[0]


def contains_pattern(input: str, pattern: str) -> bool:
    """Check if the `input` contains all signals of the given `pattern`"""
    assert len(input) >= len(pattern)
    return all([p in input for p in pattern])


def build_pattern_map(patterns: List[str]) -> PatternMap:
    """Build the dictionary mapping patterns to the respective digits"""
    sorted_patterns = [*map(sorted_str, patterns)]
    pattern_results = [""] * 10

    # Start with digits with a distinct length
    pattern_results[1] = find_pattern(sorted_patterns, lambda s: len(s) == 2)
    sorted_patterns.remove(pattern_results[1])

    pattern_results[4] = find_pattern(sorted_patterns, lambda s: len(s) == 4)
    sorted_patterns.remove(pattern_results[4])

    pattern_results[7] = find_pattern(sorted_patterns, lambda s: len(s) == 3)
    sorted_patterns.remove(pattern_results[7])

    pattern_results[8] = find_pattern(sorted_patterns, lambda s: len(s) == 7)
    sorted_patterns.remove(pattern_results[8])

    # Now deduce the rest of the digits from the already known patterns
    pattern_results[3] = find_pattern(
        sorted_patterns,
        lambda s: contains_pattern(s, pattern_results[1]) and len(s) == 5,
    )
    sorted_patterns.remove(pattern_results[3])

    pattern_results[6] = find_pattern(
        sorted_patterns,
        lambda s: not contains_pattern(s, pattern_results[1]) and len(s) == 6,
    )
    sorted_patterns.remove(pattern_results[6])

    pattern_results[9] = find_pattern(
        sorted_patterns, lambda s: contains_pattern(s, pattern_results[3])
    )
    sorted_patterns.remove(pattern_results[9])

    pattern_results[0] = find_pattern(sorted_patterns, lambda s: len(s) == 6)
    sorted_patterns.remove(pattern_results[0])

    pattern_results[5] = find_pattern(
        sorted_patterns, lambda s: contains_pattern(pattern_results[6], s)
    )
    sorted_patterns.remove(pattern_results[5])

    # Digit 2 is the only one left
    pattern_results[2] = sorted_patterns.pop()
    return {pattern: i for i, pattern in enumerate(pattern_results)}


if __name__ == "__main__":
    data_path = get_input_path("Day 8: Seven Segment Search")
    with open(data_path, "r") as file:
        raw_notes = file.readlines()
    notes = [NoteEntry(raw_entry) for raw_entry in raw_notes]

    start = timer()

    # Part 1: Filter flat list of digits for 1, 4 ,7 and 8 (by their unique length)
    output_digits = [digit for note in notes for digit in note.output_value]
    filtered_digits = [*filter(lambda x: len(x) in {2, 3, 4, 7}, output_digits)]

    # Part 2: Decode the patterns and use them to calculate the sum of output values
    sum = 0
    for note in notes:
        pattern_map = build_pattern_map(note.signal_patterns)
        digits = [pattern_map[sorted_str(pattern)] for pattern in note.output_value]
        sum += int("".join(map(str, digits)))

    stop = timer()

    print(f"Appearances of digits 1, 4, 7 and 8: {len(filtered_digits)}")
    print(f"Sum of output values: {sum}")
    print_elapsed_time(start, stop)
