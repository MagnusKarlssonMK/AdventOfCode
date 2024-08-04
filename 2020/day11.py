"""
Pre-calculate the neighbor seats in all directions for every seat, which is done differently for Part 1 vs Part 2. This
does most of the heavy lifting, so after that just keep playing rounds until the occupied seats no longer changes.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day11.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x if self.x != other.x else self.y < other.y


class WaitingArea:
    __DIRECTIONS = (Point(-1, -1), Point(0, -1), Point(1, -1), Point(-1, 0),
                    Point(1, 0), Point(-1, 1), Point(0, 1), Point(1, 1))

    def __init__(self, rawstr: str) -> None:
        self.__seats_adj: dict[Point: set[Point]] = {}
        self.__seats_first: dict[Point: set[Point]] = {}
        xmax = ymax = 0
        for y, line in enumerate(rawstr.splitlines()):
            ymax = max(y, ymax)
            for x, c in enumerate(line):
                xmax = max(x, xmax)
                if c == 'L':
                    self.__seats_adj[Point(x, y)] = set()
                    self.__seats_first[Point(x, y)] = set()
        for seat in self.__seats_adj:
            for d in WaitingArea.__DIRECTIONS:
                if (n := seat + d) in self.__seats_adj:
                    self.__seats_adj[seat].add(n)
        for seat in self.__seats_first:
            for d in WaitingArea.__DIRECTIONS:
                n = seat + d
                while 0 <= n.x <= xmax and 0 <= n.y <= ymax:
                    if n in self.__seats_first:
                        self.__seats_first[seat].add(n)
                        break
                    else:
                        n += d

    def get_steadystate_occupied(self, firstseat: bool = False) -> int:
        tolerance = 4 if not firstseat else 5
        occupied_chairs: set[Point] = set()
        neighborlist = self.__seats_adj if not firstseat else self.__seats_first
        while True:
            buffer: set[Point] = set()
            for chair, neighbors in neighborlist.items():
                taken = sum([1 for n in neighbors if n in occupied_chairs])
                if chair in occupied_chairs:
                    if taken < tolerance:
                        buffer.add(chair)
                else:
                    if taken == 0:
                        buffer.add(chair)
            if buffer == occupied_chairs:
                return len(buffer)
            occupied_chairs = buffer


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        area = WaitingArea(file.read().strip('\n'))
    print(f"Part 1: {area.get_steadystate_occupied()}")
    print(f"Part 2: {area.get_steadystate_occupied(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
