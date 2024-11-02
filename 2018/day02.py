"""
Part 1: Simply count the characters in each string, and keep track of how many times a string has a character with
exactly 2 / 3 repetitions. Guess I could have used count from itertools, but meh.
Part 2: Go through the combinations of strings and generate a string of the matching characters; if its length is
exactly 1 smaller, we found the match.
"""
import time
from pathlib import Path
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


def main(aoc_input: str) -> None:
    warehouse = Warehouse(aoc_input)
    print(f"Part 1: {warehouse.get_checksum()}")
    print(f"Part 2: {warehouse.get_common_letters()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day02.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
