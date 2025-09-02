"""
2023 day 3 - Gear Ratios

Store the symbols in a dict with the type stored for each symbol, and then a dict for all parts which stores a list
of adjacent symbols for each part.
Then for part 1, simply iterate over the parts and get the sum of the values for the parts that have at least one
symbol in its adjacent list.
For part 2, instead iterate over the symbols and find the gears, and then iterate over the parts to see how many parts
that are adjacent for each gear.
"""

import time
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Part:
    point: Point
    length: int
    value: int

    def get_adjacent_points(self) -> Generator[Point]:
        for y in range(self.point.y - 1, self.point.y + 2):
            for x in range(self.point.x - 1, self.point.x + self.length + 1):
                yield Point(x, y)


class InputData:
    def __init__(self, s: str) -> None:
        self.__parts: dict[Part, set[Point]] = {}
        self.__symbols: dict[Point, str] = {}
        number = 0
        parts: set[Part] = set()
        numberpoint = Point(0, 0)
        for y, row in enumerate(s.splitlines()):
            for x, c in enumerate(row):
                if c.isdecimal():
                    if number == 0:
                        numberpoint = Point(x, y)
                    number = 10 * number + int(c)
                else:
                    if number > 0:
                        parts.add(Part(numberpoint, x - numberpoint.x, number))
                        number = 0
                    if c != ".":
                        self.__symbols[Point(x, y)] = c
            if number > 0:
                parts.add(Part(numberpoint, len(row) - numberpoint.x, number))
                number = 0

        # Connect symbols to parts
        for part in parts:
            adj: set[Point] = set()
            for p in part.get_adjacent_points():
                if p in self.__symbols:
                    adj.add(p)
            self.__parts[part] = adj

    def solve_part1(self) -> int:
        return sum([part.value for part in self.__parts if len(self.__parts[part]) > 0])

    def solve_part2(self) -> int:
        result = 0
        for symbol, symbtype in self.__symbols.items():
            if symbtype == "*":
                adj_parts = [
                    part.value for part in self.__parts if symbol in self.__parts[part]
                ]
                if len(adj_parts) == 2:
                    result += adj_parts[0] * adj_parts[1]
        return result


def main(aoc_input: str) -> None:
    myschematic = InputData(aoc_input)
    print(f"Part 1: {myschematic.solve_part1()}")
    print(f"Part 2: {myschematic.solve_part2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2023/day03.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
