"""
Part 1: Stores the grid in a new class, and finds reachable tiles within the step count limit using BFS, then count
only the ones that have odd/even number of steps (depending on whether the count limit is odd/even).
Part 2: Solves it with three-point-formula to determine the coefficients in a quadratic formula, and calculate the
answer from that.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> Generator["Point"]:
        for d in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            yield self + Point(*d)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Grid:
    def __init__(self, rawstr: str):
        lines = rawstr.splitlines()
        self.__height = len(lines)
        self.__width = len(lines[0])
        self.__start = Point(-1, -1)
        self.__rocks: set[Point] = set()
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                if c == 'S':
                    self.__start = Point(x, y)
                elif c == '#':
                    self.__rocks.add(Point(x, y))

    def __get_neighbors(self, coord: Point, expand: bool) -> Generator[Point]:
        for neighbor in coord.get_neighbors():
            if expand:
                if Point(neighbor.x % self.__width, neighbor.y % self.__height) not in self.__rocks:
                    yield neighbor
            else:
                if Point(neighbor.x, neighbor.y) not in self.__rocks:
                    yield neighbor

    def get_reachablecount(self, steps: int, expand: bool = False) -> int:
        seen: set[Point] = set()
        reachable: set[Point] = set()
        bfs_queue = [(self.__start, 0)]
        while bfs_queue:
            u, count = bfs_queue.pop(0)
            if count <= steps:
                if count % 2 == steps % 2:
                    reachable.add(u)
                for v in self.__get_neighbors(u, expand):
                    if v not in seen:
                        bfs_queue.append((v, count + 1))
                        seen.add(v)
        return len(reachable)

    def get_reachablecount_infinite(self, maxstep: int) -> int:
        n = (self.__height - 1) // 2
        three_vec = [n + (self.__height * i) for i in range(3)]
        # y = a*x^2 + b*x + c
        y = [self.get_reachablecount(i, True) for i in three_vec]
        c = y[0]
        b = ((4 * y[1]) - (3 * y[0]) - y[2]) // 2
        a = y[1] - y[0] - b
        x = (maxstep - n) // self.__height
        return (a * x ** 2) + (b * x) + c


def main(aoc_input: str) -> None:
    mygrid = Grid(aoc_input)
    print(f"Part 1: {mygrid.get_reachablecount(64)}")
    print(f"Part 2: {mygrid.get_reachablecount_infinite(26501365)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day21.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
