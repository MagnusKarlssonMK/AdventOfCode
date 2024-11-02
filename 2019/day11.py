"""
Mostly straightforward just figuring out how to use the computer.
A bit unclear from the description for part 1 whether it counts as painting a tile if the output color is the same as
input, but it seems like it should be counted.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from intcode import Intcode, IntResult


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def turn(self, turnval: int) -> "Point":
        if turnval == 1:  # 0=left, 1=right
            return Point(-self.y, self.x)
        else:
            return Point(self.y, -self.x)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class PaintingRobot:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))
        self.__position = Point(0, 0)
        self.__direction = Point(0, -1)

    def __reset(self) -> None:
        self.__cpu.reboot()
        self.__position = Point(0, 0)
        self.__direction = Point(0, -1)

    def __paint(self, startcolor: int = 0) -> dict[Point: int]:
        painted: dict[Point: int] = {}  # point: color; 0=black, 1=white
        color = startcolor
        while True:
            self.__cpu.add_input(color)
            color, _ = self.__cpu.run_program()
            val, res = self.__cpu.run_program()
            if res == IntResult.OUTPUT:
                painted[self.__position] = color
                self.__direction = self.__direction.turn(val)
                self.__position += self.__direction
                color = 0 if self.__position not in painted else painted[self.__position]
            else:
                break
        self.__reset()
        return painted

    def get_painted_panels_count(self) -> int:
        painted = self.__paint()
        return len(painted)

    def get_registration_id(self) -> str:
        painted: dict[Point: int] = self.__paint(1)
        x_max = max(list(painted.keys()), key=lambda x: x.x).x + 1
        y_max = max(list(painted.keys()), key=lambda x: x.y).y + 1
        grid = [[' ' for _ in range(x_max)] for _ in range(y_max)]
        for p, c in painted.items():
            grid[p.y][p.x] = '#' if c == 1 else ' '
        result = '\n'
        for row in grid:
            result += ''.join(row)
            result += '\n'
        return result


def main(aoc_input: str) -> None:
    robot = PaintingRobot(aoc_input)
    print(f"Part 1: {robot.get_painted_panels_count()}")
    print(f"Part 2: {robot.get_registration_id()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
