"""
For part 1, we can find all intersections by putting all coordinates in sets for each wire, and then find the common
points. Then the answer is given by the smallest manhattan distance from origin to intersection.
For Part 2, we can get the distances by finding the index of each intersection's coordinate in the wire lists.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Wireline:
    length: int
    direction: Point


class FuelSystem:
    __DIRMAP = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}

    def __init__(self, rawstr: str) -> None:
        self.__wires = [[Wireline(int(step[1:]), Point(*FuelSystem.__DIRMAP[step[0]])) for step in line.split(',')]
                        for line in rawstr.splitlines()]
        self.__points = [[p for p in self.__get_coordinates(i)] for i, _ in enumerate(self.__wires)]
        self.__intersections: set[Point] = set(self.__points[0]) & set(self.__points[1])

    def __get_coordinates(self, idx: int) -> iter:
        current = Point(0, 0)
        for w in self.__wires[idx]:
            for _ in range(w.length):
                current += w.direction
                yield current

    def get_closest_intersection_mh(self) -> int:
        return min([i.get_distance(Point(0, 0)) for i in self.__intersections if i != Point(0, 0)])

    def get_closest_intersection_steps(self) -> int:
        return min([sum([1 + self.__points[w].index(i) for w, _ in enumerate(self.__wires)])
                    for i in self.__intersections])


def main(aoc_input: str) -> None:
    system = FuelSystem(aoc_input)
    print(f"Part 1: {system.get_closest_intersection_mh()}")
    print(f"Part 2: {system.get_closest_intersection_steps()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
