"""
Parse the input to a list of sorted lists of integers.
For part 1, simply take the sum of the difference between the last and the first value of each list.
For part 2, instead use itertools to find the combination of numbers in each list that yields an even division, and
accumulate the sum of the result of those divisions.
"""
import sys
from itertools import combinations


class Spreadsheet:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [sorted(int(n) for n in line.split()) for line in rawstr.splitlines()]

    def get_checksum(self, evendiv: bool = False) -> int:
        if not evendiv:
            return sum([line[-1] - line[0] for line in self.__nbrs])
        else:
            result = 0
            for line in self.__nbrs:
                for p1, p2 in sorted(combinations(line, 2)):
                    if p2 % p1 == 0:
                        result += p2 // p1
                        break
            return result


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        sheet = Spreadsheet(file.read().strip('\n'))
    print(f"Part 1: {sheet.get_checksum()}")
    print(f"Part 2: {sheet.get_checksum(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
