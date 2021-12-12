#!/usr/bin/env python3

from aoc_utils import get_input_path, print_elapsed_time
from timeit import default_timer as timer
from typing import Dict, Iterator, List, Optional, Set

START = "start"
END = "end"

Cave = str
CaveMap = Dict[Cave, Set[Cave]]
Path = List[Cave]


def is_small_cave(name: str) -> bool:
    """Return `True` if the cave is a small one"""
    return name.islower()


def get_small_caves(map: CaveMap) -> Iterator[Cave]:
    """Get all small caves of the `map` (besides start and end)"""
    return filter(lambda c: is_small_cave(c) and c != START and c != END, map)


def explore(
    map: CaveMap,
    visited: Set[Cave],
    current_path: Path,
    successful_paths: List[Path],
    double_visit_cave: Optional[Cave] = None,
    visited_twice: bool = False,
) -> None:
    """Explore every possible path of the `map` and find the successful ones

    Note that this method does not work if two big caves are directly connected to each
    other. However, this is not the case for our inputs. If it was, we would  also need
    to track which neighbors of each big cave we have visited.

    Args:
        map (CaveMap): The map of the cave, associating caves to their neighbors
        visited (Set[str]): Set of visited caves (only small caves)
        current_path (Path): The currently explored path
        successful_paths (List[Path]): List of paths which lead to the end
        double_visit_cave (Optional[str], optional): Optional small cave which can be
            visited two times. Defaults to None.
        visited_twice (bool, optional): Flag indicating that the cave has been visited
            twice. Defaults to False.
    """
    current_cave = current_path[-1]

    # Stopping condition
    if current_cave == END:
        successful_paths.append(current_path)
        return

    if is_small_cave(current_cave):
        # If double access for the current cave is allowed, skip adding the respective
        # cave to the `visited` set this one time
        if double_visit_cave == current_cave and not visited_twice:
            visited_twice = True
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
            double_visit_cave,
            visited_twice,
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
        explore(map, visited, current_path, successful_paths, double_visit_cave=cave)

    # It is necessary to remove some duplicated paths
    paths_with_double_access = len(set(tuple(path) for path in successful_paths))

    stop = timer()

    print("Paths without double access:", paths_without_double_access)
    print("Paths with double access:", paths_with_double_access)
    print_elapsed_time(start, stop)
