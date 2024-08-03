"""
Part 1: Simply count the characters in each string, and keep track of how many times a string has a character with
exactly 2 / 3 repetitions. Guess I could have used count from itertools, but meh.
Part 2: Go through the combinations of strings and generate a string of the matching characters; if its length is
exactly 1 smaller, we found the match.
"""
import sys
from itertools import combinations


class Warehouse:
    def __init__(self, rawstr: str) -> None:
        self.__lines = rawstr.splitlines()

    def get_checksum(self) -> int:
        twos = threes = 0
        for line in self.__lines:
            counts = {}
            for c in line:
                counts[c] = 1 if c not in counts else counts[c] + 1
            if 2 in counts.values():
                twos += 1
            if 3 in counts.values():
                threes += 1
        return twos * threes

    def get_common_letters(self) -> str:
        for one, two in combinations(self.__lines, 2):
            common = ''.join([c for i, c in enumerate(one) if one[i] == two[i]])
            if len(common) == len(one) - 1:
                return common
        return ''


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        warehouse = Warehouse(file.read().strip('\n'))
    print(f"Part 1: {warehouse.get_checksum()}")
    print(f"Part 2: {warehouse.get_common_letters()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
