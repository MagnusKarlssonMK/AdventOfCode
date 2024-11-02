"""
Parse the input to a list of sorted lists of integers.
For part 1, simply take the sum of the difference between the last and the first value of each list.
For part 2, instead use itertools to find the combination of numbers in each list that yields an even division, and
accumulate the sum of the result of those divisions.
"""
import time
from pathlib import Path
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


def main(aoc_input: str) -> None:
    sheet = Spreadsheet(aoc_input)
    print(f"Part 1: {sheet.get_checksum()}")
    print(f"Part 2: {sheet.get_checksum(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day02.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
