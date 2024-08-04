"""
This intcode program halts after each coordinate, so we need to keep rebooting it after every run.
"""
import sys
from pathlib import Path
from enum import Enum

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day19.txt')


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


class IntResult(Enum):
    WAIT_INPUT = 0
    OUTPUT = 1
    HALTED = 2


class Intcode:
    def __init__(self, program: list[int]) -> None:
        self.__program = list(program)
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

    def run_program(self) -> tuple[int, IntResult]:
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
                        return -1, IntResult.WAIT_INPUT
                case OpCode.OUTPUT:
                    self.__head += 2
                    return __get_value(modes[0], p[0]), IntResult.OUTPUT
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
        return -1, IntResult.HALTED


class TractorBeam:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def __get_drone_status(self, x: int, y: int) -> int:
        while True:
            self.__cpu.add_input(x)
            self.__cpu.add_input(y)
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                self.__cpu.reboot()
                return val
            else:
                break
        self.__cpu.reboot()
        return 0

    def get_nbr_affected_points(self) -> int:
        return sum([self.__get_drone_status(x, y) for x in range(50) for y in range(50)])

    def get_square_val(self) -> int:
        x = y = 0
        while not self.__get_drone_status(x + 99, y):
            y += 1
            while not self.__get_drone_status(x, y + 99):
                x += 1
        return x * 10000 + y


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        tractorbeam = TractorBeam(file.read().strip())
    print(f"Part 1: {tractorbeam.get_nbr_affected_points()}")
    print(f"Part 2: {tractorbeam.get_square_val()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
