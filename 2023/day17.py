"""
Sort of a Dijkstra solution but with a bit more complicated state, since it also needs to track direction.
Certainly not fast, but gets the job done.
"""
import sys
from pathlib import Path
from heapq import heappop, heappush
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day17.txt')


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def rotate_ccw(self) -> "Coord":
        return Coord(-self.col, self.row)

    def rotate_cw(self) -> "Coord":
        return Coord(self.col, -self.row)

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.row + other.row, self.col + other.col)


@dataclass(frozen=True)
class State:
    pos: Coord
    direction: Coord
    steps: int

    def __lt__(self, other: "State"):
        return self.steps < other.steps


class CityBoard:
    def __init__(self, rawstr: str) -> None:
        self.__grid = [[int(c) for c in line] for line in rawstr.splitlines()]
        self.__width = len(self.__grid[0])
        self.__height = len(self.__grid)

    def __get_value(self, point: Coord) -> int:
        if (0 <= point.row < self.__height) and (0 <= point.col < self.__width):
            return self.__grid[point.row][point.col]
        return -1

    def get_shortestpath(self, minsteps: int = 0, maxsteps: int = 3) -> int:
        state = State(Coord(0, 0), Coord(0, 1), 0)
        target = Coord(self.__height - 1, self.__width - 1)
        visited = {}
        queue = []
        heappush(queue, (0, state))
        while queue:
            heat, state = heappop(queue)
            if state.pos == target and state.steps >= minsteps:
                return heat
            neighborstates: list[State] = []
            if state.steps >= minsteps:
                ccw = state.direction.rotate_ccw()
                neighborstates.append(State(state.pos + ccw, ccw, 1))
                cw = state.direction.rotate_cw()
                neighborstates.append(State(state.pos + cw, cw, 1))
            if state.steps < maxsteps:
                neighborstates.append(State(state.pos + state.direction, state.direction, state.steps + 1))
            for ns in neighborstates:
                if (newheat := self.__get_value(ns.pos)) < 0:
                    continue
                newheat += heat
                if ns not in visited or newheat < visited[ns]:
                    visited[ns] = newheat
                    heappush(queue, (newheat, ns))
        return -1


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        mycity = CityBoard(file.read().strip('\n'))
    print(f"Part 1: {mycity.get_shortestpath()}")
    print(f"Part 2: {mycity.get_shortestpath(4, 10)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
