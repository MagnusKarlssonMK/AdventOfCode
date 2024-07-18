"""

"""
import sys
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class TileType(Enum):
    OPEN = 0
    KEY = 1
    DOOR = 2


@dataclass
class Tile:
    type: TileType
    value: str
    neighbors: set[Point]


class Vault:
    def __init__(self, rawstr: str) -> None:
        self.__tiles: dict[Point: Tile] = {}
        self.__start: Point = Point(-1, -1)
        self.__nbr_keys = 0
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    continue
                elif c == ".":
                    self.__tiles[Point(x, y)] = Tile(TileType.OPEN, '', set())
                elif c == "@":
                    self.__tiles[Point(x, y)] = Tile(TileType.OPEN, '', set())
                    self.__start = Point(x, y)
                elif c.islower():
                    self.__tiles[Point(x, y)] = Tile(TileType.KEY, c, set())
                    self.__nbr_keys += 1
                elif c.isupper():
                    self.__tiles[Point(x, y)] = Tile(TileType.DOOR, c, set())
        for point in self.__tiles:
            for n in (Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)):
                if (newpoint := point + n) in self.__tiles:
                    self.__tiles[point].neighbors.add(newpoint)

    def get_shortest_key_steps(self) -> int:
        seen: set[tuple[Point, tuple[str]]] = set()
        queue = [(self.__start, '', Point(-1, -1), 0)]
        while queue:
            current, keys, previous, steps = queue.pop(0)
            keyfound = False
            if self.__tiles[current].type == TileType.KEY and self.__tiles[current].value not in keys:
                keys += self.__tiles[current].value
                if len(keys) == self.__nbr_keys:
                    return steps
                keyfound = True
                keys = ''.join(sorted(keys))
            if (current, keys) in seen:
                continue
            seen.add((current, keys))
            for n in self.__tiles[current].neighbors:
                if ((self.__tiles[n].type != TileType.DOOR or self.__tiles[n].value.lower() in keys) and
                        (n != previous or keyfound)):
                    queue.append((n, keys, current, steps + 1))
        return -1


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        vault = Vault(file.read().strip('\n'))
    print(f"Part 1: {vault.get_shortest_key_steps()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
