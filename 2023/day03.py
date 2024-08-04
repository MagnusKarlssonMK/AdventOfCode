"""
Store the symbols in a dict with the type stored for each symbol, and then a dict for all parts which stores a list
of adjacent symbols for each part.
Then for part 1, simply iterate over the parts and get the sum of the values for the parts that have at least one
symbol in its adjacent list.
For part 2, instead iterate over the symbols and find the gears, and then iterate over the parts to see how many parts
that are adjacent for each gear.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day03.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Part:
    point: Point
    length: int
    value: int

    def get_adjacent_points(self) -> iter:
        for y in range(self.point.y - 1, self.point.y + 2):
            for x in range(self.point.x - 1, self.point.x + self.length + 1):
                yield Point(x, y)


class Schematic:
    def __init__(self, rawstr: str) -> None:
        self.__parts: dict[Part: set[Point]] = {}
        self.__symbols: dict[Point: str] = {}
        for y, row in enumerate(rawstr.splitlines()):
            nbrs = re.finditer(r"(\d+)", row)
            symbs = re.finditer(r"[^.\d]", row)
            for nbr in nbrs:
                self.__parts[Part(Point(nbr.start(), y),
                                  nbr.end() - nbr.start(),
                                  int(row[nbr.start():nbr.end()]))] = set()
            for symb in symbs:
                self.__symbols[Point(symb.start(), y)] = row[symb.start()]
        # Connect symbols to parts
        for part in self.__parts:
            for adj in part.get_adjacent_points():
                if adj in self.__symbols:
                    self.__parts[part].add(adj)

    def get_partnumber_sum(self) -> int:
        return sum([part.value for part in self.__parts if len(self.__parts[part]) > 0])

    def get_gearratio_sum(self) -> int:
        result = 0
        for symbol, symbtype in self.__symbols.items():
            if symbtype == "*":
                adj_parts = [part.value for part in self.__parts if symbol in self.__parts[part]]
                if len(adj_parts) == 2:
                    result += adj_parts[0] * adj_parts[1]
        return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myschematic = Schematic(file.read().strip('\n'))
    print(f"Part 1: {myschematic.get_partnumber_sum()}")
    print(f"Part 2: {myschematic.get_gearratio_sum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
