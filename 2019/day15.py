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
import time
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from intcode import Intcode, IntResult


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
        self.__maze: dict[Point, DroidStatus] = {Point(0, 0): DroidStatus.OK}

    def get_unknown_path(self, from_pos: Point) -> list[InputCommand]:
        queue: list[tuple[Point, Point, InputCommand]] = [(from_pos, None, None)]
        seen: dict[Point, tuple[Point, InputCommand]] = {}
        while queue:
            current, previous, command = queue.pop(0)
            if current not in self.__maze:
                seen[current] = (previous, command)
                result: list[InputCommand] = []
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
        seen: set[Point] = set()
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
        seen: set[Point] = set()
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
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))
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


def main(aoc_input: str) -> None:
    droid = RepairDroid(aoc_input)
    print(f"Part 1: {droid.get_min_movement_cmds()}")
    print(f"Part 2: {droid.get_oxygen_fill_time()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day15.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
