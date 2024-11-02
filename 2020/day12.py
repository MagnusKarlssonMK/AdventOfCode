"""
Use a point class to simplify coordinate handling, then it's mostly just a matter of going through the instructions
and moving the ship accordingly.
"""
import time
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class Action(Enum):
    LEFT = 'L'
    RIGHT = 'R'
    FORWARD = 'F'
    NORTH = 'N'
    SOUTH = 'S'
    WEST = 'W'
    EAST = 'E'


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rotate(self, d: Action) -> "Point":
        if d == Action.LEFT:
            return Point(self.y, -self.x)
        else:
            return Point(-self.y, self.x)

    def get_distance(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)


@dataclass(frozen=True)
class Instruction:
    action: Action
    value: int


class Ship:
    __DIRECTIONMAP = {Action.EAST: Point(1, 0), Action.SOUTH: Point(0, 1),
                      Action.WEST: Point(-1, 0), Action.NORTH: Point(0, -1)}

    def __init__(self, rawstr: str) -> None:
        self.__instructions = [Instruction(Action(line[0]), int(line[1:])) for line in rawstr.splitlines()]

    def get_distance(self, use_waypoint: bool = False) -> int:
        position = Point(0, 0)
        direction = Ship.__DIRECTIONMAP[Action.EAST] if not use_waypoint else Point(10, -1)
        for instr in self.__instructions:
            if instr.action in (Action.LEFT, Action.RIGHT):
                for nbr in range(instr.value // 90):
                    direction = direction.rotate(instr.action)
            elif instr.action in (Action.NORTH, Action.EAST, Action.SOUTH, Action.WEST):
                if not use_waypoint:
                    position += Ship.__DIRECTIONMAP[instr.action] * instr.value
                else:
                    direction += Ship.__DIRECTIONMAP[instr.action] * instr.value
            elif instr.action == Action.FORWARD:
                position += direction * instr.value
        return position.get_distance()


def main(aoc_input: str) -> None:
    myship = Ship(aoc_input)
    print(f"Part 1: {myship.get_distance()}")
    print(f"Part 2: {myship.get_distance(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
