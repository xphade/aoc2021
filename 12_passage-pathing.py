#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Dict, Iterator, List, Optional, Set

START = "start"
END = "end"

CaveMap = Dict[str, Set[str]]
Path = List[str]


def is_small_cave(name: str) -> bool:
    """Return `True` if the cave is a small one"""
    return name.islower()


def get_small_caves(map: CaveMap) -> Iterator[str]:
    """Get all small caves of the `map` (besides start and end)"""
    return filter(lambda c: is_small_cave(c) and c != START and c != END, map)


def explore(
    map: CaveMap,
    visited: Set[str],
    current_path: Path,
    successful_paths: List[Path],
    double_access_cave: Optional[str] = None,
    accessed_twice: bool = False,
) -> None:
    """Explore every possible path of the `map` and find the successful ones"""
    current_cave = current_path[-1]

    # Stopping condition
    if current_cave == END:
        successful_paths.append(current_path)
        return

    if is_small_cave(current_cave):
        # If double access for the current cave is allowed, skip adding the respective
        # cave to the `visited` set this one time
        if double_access_cave == current_cave and not accessed_twice:
            accessed_twice = True
        else:
            visited.add(current_cave)

    for neighbor in map[current_cave]:
        if neighbor in visited:
            continue

        explore(
            map,
            visited.copy(),
            current_path + [neighbor],
            successful_paths,
            double_access_cave,
            accessed_twice,
        )


def generate_cave_map(raw_lines: List[str]) -> CaveMap:
    """Generate a map containing all caves and their respective neighbors"""
    map: CaveMap = {}
    for line in raw_lines:
        entries = line.split("-")
        assert len(entries) == 2
        a, b = entries

        if a not in map:
            map[a] = set()
        if b not in map:
            map[b] = set()

        map[a].add(b)
        map[b].add(a)

    return map


if __name__ == "__main__":
    data_path = get_input_path("Day 12: Passage Pathing")
    with open(data_path, "r") as file:
        lines = file.read().split()
        map = generate_cave_map(lines)

    start = timer()

    visited: Set[str] = set()
    current_path: Path = [START]
    successful_paths: List[Path] = []

    explore(map, visited, current_path, successful_paths)
    paths_without_double_access = len(successful_paths)

    successful_paths.clear()
    for cave in get_small_caves(map):
        visited.clear()
        current_path = [START]
        explore(map, visited, current_path, successful_paths, double_access_cave=cave)

    # It is necessary to remove some duplicated paths
    paths_with_double_access = len(set(tuple(path) for path in successful_paths))

    stop = timer()

    print("Paths without double access:", paths_without_double_access)
    print("Paths with double access:", paths_with_double_access)
    print_elapsed_time(start, stop)
