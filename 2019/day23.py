"""

"""
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day23.txt')


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


@dataclass
class Computer:
    cpu: Intcode
    output_buffer: list[int]
    input_buffer: list[tuple[int, int]]


class Network:
    def __init__(self, rawstr: str) -> None:
        nic = list(map(int, rawstr.split(',')))
        self.__computers = {i: Computer(Intcode(nic), [], []) for i in range(50)}

    def get_first_packets_y_value(self) -> tuple[int, int]:
        [self.__computers[i].cpu.add_input(i) for i, _ in enumerate(self.__computers)]
        i = -1
        p1 = p2 = None
        nat = None
        nat_previous_y = -1
        network_idle = True
        while not p1 or not p2:
            i = (i + 1) % len(self.__computers)
            if i == 0:
                if network_idle and nat:
                    x = nat.pop(0)
                    y = nat.pop(0)
                    self.__computers[0].cpu.add_input(x)
                    self.__computers[0].cpu.add_input(y)
                    network_idle = False
                    if y == nat_previous_y:
                        p2 = y
                        break
                    else:
                        nat_previous_y = y
                else:
                    network_idle = True
            while True:
                val, res = self.__computers[i].cpu.run_program()
                if res == IntResult.OUTPUT:
                    self.__computers[i].output_buffer.append(val)
                    if len(self.__computers[i].output_buffer) == 3:
                        dest = self.__computers[i].output_buffer.pop(0)
                        x = self.__computers[i].output_buffer.pop(0)
                        y = self.__computers[i].output_buffer.pop(0)
                        if dest == 255:
                            if not p1:
                                p1 = y
                            nat = [x, y]
                        else:
                            self.__computers[dest].input_buffer.append((x, y))
                            network_idle = False
                elif res == IntResult.WAIT_INPUT:
                    if self.__computers[i].input_buffer:
                        x, y = self.__computers[i].input_buffer.pop(0)
                        self.__computers[i].cpu.add_input(x)
                        self.__computers[i].cpu.add_input(y)
                        network_idle = False
                    else:
                        self.__computers[i].cpu.add_input(-1)
                    break
                else:
                    print("halted", i)
                    break
        return p1, p2


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        net = Network(file.read().strip('\n'))
    p1, p2 = net.get_first_packets_y_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
