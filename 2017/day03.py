"""
Part 1: This can be solved algebraicly, since the lower right corner is n^2 with n=1,3,5,7... In other words, given a
certain number, we can use this to calculate the corners for the value of 'n' that will contain this number, and from
there figure out the manhattan distance from the center. However, this is somewhat cumbersome, and doesn't carry over
at all for part 2, so instead I'll just stick with simply 'drawing' the spiral to find the answer. The input number
is still low enough that this is a somewhat reasonable approach (runs in about a second).

Part 2: Pretty much the same thing, just with a small modification for how to keep track of the current number while
building the spiral.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Head:
    def __init__(self) -> None:
        self.__pos = Point(0, 0)
        self.__direction = Point(1, 0)

    def get_pos(self) -> Point:
        return self.__pos

    def get_manhattan(self) -> int:
        return abs(self.__pos.x) + abs(self.__pos.y)

    def get_left(self) -> Point:
        return Point(self.__pos.x + self.__direction.y, self.__pos.y - self.__direction.x)

    def step(self, turn_left: bool = False) -> None:
        if turn_left:
            self.__direction = Point(self.__direction.y, -self.__direction.x)
        self.__pos += self.__direction

    def get_neighbors(self) -> iter:
        for n in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
            yield self.__pos + Point(*n)


class Memory:
    def __init__(self, rawstr: str) -> None:
        self.__nbr = int(rawstr)

    def get_manhattan_distance(self) -> int:
        head = Head()
        points: set[Point] = {head.get_pos()}
        head.step()
        i = 2
        points.add(head.get_pos())
        while i < self.__nbr:
            head.step(head.get_left() not in points)
            i += 1
            points.add(head.get_pos())
        return head.get_manhattan()

    def get_larger_number(self) -> int:
        head = Head()
        points: dict[Point: int] = {head.get_pos(): 1}
        head.step()
        points[head.get_pos()] = i = 1
        while i <= self.__nbr:
            head.step(head.get_left() not in points)
            i = 0
            for n in head.get_neighbors():
                if n in points:
                    i += points[n]
            points[head.get_pos()] = i
        return i


def main(aoc_input: str) -> None:
    memory = Memory(aoc_input)
    print(f"Part 1: {memory.get_manhattan_distance()}")
    print(f"Part 2: {memory.get_larger_number()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
