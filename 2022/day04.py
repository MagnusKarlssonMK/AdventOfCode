import time
import re
from pathlib import Path


class Assignments:
    def __init__(self, rawstr: str) -> None:
        self.__pairs = [tuple(map(int, re.findall(r"\d+", line))) for line in rawstr.splitlines()]

    def get_assignments_contained(self) -> int:
        return sum([1 for a, b, c, d in self.__pairs if a <= c <= d <= b or c <= a <= b <= d])

    def get_assignments_overlap(self) -> int:
        return sum([1 for a, b, c, d in self.__pairs if a <= d and c <= b])


def main(aoc_input: str) -> None:
    assignments = Assignments(aoc_input)
    print(f"Part 1: {assignments.get_assignments_contained()}")
    print(f"Part 2: {assignments.get_assignments_overlap()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
