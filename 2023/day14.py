"""
"""
import time
from pathlib import Path
from dataclasses import dataclass


# I really want to move Point and Grid to utility packages, but not exactly
# best friends with the python import system...
@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rotate_left(self) -> "Point":
        return Point(self.y, -self.x)

    def rotate_right(self) -> "Point":
        return Point(-self.y, self.x)

    def manhattan(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def determinant(self, other: "Point") -> int:
        return (self.x * other.y) - (self.y * other.x)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, m: int) -> "Point":
        return Point(self.x * m, self.y * m)


ORIGIN = Point(0, 0)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
UP = Point(0, -1)
DOWN = Point(0, 1)

DIAG_R_D = Point(1, 1)
DIAG_L_D = Point(-1, 1)
DIAG_L_U = Point(-1, -1)
DIAG_R_U = Point(1, -1)

NEIGHBORS_STRAIGHT = [RIGHT, DOWN, LEFT, UP]
NEIGHBORS_ALL = [RIGHT, DIAG_R_D, DOWN, DIAG_L_D, LEFT, DIAG_L_U, UP, DIAG_R_U]


class Grid:
    def __init__(self, s: str):
        '''Creates a new Grid object based on the string input.
        Assumes that the input is in valid format.'''
        lines = s.splitlines()
        self.x_max: int = len(lines[0])
        self.y_max: int = len(lines)
        self.elements: list[str] = [c for c in s if c != "\n"]

    def get_element(self, p: Point) -> str:
        '''Returns the element in a certain point in the grid.
        If the input point is out-of-bounds, an empty string is returned.'''
        if 0 <= p.x < self.x_max and 0 <= p.y < self.y_max:
            return self.elements[(self.x_max * p.y) + p.x]
        else:
            return ""

    def find(self, item: str) -> Point:
        '''Searches the Grid for an element matching item. The first one found
        will be returned as a Point, searching top left to the right and then down.
        If no match is found, (-1, -1) is returned.'''
        for i, e in enumerate(self.elements):
            if e == item:
                return Point(i % self.x_max, i // self.x_max)
        return Point(-1, -1)

    def get_index(self, p: Point) -> int:
        '''Returns the Point corresponding to an index in the Grid element array.
        Will return -1 if the input is out-of-bounds.'''
        if 0 <= p.x < self.x_max and 0 <= p.y < self.y_max:
            return self.x_max * p.y + p.x
        else:
            return -1

    def set_point(self, p: Point, v: str):
        '''Sets the Point p to the value v. Will do nothing if p is out-of-bounds.'''
        if 0 <= p.x < self.x_max and 0 <= p.y < self.y_max:
            self.elements[self.x_max * p.y + p.x] = v


class ReflectorDish:
    def __init__(self, rawinput: str):
        self.grid = Grid(rawinput)

    def tilt_north(self):
        for x in range(0, self.grid.x_max):
            floor = 0
            for y in range(0, self.grid.y_max):
                current_point = Point(x, y)
                e = self.grid.get_element(current_point)
                if e == "#":
                    floor = y + 1
                elif e == "O":
                    if y > floor:
                        self.grid.set_point(Point(x, floor), "O")
                        self.grid.set_point(current_point, ".")
                    floor += 1

    def tilt_south(self):
        for x in range(0, self.grid.x_max):
            floor = self.grid.y_max - 1
            for y in reversed(range(0, self.grid.y_max)):
                current_point = Point(x, y)
                e = self.grid.get_element(current_point)
                if e == "#":
                    floor = y - 1
                elif e == "O":
                    if y < floor:
                        self.grid.set_point(Point(x, floor), "O")
                        self.grid.set_point(current_point, ".")
                    floor -= 1

    def tilt_east(self):
        for y in range(0, self.grid.y_max):
            floor = self.grid.x_max - 1
            for x in reversed(range(0, self.grid.x_max)):
                current_point = Point(x, y)
                e = self.grid.get_element(current_point)
                if e == "#":
                    floor = x - 1
                elif e == "O":
                    if x < floor:
                        self.grid.set_point(Point(floor, y), "O")
                        self.grid.set_point(current_point, ".")
                    floor -= 1

    def tilt_west(self):
        for y in range(0, self.grid.y_max):
            floor = 0
            for x in range(0, self.grid.x_max):
                current_point = Point(x, y)
                e = self.grid.get_element(current_point)
                if e == "#":
                    floor = x + 1
                elif e == "O":
                    if x > floor:
                        self.grid.set_point(Point(floor, y), "O")
                        self.grid.set_point(current_point, ".")
                    floor += 1

    def cycle(self):
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def get_load(self):
        return sum([self.grid.y_max - (i // self.grid.x_max) for i, e in enumerate(self.grid.elements) if e == "O"])

    def get_part_1(self) -> int:
        self.tilt_north()
        return self.get_load()

    def get_part_2(self) -> int:
        target_cycles = 1_000_000_000
        seen: dict[str, int] = {}
        loads: list[int] = []

        for cycle in range(0, target_cycles):
            self.cycle()
            loads.append(self.get_load())
            k = str(self.grid.elements)
            if k in seen:
                previous = seen[k]
                idx = previous + ((target_cycles - 1 - previous) % (cycle - previous))
                return loads[idx]
            else:
                seen[k] = cycle
        return 0


def main(aoc_input: str) -> None:
    dish = ReflectorDish(aoc_input)
    p1 = dish.get_part_1()
    print(f"Part 1: {p1}")

    p2 = dish.get_part_2()
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day14.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
