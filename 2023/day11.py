"""
Stores the coordinates of galaxies in a Space class, and also generates lists of empty rows and columns. For Part 1,
the distance is then calculated with the manhattan distance between each pair of galaxies, and for each pair also
checking the number of empty rows/columns between them. Since the grid input doesn't change between Part 1 & 2 other
than the scaling of empty space, we can calculate the answers to both part 1 and 2 at the same time by not evaluating
the value of empty space until the last step everything has been assembled.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from itertools import combinations

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day11.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_x_ranges(self, other: "Point") -> tuple[int, int]:
        return min(self.x, other.x), max(self.x, other.x)

    def get_y_ranges(self, other: "Point") -> tuple[int, int]:
        return min(self.y, other.y), max(self.y, other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x


class Space:
    __SMALL_EXPANSION_RATE = 2
    __LARGE_EXPANSION_RATE = 1_000_000

    def __init__(self, rawstr: str) -> None:
        self.__galaxies: list[Point] = [Point(x, y) for y, line in enumerate(rawstr.splitlines())
                                        for x, c in enumerate(line) if c == "#"]

    def get_distance_sum(self) -> tuple[int, int]:
        total_steps = 0
        total_emptyspace = 0
        x_occupied = set([g.x for g in self.__galaxies])
        y_occupied = set([g.y for g in self.__galaxies])
        x_empty = [x for x in range(max(x_occupied)) if x not in x_occupied]
        y_empty = [y for y in range(max(y_occupied)) if y not in y_occupied]
        for g1, g2 in combinations(self.__galaxies, 2):
            x_range = g1.get_x_ranges(g2)
            y_range = g1.get_y_ranges(g2)
            total_emptyspace += (sum([1 for x in x_empty if x_range[0] < x < x_range[1]]) +
                                 sum([1 for y in y_empty if y_range[0] < y < y_range[1]]))
            total_steps += g1.get_manhattan(g2)
        # Note: -1 on the expansion rates since those tiles are already counted once in normal steps
        return (total_steps + total_emptyspace * (Space.__SMALL_EXPANSION_RATE - 1),
                total_steps + total_emptyspace * (Space.__LARGE_EXPANSION_RATE - 1))


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        space = Space(file.read().strip('\n'))
    p1, p2 = space.get_distance_sum()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
