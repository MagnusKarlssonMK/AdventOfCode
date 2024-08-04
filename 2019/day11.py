"""
Intcode returns... might be time to move it to a separate file instead so that it can be imported rather than copied.
Mostly straightforward just figuring out how to use the computer.
A bit unclear from the description for part 1 hether it counts as painting a tile if the output color is the same as
input, but it seems like it should be counted.
"""
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day11.txt')


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    RELATIVE_BASE = 9
    HALT = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


class Intcode:
    def __init__(self, rawstr: str) -> None:
        self.__program = [int(nbr) for nbr in rawstr.split(',')]
        self.__inputbuffer = []
        self.__head = 0
        self.__relative = 0
        self.__memory: dict[int: int] = {i: nbr for i, nbr in enumerate(self.__program)}

    def reboot(self) -> None:
        self.__inputbuffer = []
        self.__head = 0
        self.__relative = 0
        self.__memory = {i: nbr for i, nbr in enumerate(self.__program)}

    def add_input(self, value: int) -> None:
        self.__inputbuffer.append(value)

    def run_program(self) -> tuple[int, bool]:
        def __read(position: int) -> int:
            if position in self.__memory:
                return self.__memory[position]
            return 0

        def __write(position: int, value: int) -> None:
            self.__memory[position] = value

        def __get_value(m: Mode, param: int) -> int:
            if m == Mode.POSITION:
                return __read(param)
            elif m == Mode.IMMEDIATE:
                return param
            elif m == Mode.RELATIVE:
                return __read(self.__relative + param)
            return -1

        while 0 <= self.__head:
            op = __read(self.__head)
            modes = [0, 0, 0]
            modes[2] = Mode(op // 10000)
            op %= 10000
            modes[1] = Mode(op // 1000)
            op %= 1000
            modes[0] = Mode(op // 100)
            op_code = OpCode(op % 100)
            p = [__read(i) for i in range(self.__head + 1, self.__head + 4)]
            match op_code:
                case OpCode.ADD:
                    dest = p[2] if modes[2] != Mode.RELATIVE else self.__relative + p[2]
                    __write(dest, __get_value(modes[0], p[0]) + __get_value(modes[1], p[1]))
                    self.__head += 4
                case OpCode.MULTIPLY:
                    dest = p[2] if modes[2] != Mode.RELATIVE else self.__relative + p[2]
                    __write(dest, __get_value(modes[0], p[0]) * __get_value(modes[1], p[1]))
                    self.__head += 4
                case OpCode.INPUT:
                    dest = p[0] if modes[0] != Mode.RELATIVE else self.__relative + p[0]
                    if self.__inputbuffer:
                        __write(dest, self.__inputbuffer.pop(0))
                        self.__head += 2
                    else:
                        print("Input buffer empty")
                        return -1, True
                case OpCode.OUTPUT:
                    self.__head += 2
                    return __get_value(modes[0], p[0]), False
                case OpCode.JUMP_IF_TRUE:
                    if __get_value(modes[0], p[0]) != 0:
                        self.__head = __get_value(modes[1], p[1])
                    else:
                        self.__head += 3
                case OpCode.JUMP_IF_FALSE:
                    if not __get_value(modes[0], p[0]):
                        self.__head = __get_value(modes[1], p[1])
                    else:
                        self.__head += 3
                case OpCode.LESS_THAN:
                    dest = p[2] if modes[2] != Mode.RELATIVE else self.__relative + p[2]
                    __write(dest, 1 if __get_value(modes[0], p[0]) < __get_value(modes[1], p[1]) else 0)
                    self.__head += 4
                case OpCode.EQUALS:
                    dest = p[2] if modes[2] != Mode.RELATIVE else self.__relative + p[2]
                    __write(dest, 1 if __get_value(modes[0], p[0]) == __get_value(modes[1], p[1]) else 0)
                    self.__head += 4
                case OpCode.RELATIVE_BASE:
                    self.__relative += __get_value(modes[0], p[0])
                    self.__head += 2
                case OpCode.HALT:
                    break
        return -1, True


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
        self.__cpu = Intcode(rawstr)
        self.__position = Point(0, 0)
        self.__direction = Point(0, -1)

    def __reset(self) -> None:
        self.__cpu.reboot()
        self.__position = Point(0, 0)
        self.__direction = Point(0, -1)

    def __paint(self, startcolor: int = 0) -> dict[Point: int]:
        painted: dict[Point: int] = {}  # point: color; 0=black, 1=white
        color = startcolor
        done = False
        while not done:
            self.__cpu.add_input(color)
            color, _ = self.__cpu.run_program()
            direction, done = self.__cpu.run_program()
            if not done:
                painted[self.__position] = color
                self.__direction = self.__direction.turn(direction)
                self.__position += self.__direction
                color = 0 if self.__position not in painted else painted[self.__position]
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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        robot = PaintingRobot(file.read().strip('\n'))
    print(f"Part 1: {robot.get_painted_panels_count()}")
    print(f"Part 2: {robot.get_registration_id()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
