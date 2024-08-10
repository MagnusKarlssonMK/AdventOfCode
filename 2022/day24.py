"""
To avoid having to continuously update the list of blizzards, instead store the blizzards in a per-direction dict,
and calculate dynamically whether a certain point will be occupied by at least one blizzard at a certain minute.
Use A* to traverse the map and find the shortest path, using the manhattan distance to the target as heuristic. The
time spent is effectively a third dimension in the space, since the possible neighbors changes with time, so we need
to include both position and time as key for the visited nodes.
The map state is cyclic since the winds will eventually return to the start position (lcm of width, height), but the
cycle is longer than the time spent to traverse the map, so there isn't much of a benefit to optimize making use of the
cycle.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day24.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_steps(self) -> iter:
        for d in Direction:
            yield self + d.value
        yield self

    def manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x


class Direction(Enum):
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)
    UP = Point(0, -1)


class Valley:
    def __init__(self, rawstr: str) -> None:
        dirmap = {'>': Direction.RIGHT, '<': Direction.LEFT, '^': Direction.UP, 'v': Direction.DOWN}
        self.__startpoint = Point(-1, -1)
        self.__exitpoint = Point(-1, -1)
        self.__walls: set[Point] = set()
        self.__blizzards: dict[Direction: set[Point]] = {d: set() for d in Direction}
        lines = rawstr.splitlines()
        self.__width = len(lines[0]) - 2  # Don't include the walls
        self.__height = len(lines) - 2
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    self.__walls.add(Point(x, y))
                elif y == 0 and c == '.':
                    self.__startpoint = Point(x, y)
                elif y == self.__height + 1 and c == '.':
                    self.__exitpoint = Point(x, y)
                elif c in dirmap:
                    self.__blizzards[dirmap[c]].add(Point(x, y))

    def __is_occupied_at_step(self, point: Point, step: int) -> bool:
        if point == self.__startpoint or point == self.__exitpoint:
            return False
        for direction in self.__blizzards:
            start_x = 1 + (point.x - 1 - (step * direction.value.x)) % self.__width
            start_y = 1 + (point.y - 1 - (step * direction.value.y)) % self.__height
            if Point(start_x, start_y) in self.__blizzards[direction]:
                return True
        return False

    def __shortest_path(self, start: Point, end: Point, startstep: int = 0) -> int:
        queue = []
        heappush(queue, (0, start, startstep))
        seen = set()
        while queue:
            _, point, steps = heappop(queue)
            if point == end:
                return steps
            if (point, steps) in seen:
                continue
            seen.add((point, steps))
            for next_step in point.get_steps():
                if ((0 < next_step.y <= self.__height and 0 < next_step.x <= self.__width) or
                        next_step in (start, end)):
                    if not self.__is_occupied_at_step(next_step, steps + 1):
                        heappush(queue, (steps + 1 + next_step.manhattan(end), next_step, steps + 1))
        return -1

    def get_there_and_back_again(self) -> tuple[int, int]:
        a = self.__shortest_path(self.__startpoint, self.__exitpoint, 0)
        b = self.__shortest_path(self.__exitpoint, self.__startpoint, a)
        c = self.__shortest_path(self.__startpoint, self.__exitpoint, b)
        return a, c


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        valley = Valley(file.read().strip('\n'))
    p1, p2 = valley.get_there_and_back_again()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
