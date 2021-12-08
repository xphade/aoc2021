from argparse import ArgumentParser
from pathlib import Path


def get_input_path(message: str) -> Path:
    parser = ArgumentParser(description=message)
    parser.add_argument("input_path", type=Path, help="Path to the input file")
    args = parser.parse_args()
    path: Path = args.input_path

    if not path.exists() or not path.is_file():
        parser.error("Input path must be a valid file")

    return path


def print_elapsed_time(start: float, stop: float) -> None:
    time_diff = stop - start
    n = 1
    while time_diff < 1 and n <= 3:
        time_diff *= 1000
        n += 1

    units = {1: "s", 2: "ms", 3: "µs", 4: "ns"}
    print(f"Elapsed time: {time_diff:.2f} {units[n]}")
