import sys
from pathlib import Path
from itertools import combinations

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day02.txt')


class PresentList:
    def __init__(self, rawstr: str) -> None:
        self.__dimensions = [tuple(map(int, line.split('x'))) for line in rawstr.splitlines()]

    def get_paper_total(self) -> int:
        paper = 0
        for present in self.__dimensions:
            areas = [x * y for x, y in combinations(present, 2)]
            paper += 2 * sum(areas) + min(areas)
        return paper

    def get_ribbon_total(self) -> int:
        ribbon = 0
        for present in self.__dimensions:
            dims = sorted(present)
            ribbon += 2 * (dims[0] + dims[1]) + (dims[0] * dims[1] * dims[2])
        return ribbon


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        presents = PresentList(file.read().strip('\n'))
    print(f"Part 1: {presents.get_paper_total()}")
    print(f"Part 2: {presents.get_ribbon_total()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
