"""
Mostly a parsing exercise, especially for Part 2. Also realizing that the condition for valid triangle can be boiled
down to just checking the sum of the two smallest sides agains the largest side; there is no need to check all
combinations.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day03.txt')


class Triangle:
    def __init__(self, side1: int, side2: int, side3: int) -> None:
        self.__sides = sorted([side1, side2, side3])

    def is_valid(self) -> bool:
        """A triangle is valid if the sum of any two sides is larger than the third side. Since the sides are already
        sorted in increasing order, we only need to check that the sum of the first two is larger than the third."""
        return self.__sides[0] + self.__sides[1] > self.__sides[2]


class DesignOffice:
    def __init__(self, rawstr: str) -> None:
        self.__triangles_row = []
        self.__triangles_col = []
        buffer = [[], [], []]
        for line in rawstr.splitlines():
            nbrs = list(map(int, line.split()))
            self.__triangles_row.append(Triangle(*nbrs))
            for i, n in enumerate(nbrs):
                buffer[i].append(n)
                if len(buffer[i]) == 3:
                    self.__triangles_col.append(Triangle(*buffer[i]))
                    buffer[i] = []

    def get_valid_row_count(self) -> int:
        return sum([1 if t.is_valid() else 0 for t in self.__triangles_row])

    def get_valid_col_count(self) -> int:
        return sum([1 if t.is_valid() else 0 for t in self.__triangles_col])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        office = DesignOffice(file.read().strip('\n'))
    print(f"Part 1: {office.get_valid_row_count()}")
    print(f"Part 2: {office.get_valid_col_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
