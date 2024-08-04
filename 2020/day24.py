"""
Similar to the hexgrid problem in 2017 day 11, but using pointy top hex tiles rather than flat top.

Stores the hexgrid using axial coordinate system, i.e. based on 3d system (q, r, s) but with the third dimension
truncated, since the sum of all three must be zero, meaning that it can be calculated when necessary.

Parse each line of instructions into a list of directions, which can then be used to move a point starting from the
reference point (0, 0), and then flip the destination tile, i.e. add to list of black tiles if not there already,
otherwise remove it.

For part 2, it's simply game of life again. For each round, check the neighbors of all black tiles and determine
whether to flip it to white, and also store any white neigbors and check them afterward to see which ones to flip to
black.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day24.txt')


STR_TO_POINT = {'ne': (1, -1), 'e': (1, 0), 'se': (0, 1), 'sw': (-1, 1), 'w': (-1, 0), 'nw': (0, -1)}


@dataclass(frozen=True)
class HexPoint:
    """Represents hex coordinates in axial form, using pointy top hex tiles."""
    q: int = 0
    r: int = 0

    def get_neighbors(self) -> iter:
        for dq, dr in STR_TO_POINT.values():
            yield HexPoint(self.q + dq, self.r + dr)

    def move(self, direction: str) -> "HexPoint":
        return self + HexPoint(*STR_TO_POINT[direction])

    def __add__(self, other: "HexPoint") -> "HexPoint":
        return HexPoint(self.q + other.q, self.r + other.r)


class Hexgrid:
    def __init__(self, rawstr: str) -> None:
        self.__move_instr: list[list[str]] = []
        for line in rawstr.splitlines():
            self.__move_instr.append([])
            i = 0
            while i < len(line):
                if line[i] in STR_TO_POINT:
                    self.__move_instr[-1].append(line[i])
                    i += 1
                else:
                    self.__move_instr[-1].append(line[i: i + 2])
                    i += 2
        self.__black_tiles: set[HexPoint] = set()

    def get_nbr_black_tiles(self) -> int:
        for instr in self.__move_instr:
            tile = HexPoint()
            for move in instr:
                tile = tile.move(move)
            if tile in self.__black_tiles:
                self.__black_tiles.remove(tile)
            else:
                self.__black_tiles.add(tile)
        return len(self.__black_tiles)

    def flip_and_get_nbr_black_tiles(self, days: int = 100) -> int:
        for _ in range(days):
            black_tiles = set()
            white_neighbors = set()
            for tile in self.__black_tiles:
                b = 0
                for n in tile.get_neighbors():
                    if n in self.__black_tiles:
                        b += 1
                    else:
                        white_neighbors.add(n)
                if 1 <= b <= 2:
                    black_tiles.add(tile)
            for tile in white_neighbors:
                if sum([1 for n in tile.get_neighbors() if n in self.__black_tiles]) == 2:
                    black_tiles.add(tile)
            self.__black_tiles = black_tiles
        return len(self.__black_tiles)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        hexgrid = Hexgrid(file.read().strip('\n'))
    print(f"Part 1: {hexgrid.get_nbr_black_tiles()}")
    print(f"Part 2: {hexgrid.flip_and_get_nbr_black_tiles()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
