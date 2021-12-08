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


def sortedStr(s: str) -> str:
    """Sort `s` alphabetically and return it"""
    return "".join(sorted(s))


def findPattern(patterns: List[str], filter_func: Callable[[str], bool]) -> str:
    """Find the pattern defined by `filter_func` in the list of `patterns`"""
    findResult = [*filter(filter_func, patterns)]
    assert len(findResult) == 1
    return findResult[0]


def containsPattern(input: str, pattern: str) -> bool:
    """Check if the `input` contains all signals of the given `pattern`"""
    assert len(input) >= len(pattern)
    return all([p in input for p in pattern])


def buildPatternMap(patterns: List[str]) -> PatternMap:
    """Build the dictionary mapping patterns to the respective digits"""
    sortedPatterns = [*map(sortedStr, patterns)]
    patternResults = [""] * 10

    # Start with digits with a distinct length
    patternResults[1] = findPattern(sortedPatterns, lambda s: len(s) == 2)
    sortedPatterns.remove(patternResults[1])

    patternResults[4] = findPattern(sortedPatterns, lambda s: len(s) == 4)
    sortedPatterns.remove(patternResults[4])

    patternResults[7] = findPattern(sortedPatterns, lambda s: len(s) == 3)
    sortedPatterns.remove(patternResults[7])

    patternResults[8] = findPattern(sortedPatterns, lambda s: len(s) == 7)
    sortedPatterns.remove(patternResults[8])

    # Now deduce the rest of the digits from the already known patterns
    patternResults[3] = findPattern(
        sortedPatterns,
        lambda s: containsPattern(s, patternResults[1]) and len(s) == 5,
    )
    sortedPatterns.remove(patternResults[3])

    patternResults[6] = findPattern(
        sortedPatterns,
        lambda s: not containsPattern(s, patternResults[1]) and len(s) == 6,
    )
    sortedPatterns.remove(patternResults[6])

    patternResults[9] = findPattern(
        sortedPatterns, lambda s: containsPattern(s, patternResults[3])
    )
    sortedPatterns.remove(patternResults[9])

    patternResults[0] = findPattern(sortedPatterns, lambda s: len(s) == 6)
    sortedPatterns.remove(patternResults[0])

    patternResults[5] = findPattern(
        sortedPatterns, lambda s: containsPattern(patternResults[6], s)
    )
    sortedPatterns.remove(patternResults[5])

    # Digit 2 is the only one left
    patternResults[2] = sortedPatterns.pop()
    return {pattern: i for i, pattern in enumerate(patternResults)}


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
        patternMap = buildPatternMap(note.signal_patterns)
        digits = [patternMap[sortedStr(pattern)] for pattern in note.output_value]
        sum += int("".join(map(str, digits)))

    stop = timer()

    print(f"Appearances of digits 1, 4, 7 and 8: {len(filtered_digits)}")
    print(f"Sum of output values: {sum}")
    print_elapsed_time(start, stop)
