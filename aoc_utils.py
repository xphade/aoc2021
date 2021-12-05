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
