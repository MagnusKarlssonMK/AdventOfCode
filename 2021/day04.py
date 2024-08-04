"""
Create a class to hold each bingo board with methods to draw a number.
Loop through the numbers for each bingo board and save the result for Part 1 on the first bingo.
Loop the boards in reverse order so that they can be popped safely when getting bingo, and keep
going until there is only one board left to get the score for Part 2.

"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2021/day04.txt')


class BingoBoard:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = []
        [self.__nbrs.append(list(map(int, row.split()))) for row in rawstr.splitlines()]
        self.__rowtotals = [0 for _, _ in enumerate(self.__nbrs)]
        self.__coltotals = [0 for _, _ in enumerate(self.__nbrs[0])]
        self.__matchnbrs = set()

    def drawnumber(self, nbr) -> int:
        """Returns the card score if bingo, otherwise 0."""
        for row, _ in enumerate(self.__nbrs):
            for col, _ in enumerate(self.__nbrs[0]):
                if self.__nbrs[row][col] == nbr:
                    self.__matchnbrs.add(nbr)
                    self.__rowtotals[row] += 1
                    self.__coltotals[col] += 1
                    if self.__rowtotals[row] >= len(self.__coltotals) or self.__coltotals[col] >= len(self.__rowtotals):
                        return self.__calculatescore(nbr)
        return 0

    def __calculatescore(self, lastnbr: int) -> int:
        nomatchsum = 0
        for row, _ in enumerate(self.__nbrs):
            for col, _ in enumerate(self.__nbrs[0]):
                if self.__nbrs[row][col] not in self.__matchnbrs:
                    nomatchsum += self.__nbrs[row][col]
        return lastnbr * nomatchsum


class BingoModule:
    def __init__(self, rawinput: str) -> None:
        blocks = rawinput.split('\n\n')
        self.__nbrs = list(map(int, blocks[0].split(',')))
        self.__boards = [BingoBoard(blocks[b_idx]) for b_idx in range(1, len(blocks))]

    def get_scores(self) -> tuple[int, int]:  # (Part1, Part2)
        p1_score = 0
        p2_score = 0
        for nbr in self.__nbrs:
            for b in reversed(range(len(self.__boards))):
                if (result := self.__boards[b].drawnumber(nbr)) > 0:
                    if p1_score == 0:
                        p1_score = result
                    if len(self.__boards) == 1:
                        p2_score = result
                    self.__boards.pop(b)
        return p1_score, p2_score


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        bingo = BingoModule(file.read().strip('\n'))
    p1_score, p2_score = bingo.get_scores()
    print(f"Part 1: {p1_score}")
    print(f"Part 2: {p2_score}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
