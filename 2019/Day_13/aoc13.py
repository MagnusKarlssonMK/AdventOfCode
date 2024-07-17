"""
Part 1 is mostly just running the Intcode program without any input, storing the output in a dict and then count number
of blocks.
Part 2 is not clear at all from the problem description what the joystick actually controls or how to use it to beat
the game, but apparently all we need to do is to steer the x-position of the paddle towards the ball (so it's basically
sort of an Arkanoid game), e.g. if ball < paddle steer left.
"""
import sys
from enum import Enum
from dataclasses import dataclass


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

    def start_game(self) -> None:
        self.__memory[0] = 2


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class TileId(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    HORIZONTAL_PADDLE = 3
    BALL = 4


class Joystick(Enum):
    NEUTRAL = 0
    LEFT = -1
    RIGHT = 1


class ArcadeGame:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(rawstr)

    def get_block_tiles(self) -> int:
        tiles: dict[Point: TileId] = {}
        output_buffer = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                output_buffer.append(val)
                if len(output_buffer) == 3:
                    x, y, t = output_buffer
                    tiles[Point(x, y)] = TileId(t)
                    output_buffer = []
            else:
                break
        self.__cpu.reboot()
        return sum([1 for t in tiles if tiles[t] == TileId.BLOCK])

    def get_winning_score(self) -> int:
        self.__cpu.start_game()
        score = 0
        ball = 0
        paddle = 0
        output_buffer = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                if ball < paddle:
                    self.__cpu.add_input(Joystick.LEFT.value)
                elif ball > paddle:
                    self.__cpu.add_input(Joystick.RIGHT.value)
                else:
                    self.__cpu.add_input(Joystick.NEUTRAL.value)
            elif res == IntResult.OUTPUT:
                output_buffer.append(val)
                if len(output_buffer) == 3:
                    x, y, t = output_buffer
                    if (x, y) == (-1, 0):
                        score = t
                    else:
                        if TileId(t) == TileId.BALL:
                            ball = x
                        elif TileId(t) == TileId.HORIZONTAL_PADDLE:
                            paddle = x
                    output_buffer = []
            else:  # Halted
                break
        return score


def main() -> int:
    with open('../Inputfiles/aoc13.txt', 'r') as file:
        arcade = ArcadeGame(file.read().strip('\n'))
    print(f"Part 1: {arcade.get_block_tiles()}")
    print(f"Part 2: {arcade.get_winning_score()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
