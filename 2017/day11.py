"""
Stores the hexgrid using axial coordinate system, i.e. based on 3d system (q, r, s) but with the third dimension
truncated, since the sum of all three must be zero, meaning that it can be calculated when necessary.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2017/day11.txt')


class HexPoint:
    """Represents hex coordinates in axial form."""
    STR_TO_POINT = {'n': (0, -1), 'ne': (1, -1), 'se': (1, 0), 's': (0, 1), 'sw': (-1, 1), 'nw': (-1, 0)}

    def __init__(self, q: int = 0, r: int = 0) -> None:
        self.q: int = q
        self.r: int = r

    def get_neighbors(self) -> iter:
        for dq, dr in HexPoint.STR_TO_POINT.values():
            yield HexPoint(self.q + dq, self.r + dr)

    def move(self, direction: str) -> "HexPoint":
        return HexPoint(self.q + HexPoint.STR_TO_POINT[direction][0], self.r + HexPoint.STR_TO_POINT[direction][1])

    def get_distance(self, other: "HexPoint") -> int:
        s1 = -(self.q + self.r)
        s2 = -(other.q + other.r)
        return (abs(self.r - other.r) + abs(self.q - other.q) + abs(s1 - s2)) // 2

    def __add__(self, other: "HexPoint") -> "HexPoint":
        return HexPoint(self.q + other.q, self.r + other.r)


class Hexgrid:
    def __init__(self, rawstr: str) -> None:
        self.__move_instr = rawstr.split(',')

    def get_distance(self) -> tuple[int, int]:
        start_location = HexPoint()
        current_location = start_location
        current_distance = 0
        maxdistance = 0
        for instr in self.__move_instr:
            current_location = current_location.move(instr)
            current_distance = current_location.get_distance(start_location)
            maxdistance = max(maxdistance, current_distance)
        return current_distance, maxdistance


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        hexgrid = Hexgrid(file.read().strip('\n'))
    p1, p2 = hexgrid.get_distance()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
