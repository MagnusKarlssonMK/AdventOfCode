"""
Straightforward, just go through the instructions and update the position according to the rules.
"""
import sys
from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    FORWARD = 'forward'


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Submarine:
    def __init__(self, rawstr: str) -> None:
        self.__instructions = [(Direction(left), int(right)) for left, right in
                               [line.split() for line in rawstr.splitlines()]]

    def get_move_result(self) -> int:
        position = Point(0, 0)
        for direction, value in self.__instructions:
            match direction:
                case Direction.UP:
                    position += Point(0, -value)
                case Direction.DOWN:
                    position += Point(0, value)
                case Direction.FORWARD:
                    position += Point(value, 0)
        return position.x * position.y

    def get_aimed_move_result(self) -> int:
        position = Point(0, 0)
        aim = 0
        for direction, value in self.__instructions:
            match direction:
                case Direction.UP:
                    aim -= value
                case Direction.DOWN:
                    aim += value
                case Direction.FORWARD:
                    position += Point(value, aim * value)
        return position.x * position.y


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        submarine = Submarine(file.read().strip('\n'))
    print(f"Part 1: {submarine.get_move_result()}")
    print(f"Part 2: {submarine.get_aimed_move_result()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
