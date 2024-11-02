"""
Pretty basic game of life. Not a very efficient solution, but gets the job done in a couple of seconds.
Would probably be much improved just by using numpy instead.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def __add__(self, other: 'Coord') -> 'Coord':
        return Coord(self.row + other.row, self.col + other.col)


class Grid:
    __NEIGHBORS = [Coord(-1, -1), Coord(-1, 0), Coord(-1, 1), Coord(0, -1),
                   Coord(0, 1), Coord(1, -1), Coord(1, 0), Coord(1, 1)]

    def __init__(self, rawstr: str) -> None:
        self.__startgrid = []
        self.__currentgrid = []
        for line in rawstr.splitlines():
            self.__startgrid.append([1 if c == '#' else 0 for c in line])
            self.__currentgrid.append(list(self.__startgrid[-1]))
        self.__height = len(self.__startgrid)
        self.__width = len(self.__startgrid[0])
        self.__corners = [(0, 0), (0, self.__width - 1), (self.__height - 1, 0), (self.__height - 1, self.__width - 1)]

    def __get_neighbor_sum(self, c: Coord) -> int:
        n_sum = 0
        for n in Grid.__NEIGHBORS:
            point = c + n
            if 0 <= point.row < self.__height and 0 <= point.col < self.__width:
                n_sum += self.__currentgrid[point.row][point.col]
        return n_sum

    def __process_grid(self, corners_locked: bool) -> None:
        changelist = []
        for r, row in enumerate(self.__currentgrid):
            for c, val in enumerate(row):
                n_val = self.__get_neighbor_sum(Coord(r, c))
                if val == 1:
                    if n_val < 2 or n_val > 3:
                        changelist.append((r, c))
                else:
                    if n_val == 3:
                        changelist.append((r, c))
        for r, c in changelist:
            if not corners_locked or (r, c) not in self.__corners:
                self.__currentgrid[r][c] = (self.__currentgrid[r][c] + 1) % 2

    def get_lights_after_steps(self, corners_locked: bool = False, nbrsteps: int = 100) -> int:
        if corners_locked:
            for (r, c) in self.__corners:
                self.__currentgrid[r][c] = 1
        for _ in range(nbrsteps):
            self.__process_grid(corners_locked)
        retval = sum([sum(r) for r in self.__currentgrid])
        # reset current
        self.__currentgrid = []
        for row in self.__startgrid:
            self.__currentgrid.append(list(row))
        return retval


def main(aoc_input: str) -> None:
    grid = Grid(aoc_input)
    print(f"Part 1: {grid.get_lights_after_steps()}")
    print(f"Part 2: {grid.get_lights_after_steps(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
