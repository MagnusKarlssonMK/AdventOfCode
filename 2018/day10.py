"""
Pretty much just store the points move them around a few times and then print the resulting image.
The key point is to know when to break, which will be when the points are the most concentrated, i.e. the area of the
box containing the points is the smallest.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    dx: int
    dy: int

    def step(self) -> "Point":
        return Point(self.x + self.dx, self.y + self.dy, self.dx, self.dy)


def get_box_area(points: list[Point]) -> int:
    max_x = max_y = 0
    min_x = min_y = 9999
    for p in points:
        max_x = max(max_x, p.x)
        min_x = min(min_x, p.x)
        max_y = max(max_y, p.y)
        min_y = min(min_y, p.y)
    return (max_x - min_x) * (max_y - min_y)


def print_grid(points: list[Point]) -> None:
    max_x = max_y = 0
    min_x = min_y = 9999
    for p in points:
        max_x = max(max_x, p.x)
        min_x = min(min_x, p.x)
        max_y = max(max_y, p.y)
        min_y = min(min_y, p.y)
    grid = [['.' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
    for i, r in enumerate(points):
        grid[r.y - min_y][r.x - min_x] = "#"
    [print(''.join(g)) for g in grid]


class SkyGrid:
    def __init__(self, rawstr: str) -> None:
        self.__rows = tuple([Point(*list(map(int, re.findall(r"-?\d+", line)))) for line in rawstr.splitlines()])

    def get_message(self) -> int:
        points = list(self.__rows)
        area = get_box_area(points)
        seconds = 0
        while True:
            newpoints = [points[i].step() for i, _ in enumerate(points)]
            newarea = get_box_area(newpoints)
            if newarea < area:
                area = newarea
                points = newpoints
                seconds += 1
            else:
                print_grid(points)
                break
        return seconds


def main(aoc_input: str) -> None:
    grid = SkyGrid(aoc_input)
    print(f"Part 1:")
    p2 = grid.get_message()
    print()
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
