"""
Game of life with three states instead of two, kind of.
Store the grid in a dict with the state for each coordinate and update according to the rules for each passing minute.
For part 2 we obviously don't want to brute force a trillion minutes, so instead try to find a cycle. The grid value
appears not to be unique enough for all inputs to use as hash for the seen states and look for repetitions based on
that, so instead generate a sorted tuple of the grid to use as key.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from collections import Counter


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

    def __lt__(self, other: "Point") -> bool:
        return self.y < other.y if self.y != other.y else self.x < other.x


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

    def __get_keyval(self):
        return tuple(sorted(self.__grid.items()))

    def get_total_resource_value(self) -> tuple[int, int]:
        p1 = p2 = 0
        time = 0
        seen = {}
        while True:
            time += 1
            self.__grid = self.__step_minute()
            value = self.__get_value()
            keyval = self.__get_keyval()
            if time == LumberArea.P1_TIME:
                p1 = value
            if keyval in seen:
                cycle = time - seen[keyval][0]
                offset = time - cycle
                p2_time = offset + ((LumberArea.P2_TIME - offset) % cycle)
                for v in seen:
                    if seen[v][0] == p2_time:
                        p2 = seen[v][1]
                        break
                break
            else:
                seen[keyval] = time, value
        return p1, p2


def main(aoc_input: str) -> None:
    area = LumberArea(aoc_input)
    p1, p2 = area.get_total_resource_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
