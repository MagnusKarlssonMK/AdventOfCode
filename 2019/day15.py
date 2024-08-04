"""
BFS day!
Unsurprisingly by now, we need the Intcode computer again for use on a repair bot.
- Step one: we need to create a map of the maze with the bot program. Generate inputs by using BFS to find the
shortest path to an unknown tile, until there are no more reachable unknown tiles.
- Step two: use BFS from the start point to get minimum number of steps to the tile with oxygen. This gives us the
answer to part 1.
- Step 3: use BFS starting from the oxygen tile and run until all reachable tiles have been seen / filled. This gives
the answer to part 2.
"""
import sys
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day15.txt')


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


class InputCommand(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class DroidStatus(Enum):
    WALL = 0
    OK = 1
    OXYGEN = 2


class MazeMap:
    __DIRECTIONS = {InputCommand.NORTH: Point(0, -1), InputCommand.SOUTH: Point(0, 1),
                    InputCommand.WEST: Point(-1, 0), InputCommand.EAST: Point(1, 0)}

    def __init__(self) -> None:
        self.__maze: dict[Point: DroidStatus] = {Point(0, 0): DroidStatus.OK}

    def get_unknown_path(self, from_pos: Point) -> list[InputCommand]:
        queue = [(from_pos, None, None)]
        seen: dict[Point: tuple[Point, InputCommand]] = {}
        while queue:
            current, previous, command = queue.pop(0)
            if current not in self.__maze:
                seen[current] = (previous, command)
                result = []
                while current != from_pos:
                    current, cmd = seen[current]
                    result.append(cmd)
                return list(reversed(result))
            if current in seen:
                continue
            elif previous:
                seen[current] = (previous, command)
            for dc, dp in MazeMap.__DIRECTIONS.items():
                neighbor = current + dp
                if neighbor == previous:
                    continue
                if neighbor not in self.__maze or self.__maze[neighbor] != DroidStatus.WALL:
                    queue.append((neighbor, current, dc))
        return []

    def add_tile(self, p: Point, v: DroidStatus) -> None:
        self.__maze[p] = v

    def get_shortest_path(self) -> int:
        queue = [(Point(0, 0), 0)]
        seen = set()
        while queue:
            current, steps = queue.pop(0)
            if self.__maze[current] == DroidStatus.OXYGEN:
                return steps
            if current in seen:
                continue
            seen.add(current)
            for d in MazeMap.__DIRECTIONS.values():
                n = current + d
                if n not in seen and self.__maze[n] != DroidStatus.WALL:
                    queue.append((n, steps + 1))
        return -1

    def get_flood_time(self) -> int:
        oxygen_point = list(self.__maze.keys())[list(self.__maze.values()).index(DroidStatus.OXYGEN)]
        steps = 0
        queue = [(oxygen_point, steps)]
        seen = set()
        while queue:
            current, steps = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)
            for d in MazeMap.__DIRECTIONS.values():
                n = current + d
                if n not in seen and self.__maze[n] != DroidStatus.WALL:
                    queue.append((n, steps + 1))
        return steps


class RepairDroid:
    __DIRECTIONS = {InputCommand.NORTH: Point(0, -1), InputCommand.SOUTH: Point(0, 1),
                    InputCommand.WEST: Point(-1, 0), InputCommand.EAST: Point(1, 0)}

    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(rawstr)
        self.__maze = MazeMap()

    def __build_maze_map(self) -> None:
        droid_pos = Point(0, 0)
        droid_direction = Point(0, -1)
        input_buffer = []
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                if not input_buffer:
                    input_buffer = self.__maze.get_unknown_path(droid_pos)
                if not input_buffer:  # No more reachable unknowns
                    break
                step = input_buffer.pop(0)
                droid_direction = RepairDroid.__DIRECTIONS[step]
                self.__cpu.add_input(step.value)
            elif res == IntResult.OUTPUT:
                self.__maze.add_tile(droid_pos + droid_direction, DroidStatus(val))
                if DroidStatus(val) != DroidStatus.WALL:
                    droid_pos += droid_direction
            else:
                break
        self.__cpu.reboot()

    def get_min_movement_cmds(self) -> int:
        self.__build_maze_map()
        return self.__maze.get_shortest_path()

    def get_oxygen_fill_time(self) -> int:
        return self.__maze.get_flood_time()


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        droid = RepairDroid(file.read().strip('\n'))
    print(f"Part 1: {droid.get_min_movement_cmds()}")
    print(f"Part 2: {droid.get_oxygen_fill_time()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
