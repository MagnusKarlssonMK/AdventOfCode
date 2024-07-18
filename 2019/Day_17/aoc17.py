"""
Part 1: Run the intcode program to generate the map, then store the scaffold tiles as an adjacency list. The answer
can then be determined by finding the tiles that have more than 2 neighbors.

Part 2: TBD
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


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> iter:
        for n in (Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)):
            yield self + n

    def get_alignment(self) -> int:
        return self.x * self.y

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Scaffold:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode([int(nbr) for nbr in rawstr.split(',')])
        self.__map: dict[Point: list[Point]] = {}
        self.__vacuum_pos = None
        self.__vacuum_dir = None

    def get_alignment_sum(self) -> int:
        vacuum_dirs = {'^': Point(0, -1), '>': Point(1, 0), 'v': Point(0, 1), '<': Point(-1, 0)}
        x = y = 0
        # Generate the map tiles using the intcode
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                tile = chr(val)
                if tile == "#":
                    self.__map[Point(x, y)] = set()
                    x += 1
                elif tile in vacuum_dirs:
                    self.__map[Point(x, y)] = set()
                    self.__vacuum_pos = Point(x, y)
                    self.__vacuum_dir = vacuum_dirs[tile]
                    x += 1
                elif tile == "\n":
                    y += 1
                    x = 0
                else:
                    x += 1
            else:
                break
        self.__cpu.reboot()

        # Fill in the neighbors in the map
        for p in self.__map:
            for n in p.get_neighbors():
                if n in self.__map:
                    self.__map[p].add(n)
        return sum([p.get_alignment() for p in self.__map if len(self.__map[p]) > 2])


def main() -> int:
    with open('../Inputfiles/aoc17.txt', 'r') as file:
        scaffold = Scaffold(file.read().strip('\n'))
    print(f"Part 1: {scaffold.get_alignment_sum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


"""
........................................#############..
........................................#...........#..
........#######.........................#...........#..
........#.....#.........................#...........#..
........#.....#.#############...........#...........#..
........#.....#.#...........#...........#...........#..
........#.....#.#...........#...........#...........#..
........#.....#.#...........#...........#...........#..
........#############.......#...........#...........#..
..............#.#...#.......#...........#...........#..
..............#.#.###########.....#######...........#..
..............#.#.#.#.............#.................#..
..............###########.........#.......###########..
................#.#.#...#.........#.......#............
................#.#.#...#.........#.......#............
................#.#.#...#.........#.......#............
................##########^.......#.......#............
..................#.#...#.........#.......#............
..........###########...#.........#.......#............
..........#.......#.....#.........#.......#............
..........#.......###########.....#.......#............
..........#.............#...#.....#.......#............
......###########.......###########.......#############
......#...#.....#...........#.........................#
......#...#.....#...........#.........................#
......#...#.....#...........#.........................#
......#...#.....#...........#.........................#
......#...#.....#...........#.........................#
###########.....#...........#.........................#
#.....#.........#...........#..........................
#.....#.........#...........#..........................
#.....#.........#...........#..........................
#.....#.........#############..........................
#.....#................................................
#######................................................

"""
