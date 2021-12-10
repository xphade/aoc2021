#!/usr/bin/env python3

from typing import Dict, List, Optional, Tuple
from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer

SYNTAX_SCORE: Dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETION_SCORE: Dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}
ASSOCIATED_BRACKET: Dict[str, str] = {"(": ")", "[": "]", "{": "}", "<": ">"}


def is_opening_bracket(bracket: str) -> bool:
    return bracket in ASSOCIATED_BRACKET


def is_valid_bracket_pair(first_bracket: str, second_bracket: str) -> bool:
    return (
        first_bracket in ASSOCIATED_BRACKET
        and second_bracket == ASSOCIATED_BRACKET[first_bracket]
    )


def find_illegal_character(chunk: str) -> Optional[str]:
    """Find the first illegal character if the given `chunk` is invalid"""
    stack: List[str] = []
    for bracket in chunk:
        if is_opening_bracket(bracket):
            stack.append(bracket)
        else:
            assert len(stack) > 0
            previous_bracket = stack.pop()
            if not is_valid_bracket_pair(previous_bracket, bracket):
                return bracket

    # Again no check if chunk is incomplete
    return None


def find_completion_sequence(chunk: str) -> List[str]:
    """Find the completion sequence given an incomplete (but valid) `chunk`"""
    stack: List[str] = []
    completion_sequence: List[str] = []
    for bracket in chunk:
        if is_opening_bracket(bracket):
            stack.append(bracket)
        else:
            previous_bracket = stack.pop()
            assert is_valid_bracket_pair(previous_bracket, bracket)

    # Now look at the remaining brackets
    for bracket in reversed(stack):
        completion_sequence.append(ASSOCIATED_BRACKET[bracket])

    return completion_sequence


def calculate_scores(chunks: List[str]) -> Tuple[int, int]:
    """Calculate in syntax error and middle completion score"""
    syntax_error_score: int = 0
    autocomplete_scores: List[int] = []

    for chunk in chunks:
        illegal_character = find_illegal_character(chunk)

        if illegal_character:
            syntax_error_score += SYNTAX_SCORE[illegal_character]
        else:
            sequence = find_completion_sequence(chunk)
            total_score = 0
            for bracket in sequence:
                total_score = (5 * total_score) + COMPLETION_SCORE[bracket]
            autocomplete_scores.append(total_score)

    middle_score = sorted(autocomplete_scores)[len(autocomplete_scores) // 2]
    return (syntax_error_score, middle_score)


if __name__ == "__main__":
    data_path = get_input_path("Day 10: Syntax Scoring")
    with open(data_path, "r") as file:
        chunks = file.read().splitlines()

    start = timer()
    syntax_error_score, middle_score = calculate_scores(chunks)
    stop = timer()

    print(syntax_error_score)
    print(middle_score)
    print_elapsed_time(start, stop)
