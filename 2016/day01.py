"""
Create a Point class to represent current position and then:
Part 1: Simply walk through all off the instructions and take the manhattan distance of the point we end up in.
Part 2: Store the visited points in a set and stop when landing on a point that is already in that set and return the
manhattan distance of that point. Note that unlike part 1, this means that we need to walk every single point one step
at a time, and not directly jump the number of steps in the instruction in one giant step.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto


class Rotation(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass(frozen=True)
class Point:
    x: int = 0
    y: int = 0

    def rotate(self, direction: Rotation) -> "Point":
        if direction == Rotation.LEFT:
            return Point(self.y, -self.x)
        else:
            return Point(-self.y, self.x)

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)


class WalkingSimulator:
    def __init__(self, rawstr: str) -> None:
        self.__position = Point()
        self.__direction = Point(0, -1)
        self.__instructions = [(Rotation.LEFT if line[0] == 'L' else Rotation.RIGHT, int(line.strip(',')[1:]))
                               for line in rawstr.split()]

    def get_shortest_distance(self, findrepeat: bool = False) -> int:
        pos = self.__position
        d = self.__direction
        seen = set()
        for rotation, steps in self.__instructions:
            d = d.rotate(rotation)
            if findrepeat:
                for _ in range(steps):
                    pos += d
                    if pos in seen:
                        return pos.manhattan()
                    else:
                        seen.add(pos)
            else:
                pos += d * steps
        return pos.manhattan()


def main(aoc_input: str) -> None:
    sim = WalkingSimulator(aoc_input)
    print(f"Part 1: {sim.get_shortest_distance()}")
    print(f"Part 2: {sim.get_shortest_distance(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
