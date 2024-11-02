"""
Stores non-empty tiles in a dict with its current state (clay, resting, flowing). Then starting from the source at
point (500, 0), trail the water path with a DFS, falling down as far as possible, then checking left/right.
After the queue is exhausted, the answers can be found by counting the number of tiles in state 'resting'/'flowing'
for part 1, 'resting' for part 2.
"""
import time
from pathlib import Path
import re
from dataclasses import dataclass
from enum import Enum, auto


class Tile(Enum):
    CLAY = auto()
    RESTING = auto()
    FLOWING = auto


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_below(self) -> "Point":
        return self + Point(0, 1)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Ground:
    def __init__(self, rawstr: str) -> None:
        self.__tiles: dict[Point: Tile] = {}
        for line in rawstr.splitlines():
            a, b, c = list(map(int, re.findall(r"\d+", line)))
            for i in range(b, c + 1):
                x, y = (a, i) if line[0] == 'x' else (i, a)
                self.__tiles[Point(x, y)] = Tile.CLAY
        self.__y_min = min(p.y for p in self.__tiles)
        self.__y_max = max(p.y for p in self.__tiles)

    def get_water_tile_count(self) -> tuple[int, int]:
        queue = [Point(500, 0)]
        while queue:
            p = queue.pop()
            if p.y > self.__y_max:
                continue
            below = p.get_below()
            if below not in self.__tiles or self.__tiles[below] == Tile.FLOWING:
                self.__tiles[p] = Tile.FLOWING
                queue.append(below)
            else:
                # Check left
                p_left_x = p.x
                p_left = Point(p.x, p.y)
                p_left_below = p_left.get_below()
                while ((p_left not in self.__tiles or self.__tiles[p_left] == Tile.FLOWING) and
                       (p_left_below in self.__tiles and (self.__tiles[p_left_below] in (Tile.RESTING, Tile.CLAY)))):
                    self.__tiles[p_left] = Tile.FLOWING
                    p_left_x -= 1
                    p_left = Point(p_left_x, p_left.y)
                    p_left_below = p_left.get_below()
                # Check right
                p_right_x = p.x
                p_right = Point(p.x, p.y)
                p_right_below = p_right.get_below()
                while ((p_right not in self.__tiles or self.__tiles[p_right] == Tile.FLOWING) and
                       (p_right_below in self.__tiles and (self.__tiles[p_right_below] in (Tile.RESTING, Tile.CLAY)))):
                    self.__tiles[p_right] = Tile.FLOWING
                    p_right_x += 1
                    p_right = Point(p_right_x, p_right.y)
                    p_right_below = p_right.get_below()

                if (p_left in self.__tiles and self.__tiles[p_left] == Tile.CLAY and
                        p_right in self.__tiles and self.__tiles[p_right] == Tile.CLAY):  # If delimited on both sides
                    for x in range(p_left.x + 1, p_right.x):
                        self.__tiles[Point(x, p.y)] = Tile.RESTING
                    queue.append(Point(p.x, p.y - 1))
                else:
                    if p_left not in self.__tiles:  # Left side open...
                        queue.append(p_left)
                    if p_right not in self.__tiles:  # Right side open...
                        queue.append(p_right)
        p1 = sum([1 for t in self.__tiles if self.__tiles[t] in (Tile.RESTING, Tile.FLOWING)
                  and self.__y_min <= t.y <= self.__y_max])
        p2 = sum([1 for t in self.__tiles if self.__tiles[t] == Tile.RESTING and self.__y_min <= t.y <= self.__y_max])
        return p1, p2


def main(aoc_input: str) -> None:
    ground = Ground(aoc_input)
    p1, p2 = ground.get_water_tile_count()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
