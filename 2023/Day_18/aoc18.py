"""
Store the trench in a class as a list of dig steps, i.e. expands as we dig through it without using any static grid.
After the dig commands have been carried out, the results are calculated with shoelace formula and Pick's theorem.
For part 2, simply convert the instructions before running the command.
"""
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def scale(self, multiplier) -> "Point":
        return Point(self.x * multiplier, self.y * multiplier)

    def get_length(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def get_det(self, other: "Point") -> int:
        return (self.x * other.y) - (self.y * other.x)


@dataclass(frozen=True)
class DigPlan:
    direction: Point
    step: int
    color: str


class Trench:
    __DIRECTIONS = {'R': Point(1, 0), 'D': Point(0, 1), 'L': Point(-1, 0), 'U': Point(0, -1)}
    __DIRMAP = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

    def __init__(self, rawstr: str) -> None:
        self.__digplan: list[DigPlan] = []
        for line in rawstr.splitlines():
            d, s, c = line.split()
            c = c.strip('(').strip(')').strip('#')
            self.__digplan.append(DigPlan(Trench.__DIRECTIONS[d], int(s), c))
        self.__digpath: list[Point] = []

    def __dig(self, swapped: bool) -> None:
        self.__digpath = [Point(0, 0)]
        for planline in self.__digplan:
            if swapped:
                planline = DigPlan(Trench.__DIRECTIONS[Trench.__DIRMAP[int(planline.color[-1])]],
                                   int(planline.color[0:5], 16), planline.color)
            self.__digpath.append(self.__digpath[-1] + planline.direction.scale(planline.step))

    def __get_outlinelength(self) -> int:
        return sum([self.__digpath[idx].get_length(self.__digpath[(idx + 1) % len(self.__digpath)])
                    for idx, _ in enumerate(self.__digpath)])

    def get_areapoints(self, swapped: bool = False) -> int:
        self.__dig(swapped)
        areasum = sum([self.__digpath[idx].get_det(self.__digpath[(idx + 1) % len(self.__digpath)])
                       for idx, _ in enumerate(self.__digpath)])
        length = self.__get_outlinelength()
        return (abs(areasum) // 2) + 1 + (length // 2)


def main() -> int:
    with open('../Inputfiles/aoc18.txt', 'r') as file:
        mytrench = Trench(file.read().strip('\n'))
    print(f"Part 1: {mytrench.get_areapoints()}")
    print(f"Part 2: {mytrench.get_areapoints(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
