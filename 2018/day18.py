"""
Game of life with three states instead of two, kind of.
Store the grid in a dict with the state for each coordinate and update according to the rules for each passing minute.
For part 2 we obviously don't want to brute force a trillion minutes, so instead try to find a cycle. The grid value
seems to be unique enough to hash the seen states and look for repetitions based on that, but require a found cycle to
be consistent over two consequtive minutes to be sure it's not just a coincidental match.
"""
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from collections import Counter

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day18.txt')


class State(Enum):
    OPEN = '.'
    TREES = '|'
    LUMBERYARD = '#'


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_surrounding(self) -> iter:
        for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            yield Point(self.x + dx, self.y + dy)


class LumberArea:
    P1_TIME = 10
    P2_TIME = 1_000_000_000

    def __init__(self, rawstr: str) -> None:
        self.__grid: dict[Point: State] = {}
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                self.__grid[Point(x, y)] = State(c)

    def __step_minute(self) -> dict[Point: State]:
        result = {}
        for point in self.__grid:
            surrounding = Counter([self.__grid[s] for s in point.get_surrounding() if s in self.__grid])
            newstate = self.__grid[point]
            match self.__grid[point]:
                case State.OPEN:
                    if surrounding[State.TREES] >= 3:
                        newstate = State.TREES
                case State.TREES:
                    if surrounding[State.LUMBERYARD] >= 3:
                        newstate = State.LUMBERYARD
                case State.LUMBERYARD:
                    if surrounding[State.LUMBERYARD] == 0 or surrounding[State.TREES] == 0:
                        newstate = State.OPEN
            result[point] = newstate
        return result

    def __get_value(self) -> int:
        nbrs = Counter(self.__grid.values())
        return nbrs[State.TREES] * nbrs[State.LUMBERYARD]

    def get_total_resource_value(self) -> tuple[int, int]:
        p1 = p2 = 0
        time = 0
        seen = {}
        previous_cycle = 0
        while True:
            time += 1
            self.__grid = self.__step_minute()
            value = self.__get_value()
            if time == LumberArea.P1_TIME:
                p1 = value
            if value in seen:
                cycle = time - seen[value]
                if cycle == previous_cycle:
                    offset = time - cycle
                    p2_time = offset + ((LumberArea.P2_TIME - offset) % cycle)
                    for v in seen:
                        if seen[v] == p2_time:
                            p2 = v
                            break
                    break
                else:
                    previous_cycle = cycle
            else:
                previous_cycle = 0
                seen[value] = time
        return p1, p2


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        area = LumberArea(file.read().strip('\n'))
    p1, p2 = area.get_total_resource_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
