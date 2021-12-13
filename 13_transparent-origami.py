#!/usr/bin/env python3

from typing import List, Set, Tuple
from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer

DotSet = Set[Tuple[int, int]]
Instruction = Tuple[str, int]


def fold(paper: DotSet, instruction: Instruction) -> DotSet:
    """Fold the given `paper` according to the `instruction` and return it"""
    axis, line = instruction
    index = 0 if axis == "x" else 1

    folded_paper: DotSet = set()
    for dot in paper:
        if dot[index] <= line:
            folded_paper.add(dot)
        else:
            new_line = line - (dot[index] - line)
            folded_paper.add((new_line, dot[1]) if axis == "x" else (dot[0], new_line))

    return folded_paper


def get_dimensions(paper: DotSet) -> Tuple[int, int]:
    """Return width and height of the `paper`"""
    width = max(paper, key=lambda coord: coord[0])[0] + 1
    height = max(paper, key=lambda coord: coord[1])[1] + 1
    return (width, height)


def main():
    data_path = get_input_path("Day 13: Transparent Origami")
    with open(data_path, "r") as file:
        raw_paper, raw_instructions = file.read().split("\n\n")

        paper: DotSet = set()
        for line in raw_paper.splitlines():
            x, y = map(int, line.split(","))
            paper.add((x, y))

        instructions: List[Instruction] = []
        for line in raw_instructions.splitlines():
            instruction, line_number = line.split("=")
            instructions.append((instruction[-1], int(line_number)))

    start = timer()

    # Fold the paper once for the first part
    paper = fold(paper, instructions[0])
    dots_after_first_fold = len(paper)

    # Now apply the rest of the instructions
    for instruction in instructions[1:]:
        paper = fold(paper, instruction)

    stop = timer()

    print("Number of dots after first fold:", dots_after_first_fold)

    print("Code word:")
    width, height = get_dimensions(paper)
    for j in range(height):
        line = "".join(["#" if (i, j) in paper else " " for i in range(width)])
        print(line)

    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
