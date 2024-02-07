"""
Create a class to hold each bingo board with methods to draw a number.
Loop through the numbers for each bingo board and save the result for Part 1 on the first bingo.
Loop the boards in reverse order so that they can be popped safely when getting bingo, and keep
going until there is only one board left to get the score for Part 2.

"""
import sys


class BingoBoard:
    def __init__(self, rawstr: str):
        self.__nbrs = []
        [self.__nbrs.append(list(map(int, row.split()))) for row in rawstr.splitlines()]
        self.__rowtotals = [0 for _ in range(len(self.__nbrs))]
        self.__coltotals = [0 for _ in range(len(self.__nbrs[0]))]
        self.__matchnbrs = set()

    def drawnumber(self, nbr) -> int:
        """Returns the card score if bingo, otherwise 0."""
        for row in range(len(self.__nbrs)):
            for col in range(len(self.__nbrs[0])):
                if self.__nbrs[row][col] == nbr:
                    self.__matchnbrs.add(nbr)
                    self.__rowtotals[row] += 1
                    self.__coltotals[col] += 1
                    if self.__rowtotals[row] >= len(self.__coltotals) or self.__coltotals[col] >= len(self.__rowtotals):
                        return self.__calculatescore(nbr)
        return 0

    def __calculatescore(self, lastnbr: int) -> int:
        nomatchsum = 0
        for row in range(len(self.__nbrs)):
            for col in range(len(self.__nbrs[0])):
                if self.__nbrs[row][col] not in self.__matchnbrs:
                    nomatchsum += self.__nbrs[row][col]
        return lastnbr * nomatchsum


def main() -> int:
    with open('../Inputfiles/aoc4.txt', 'r') as file:
        lines = file.read().strip('\n').split('\n\n')
    numbers = list(map(int, lines[0].strip('\n').split(',')))
    boards: list[BingoBoard] = []
    for boardindex in range(1, len(lines)):
        boards.append(BingoBoard(lines[boardindex]))

    p1_score = 0
    p2_score = 0
    for nbr in numbers:
        for b in reversed(range(len(boards))):
            result = boards[b].drawnumber(nbr)
            if result > 0:
                if p1_score == 0:
                    p1_score = result
                if len(boards) == 1:
                    p2_score = result
                boards.pop(b)
    print("Part 1: ", p1_score)
    print("Part 2: ", p2_score)
    return 0


if __name__ == "__main__":
    sys.exit(main())
