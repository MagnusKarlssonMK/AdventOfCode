"""
Rather straighforward grid problem.
Create a Grid class to store the input, and add methods to find the low point coordinates and basin coordinates.
The latter uses a stripped down BFS to find any adjacent neighbor until value '9' is found. This assumes (as also
stated in the problem description) that all low points will be surrounded by 9:s and not connected to any other
low point.
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
    def __init__(self, rawstr: str) -> None:
        self.__grid = [list(map(int, line)) for line in rawstr.splitlines()]
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.__lowpoints = set(p for p in self.__find_low_points())

    def __find_low_points(self) -> Generator[Point]:
        for y, row in enumerate(self.__grid):
            for x, _ in enumerate(row):
                for n in Point(x, y).get_neighbors():
                    if (0 <= n.y < self.__height and 0 <= n.x < self.__width and
                            self.__grid[y][x] >= self.__grid[n.y][n.x]):
                        break
                else:
                    yield Point(x, y)

    def __find_basin_points(self, lowpoint: Point) -> set[Point]:
        seen: set[Point] = set()
        queue = [lowpoint]
        while queue:
            current = queue.pop(0)
            if current not in seen:
                seen.add(current)
                for n in current.get_neighbors():
                    if n not in seen and (0 <= n.y < self.__height and 0 <= n.x < self.__width and
                                          self.__grid[n.y][n.x] < 9):
                        queue.append(n)
        return seen

    def get_low_point_score(self) -> int:
        return sum([self.__grid[point.y][point.x] + 1 for point in self.__lowpoints])

    def get_basin_score(self) -> int:
        basin_sizelist = sorted([len(self.__find_basin_points(p)) for p in self.__lowpoints], reverse=True)
        return basin_sizelist[0] * basin_sizelist[1] * basin_sizelist[2]


def main(aoc_input: str) -> None:
    grid = Grid(aoc_input)
    print(f"Part 1: {grid.get_low_point_score()}")
    print(f"Part 2: {grid.get_basin_score()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
