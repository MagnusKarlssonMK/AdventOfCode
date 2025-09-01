"""
Creates a cavern class containing the octopus grid. Also adds a class internal adjacency list to avoid having to
generate the adjacent nodes every single time. When taking a step, go through all nodes and increment them (unless
they already flashed this step), and if a node flashes, increment all adjacent nodes, i.e. incrementation is done
recursively.
"""
import time
from pathlib import Path
from collections.abc import Generator


class Cavern:
    def __init__(self, rawstr: str) -> None:
        self.__grid = [[int(c) for c in line] for line in rawstr.splitlines()]
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])
        self.__flashcount = 0
        self.__flashed: set[tuple[int, int]] = set()
        self.__adj: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for row in range(self.__height):
            for col in range(self.__width):
                self.__adj[row, col] = [n for n in self.__getadjacent(row, col)]

    def __getadjacent(self, row: int, col: int) -> Generator[tuple[int, int]]:
        rowlimits = max(0, row - 1), min(row + 1, self.__height - 1)
        collimits = max(0, col - 1), min(col + 1, self.__width - 1)
        for r in range(rowlimits[0], rowlimits[1] + 1):
            for c in range(collimits[0], collimits[1] + 1):
                if (r, c) != (row, col):
                    yield r, c

    def __takestep(self) -> bool:
        for key in self.__adj:
            if key not in self.__flashed:
                self.__increment(*key)
        flashed = len(self.__flashed)
        self.__flashcount += flashed
        self.__flashed = set()
        if flashed == self.__height * self.__width:
            return True
        return False

    def __increment(self, row: int, col: int):
        if (row, col) not in self.__flashed:
            if self.__grid[row][col] < 9:
                self.__grid[row][col] += 1
            else:
                self.__grid[row][col] = 0
                self.__flashed.add((row, col))
                [self.__increment(r, c) for r, c in self.__adj[(row, col)]]

    def get_flashcounts(self) -> tuple[int, int]:
        p2 = 0
        p1 = -1
        while not self.__takestep():
            p2 += 1
            if p2 == 100:
                p1 = self.__flashcount
        return p1, p2 + 1


def main(aoc_input: str) -> None:
    cavern = Cavern(aoc_input)
    p1, p2 = cavern.get_flashcounts()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
