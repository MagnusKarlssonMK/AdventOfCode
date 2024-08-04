"""
Extension of the Intcode computer we started in day 2.
"""
import sys
from pathlib import Path
from enum import Enum

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day05.txt')


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    INPUT = 3
    OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END = 99


class Mode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class Intcode:
    def __init__(self, rawstr: str) -> None:
        self.__program = [int(nbr) for nbr in rawstr.split(',')]

    def __run_program(self, inp: list[int]) -> int:
        program: list[int] = list(self.__program)
        inputbuffer: list[int] = list(inp)
        outputbuffer: list[int] = []

        def __get_value(m: Mode, param: int) -> int:
            if m == Mode.POSITION:
                return program[param]
            elif m == Mode.IMMEDIATE:
                return param
            return -1

        head = 0
        while 0 <= head < len(program):
            op = program[head]
            modes = [0, 0, 0]
            modes[2] = Mode(op // 10000)
            op %= 10000
            modes[1] = Mode(op // 1000)
            op %= 1000
            modes[0] = Mode(op // 100)
            op_code = OpCode(op % 100)
            p = program[head + 1: head + 4]
            match op_code:
                case OpCode.ADD:
                    program[p[2]] = __get_value(modes[0], p[0]) + __get_value(modes[1], p[1])
                    head += 4
                case OpCode.MULTIPLY:
                    program[p[2]] = __get_value(modes[0], p[0]) * __get_value(modes[1], p[1])
                    head += 4
                case OpCode.INPUT:
                    if inputbuffer:
                        program[p[0]] = inputbuffer.pop(0)
                        head += 2
                    else:
                        print("Input buffer empty")
                        break
                case OpCode.OUTPUT:
                    outputbuffer.append(__get_value(modes[0], p[0]))
                    head += 2
                case OpCode.JUMP_IF_TRUE:
                    if __get_value(modes[0], p[0]) != 0:
                        head = __get_value(modes[1], p[1])
                    else:
                        head += 3
                case OpCode.JUMP_IF_FALSE:
                    if not __get_value(modes[0], p[0]):
                        head = __get_value(modes[1], p[1])
                    else:
                        head += 3
                case OpCode.LESS_THAN:
                    program[p[2]] = 1 if __get_value(modes[0], p[0]) < __get_value(modes[1], p[1]) else 0
                    head += 4
                case OpCode.EQUALS:
                    program[p[2]] = 1 if __get_value(modes[0], p[0]) == __get_value(modes[1], p[1]) else 0
                    head += 4
                case OpCode.END:
                    break
        return outputbuffer[-1]

    def get_diagnostic_code(self, inputval: int) -> int:
        return self.__run_program([inputval])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        computer = Intcode(file.read().strip('\n'))
    print(f"Part 1: {computer.get_diagnostic_code(1)}")
    print(f"Part 2: {computer.get_diagnostic_code(5)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
