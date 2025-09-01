"""
Multidimensional game of life. While checking neighbors of active cubes, collect a set of neiboring inactive cubes,
and then go through them to see which ones to activate.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def get_neighbours(self) -> Generator["Point"]:
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    if not (x == 0 and y == 0 and z == 0):
                        yield Point(self.x + x, self.y + y, self.z + z)


@dataclass(frozen=True)
class Point4d:
    x: int
    y: int
    z: int
    w: int

    def get_neighbours(self) -> Generator["Point4d"]:
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    for w in range(-1, 2):
                        if not (x == 0 and y == 0 and z == 0 and w == 0):
                            yield Point4d(self.x + x, self.y + y, self.z + z, self.w + w)


class ConwayCubes:
    def __init__(self, rawstr: str) -> None:
        self.__cubes: set[Point] = set()
        self.__cubes4d: set[Point4d] = set()
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                if c == '#':
                    self.__cubes.add(Point(x, y, 0))
                    self.__cubes4d.add(Point4d(x, y, 0, 0))

    def get_nbr_active_cubes(self, is4d: bool = False) -> int:
        if not is4d:
            cubes = self.__cubes
        else:
            cubes = self.__cubes4d
        for _ in range(6):
            empty = set()
            buffer = set()
            for cube in cubes:
                count = 0
                for n in cube.get_neighbours():
                    if n in cubes:
                        count += 1
                    else:
                        empty.add(n)
                if 2 <= count <= 3:
                    buffer.add(cube)
            for cube in empty:
                count = 0
                for n in cube.get_neighbours():
                    if n in cubes:
                        count += 1
                        if count > 3:
                            break
                if count == 3:
                    buffer.add(cube)
            cubes = buffer
        return len(cubes)


def main(aoc_input: str) -> None:
    cubes = ConwayCubes(aoc_input)
    print(f"Part 1: {cubes.get_nbr_active_cubes()}")
    print(f"Part 2: {cubes.get_nbr_active_cubes(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
