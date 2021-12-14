#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from collections import defaultdict
from timeit import default_timer as timer
from typing import DefaultDict, Dict, Tuple


def polymerize(template: str, rules: Dict[str, str]) -> str:
    """Polymerize a new polymer according to the given `template` and `rules`"""
    new_polymer: str = ""
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        insertion = rules[pair]
        new_polymer += pair[0] + insertion

    # The last character is missing at this point, so add it
    new_polymer += template[-1]
    return new_polymer


def count_pairs_and_characters(
    template: str,
) -> Tuple[DefaultDict[str, int], DefaultDict[str, int]]:
    """Count the pairs and single characters in the given `template`"""
    pair_count: DefaultDict[str, int] = defaultdict(int)
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        pair_count[pair] += 1

    char_count: DefaultDict[str, int] = defaultdict(
        int, {c: template.count(c) for c in set(template)}
    )

    return (pair_count, char_count)


def polymerize_virtually(
    pair_count: DefaultDict[str, int],
    char_count: DefaultDict[str, int],
    rules: Dict[str, str],
) -> None:
    """Polymerize virtually by counting pairs and single elements"""
    for element, count in pair_count.copy().items():
        # Count the newly inserted character
        insertion = rules[element]
        char_count[insertion] += count

        # Update the counter for pairs (remove existing, add newly generated ones)
        pair_count[element] -= count
        pair_count[element[0] + insertion] += count
        pair_count[insertion + element[1]] += count


def main():
    data_path = get_input_path("Day 14: Extended Polymerization")
    with open(data_path, "r") as file:
        polymer_template, raw_rules = file.read().split("\n\n")

        insertion_rules: Dict[str, str] = {}
        for rule in raw_rules.splitlines():
            template, insertion = rule.split(" -> ")
            insertion_rules[template] = insertion

    start = timer()

    # Part 1: Generate the actual polymer
    polymer = polymer_template
    for _ in range(10):
        polymer = polymerize(polymer, insertion_rules)
    small_count = {c: polymer.count(c) for c in set(polymer)}
    small_polymer_result = max(small_count.values()) - min(small_count.values())

    # Part 2: Perform the polymerization "virtually" by counting the characters
    pair_count, char_count = count_pairs_and_characters(polymer_template)
    for _ in range(40):
        polymerize_virtually(pair_count, char_count, insertion_rules)
    big_polymer_result = max(char_count.values()) - min(char_count.values())

    stop = timer()

    print("Difference for the small polymer (10 steps):", small_polymer_result)
    print("Difference for the big polymer (40 steps):", big_polymer_result)
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
