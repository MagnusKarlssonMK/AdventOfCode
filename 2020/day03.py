"""
Store the tree map in a grid class, with a method to count the number of trees encountered for a certain input step
pattern. When checking the columns, take the column coordinate of the location mod number of columns in the grid,
in order to handle the expanding grid sideways.
"""
import time
from pathlib import Path
import math


class TreeMap:
    def __init__(self, rawstr: str) -> None:
        self.__grid = rawstr.splitlines()
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])

    def __counttrees(self, rowstep: int, colstep: int) -> int:
        r, c, count = 0, 0, 0
        while r < self.__height - 1:
            c += colstep
            r += rowstep
            if self.__grid[r][c % self.__width] == '#':
                count += 1
        return count

    def get_treecount_simple(self) -> int:
        return self.__counttrees(1, 3)

    def get_treecount_full(self) -> int:
        steps = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
        return math.prod([self.__counttrees(r, c) for r, c in steps])


def main(aoc_input: str) -> None:
    treemap = TreeMap(aoc_input)
    print(f"Part 1: {treemap.get_treecount_simple()}")
    print(f"Part 2: {treemap.get_treecount_full()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
