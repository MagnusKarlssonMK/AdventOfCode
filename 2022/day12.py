"""
Part 1 - loads the grid into a grid class, and then finding the path is pretty much just a basic BFS, with some extra
condition checks when looking up the neighbors.
Part 2 - similar to Part 1, but this instead does the BFS 'backwards' starting from the end point and also reverses
the condition in the neighbor check.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def get_neighbors(self) -> Generator["Point"]:
        for d in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            yield self + Point(*d)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.row + other.row, self.col + other.col)


class Grid:
    def __init__(self, rawstr: str):
        self.__grid: list[str] = [line for line in rawstr.splitlines()]
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.__startpos: Point = Point(0, 0)
        self.__endpos: Point = Point(0, 0)
        for row in range(self.__height):
            if (startcol := self.__grid[row].find('S')) >= 0:
                self.__startpos = Point(row, startcol)
                self.__grid[row] = self.__grid[row].replace('S', 'a')
            if (endcol := self.__grid[row].find('E')) >= 0:
                self.__endpos = Point(row, endcol)
                self.__grid[row] = self.__grid[row].replace('E', 'z')

    def getneigbors(self, coord: Point, downhill: bool = False) -> Generator[Point]:
        for n in coord.get_neighbors():
            if 0 <= n.row < self.__height and 0 <= n.col < self.__width:
                current = ord(self.__grid[coord.row][coord.col])
                candidate = ord(self.__grid[n.row][n.col])
                if (current + 1 >= candidate and not downhill) or (current <= candidate + 1 and downhill):
                    yield n

    def get_minsteps_fromstart(self) -> int:
        # Part 1: Regular BFS search from S to E
        visited: dict[Point, int] = {}
        tilequeue: list[tuple[Point, int]] = [(self.__startpos, 0)]
        while tilequeue:
            current_pos, current_steps = tilequeue.pop(0)
            if current_pos == self.__endpos:
                return current_steps
            if current_pos in visited:
                continue
            for neighbor in self.getneigbors(current_pos):
                if neighbor not in visited:
                    tilequeue.append((neighbor, current_steps + 1))
            visited[current_pos] = current_steps
        return -1

    def get_minsteps_fromany(self) -> int:
        # Part 2: BFS again but starting from E and going downhill until finding the first 'a'
        visited: dict[Point, int] = {}
        tilequeue: list[tuple[Point, int]] = [(self.__endpos, 0)]
        while tilequeue:
            current_pos, current_steps = tilequeue.pop(0)
            if self.__grid[current_pos.row][current_pos.col] == 'a':
                return current_steps
            if current_pos in visited:
                continue
            for neighbor in self.getneigbors(current_pos, True):
                if neighbor not in visited:
                    tilequeue.append((neighbor, current_steps + 1))
            visited[current_pos] = current_steps
        return -1


def main(aoc_input: str) -> None:
    mygrid = Grid(aoc_input)
    print(f"Part 1: {mygrid.get_minsteps_fromstart()}")
    print(f"Part 2: {mygrid.get_minsteps_fromany()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
