"""
Taking an easy approach - simply storing the lines on a grid quite literally as in the example.
After experimenting with other approaches, such as dumping all points in sets and counting length, or comparing
all line combinations and storing only intersecting points in a set, this simple solution still seems to perform
best. The first alternative is noticably slower, and the second alternative is slightly faster but much more
complicated implementation and scales badly with increased number of lines.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Coord:
    x: int = 0
    y: int = 0

    def is_diagonal(self, other: "Coord") -> bool:
        return self.x != other.x and self.y != other.y

    def get_derivate(self, other: "Coord") -> "Coord":
        dx = (other.x - self.x) // max(abs(other.x - self.x), abs(other.y - self.y), 1)
        dy = (other.y - self.y) // max(abs(other.x - self.x), abs(other.y - self.y), 1)
        return Coord(dx, dy)

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.x + other.x, self.y + other.y)


class Line:
    max_x = 0
    max_y = 0

    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.__points = [Coord(x1, y1), Coord(x2, y2)] if x1 >= x2 else [Coord(x2, y2), Coord(x1, y1)]
        Line.max_x = max(Line.max_x, x1, x2)
        Line.max_y = max(Line.max_y, y1, y2)

    def is_diagonal(self) -> bool:
        return self.__points[0].is_diagonal(self.__points[1])

    def get_points(self) -> Generator[Coord]:
        dxdy = self.__points[0].get_derivate(self.__points[1])
        point = self.__points[0]
        while True:
            yield point
            if point == self.__points[1]:
                break
            point += dxdy


class Seabottom:
    def __init__(self, inputlines: str) -> None:
        self.__lines = [Line(*list(map(int, re.findall(r"\d+", line))))
                        for line in inputlines.splitlines()]
        self.__grid = [[0 for _ in range(Line.max_x + 1)] for _ in range(Line.max_y + 1)]

    def get_score(self, use_diagonal: bool = False) -> int:
        for line in self.__lines:
            if line.is_diagonal() == use_diagonal:
                for p in line.get_points():
                    self.__grid[p.y][p.x] += 1
        return sum([1 for y in self.__grid for x in y if x > 1])


def main(aoc_input: str) -> None:
    seabottom = Seabottom(aoc_input)
    print(f"Part 1: {seabottom.get_score()}")
    print(f"Part 2: {seabottom.get_score(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
