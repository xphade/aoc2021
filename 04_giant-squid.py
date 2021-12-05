#!/usr/bin/env python3

from aoc_utils import get_input_path
from typing import Dict, List, Tuple


class BingoBoard:
    def __init__(self, board: List[List[str]]) -> None:
        self.size = len(board)  # assuming square board
        self.entries: Dict[int, Tuple[int, int]] = {}

        for i in range(self.size):
            for j in range(self.size):
                number = int(board[i][j])
                self.entries[number] = (i, j)

        self.row_hits = [0] * self.size
        self.col_hits = [0] * self.size
        self.marked_numbers: List[int] = []

    def mark(self, number: int) -> None:
        if number in self.marked_numbers:
            return

        if number in self.entries:
            self.marked_numbers.append(number)

            row = self.entries[number][0]
            col = self.entries[number][1]
            self.row_hits[row] += 1
            self.col_hits[col] += 1

    def bingo(self) -> bool:
        bingo = self.size in self.row_hits or self.size in self.col_hits
        return bingo

    def score(self) -> int:
        assert self.bingo()
        return sum(filter(lambda n: n not in self.marked_numbers, self.entries.keys()))


def calculate_bingo_scores(numbers: List[int], boards: List[BingoBoard]) -> List[int]:
    scores: List[int] = []
    finished_boards: List[int] = []

    for number in numbers:
        for idx, board in enumerate(boards):
            if idx in finished_boards:
                continue

            board.mark(number)
            if board.bingo():
                scores.append(board.score() * number)
                finished_boards.append(idx)

    return scores


if __name__ == "__main__":
    data_path = get_input_path("Day 4: Giant Squid")
    with open(data_path, "r") as file:
        blocks = file.read().split("\n\n")

    drawn_numbers = [int(number) for number in blocks[0].split(",")]
    boards: List[BingoBoard] = []

    for block in blocks[1:]:
        lines = block.split("\n")
        board = [line.split() for line in lines if len(line) != 0]
        boards.append(BingoBoard(board))

    scores = calculate_bingo_scores(drawn_numbers, boards)
    assert len(scores) >= 2
    print(f"Score of first bingo: {scores[0]}")
    print(f"Score of final bingo: {scores[-1]}")
