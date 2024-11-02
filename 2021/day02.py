"""
Straightforward, just go through the instructions and update the position according to the rules.
"""
import time
from pathlib import Path
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


def main(aoc_input: str) -> None:
    submarine = Submarine(aoc_input)
    print(f"Part 1: {submarine.get_move_result()}")
    print(f"Part 2: {submarine.get_aimed_move_result()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day02.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
