"""
Store the data in a grid, then for Part 1 simply walk through the system until returning to the start, then calculating
the answer by dividing the number of steps taken by 2. For part 2, calculate the answer by first determining the area
with the shoelace formula and then use that with Pick's theorem.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Coord:
    row: int
    col: int

    def __add__(self, other: "Coord") -> "Coord":
        return Coord(self.row + other.row, self.col + other.col)

    def get_reverse(self) -> "Coord":
        return Coord(self.row * -1, self.col * -1)


class Maze:
    __DIRECTIONS = {'u': Coord(-1, 0), 'r': Coord(0, 1), 'd': Coord(1, 0), 'l': Coord(0, -1)}
    __PIPES = {'|': ('u', 'd'), '-': ('l', 'r'), 'L': ('u', 'r'), 'J': ('u', 'l'), '7': ('d', 'l'),
               'F': ('d', 'r')}

    def __init__(self, rawstr: str) -> None:
        self.__grid = rawstr.splitlines()
        self.__startpoint = None
        for rowidx, row in enumerate(self.__grid):
            if (idx := row.find('S')) >= 0:
                self.__startpoint = Coord(rowidx, idx)
        # Note: when starting at 'S', take whatever direction we find first, it doesn't matter which way we walk
        for direction in Maze.__DIRECTIONS.values():
            v = self.__get_value(self.__startpoint + direction)
            if v == '.':
                continue
            if direction.get_reverse() in [Maze.__DIRECTIONS[p] for p in Maze.__PIPES[v]]:
                self.__startdirection = direction
                break
        self.__pipepath: list[Coord] = []

    def __get_value(self, pos: Coord) -> str:
        return self.__grid[pos.row][pos.col]

    def __get_nextstepdir(self, pos: Coord, indir: Coord) -> Coord:
        for outdir in Maze.__PIPES[self.__get_value(pos)]:
            if Maze.__DIRECTIONS[outdir] != indir.get_reverse():
                return Maze.__DIRECTIONS[outdir]
        return indir  # Should never happen, there should always be one out...

    def __traverse(self) -> None:
        self.__pipepath = []
        currentdir = self.__startdirection
        currentpos = self.__startpoint + currentdir
        self.__pipepath.append(self.__startpoint)
        while currentpos != self.__startpoint:
            self.__pipepath.append(currentpos)
            # Trust that the grid content will never lead us outside the grid, so skip boundary check of new pos
            currentdir = self.__get_nextstepdir(currentpos, currentdir)
            currentpos += currentdir

    def get_farpoint_length(self) -> int:
        if not self.__pipepath:
            self.__traverse()
        return len(self.__pipepath) // 2

    def get_enclosed_count(self) -> int:
        if not self.__pipepath:
            self.__traverse()
        # Calculate shoelace area
        area = 0
        for idx, _ in enumerate(self.__pipepath):
            area += ((self.__pipepath[idx].col * self.__pipepath[(idx + 1) % len(self.__pipepath)].row) -
                     (self.__pipepath[(idx + 1) % len(self.__pipepath)].col * self.__pipepath[idx].row))
            # Note: we need to 'close the loop' and include also the combination of the first and last entries, thus
            # mod length for the idx + 1 point
        area = abs(area) // 2
        # Use Pick's theorem to get number of enclosed tiles
        return area + 1 - (len(self.__pipepath) // 2)


def main(aoc_input: str) -> None:
    mymaze = Maze(aoc_input)
    print(f"Part 1: {mymaze.get_farpoint_length()}")
    print(f"Part 2: {mymaze.get_enclosed_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
