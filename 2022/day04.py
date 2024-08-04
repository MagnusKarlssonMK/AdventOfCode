import sys
import re
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day04.txt')


class Assignments:
    def __init__(self, rawstr: str) -> None:
        self.__pairs = [tuple(map(int, re.findall(r"\d+", line))) for line in rawstr.splitlines()]

    def get_assignments_contained(self) -> int:
        return sum([1 for a, b, c, d in self.__pairs if a <= c <= d <= b or c <= a <= b <= d])

    def get_assignments_overlap(self) -> int:
        return sum([1 for a, b, c, d in self.__pairs if a <= d and c <= b])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        assignments = Assignments(file.read().strip('\n'))
    print(f"Part 1: {assignments.get_assignments_contained()}")
    print(f"Part 2: {assignments.get_assignments_overlap()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
