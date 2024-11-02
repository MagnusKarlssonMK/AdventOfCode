import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import math


@dataclass(frozen=True)
class Coordinate:
    row: int
    col: int


class Direction(Enum):
    UP = Coordinate(-1, 0)
    RIGHT = Coordinate(0, 1)
    DOWN = Coordinate(1, 0)
    LEFT = Coordinate(0, -1)


class Forest:
    def __init__(self, rawdata: str) -> None:
        self.__grid = [[int(c) for c in line] for line in rawdata.split('\n')]
        self.__width = len(self.__grid[0])
        self.__height = len(self.__grid)
        self.__grid_scores = [[{d: -1 for d in Direction} for _ in range(self.__width)] for _ in range(self.__height)]

    def getvisibletreecount(self) -> int:
        visible: set[Coordinate] = set()
        for r in range(self.__height):
            # From left:
            [visible.add(tree) for tree in self.__generatevisibletrees(r, -1, range(self.__width))]
            # From right:
            [visible.add(tree) for tree in self.__generatevisibletrees(r, -1, reversed(range(self.__width)))]
        for c in range(len(self.__grid[0])):
            # From above
            [visible.add(tree) for tree in self.__generatevisibletrees(-1, c, range(self.__height))]
            # From below
            [visible.add(tree) for tree in self.__generatevisibletrees(-1, c, reversed(range(self.__height)))]
        return len(visible)

    def __generatevisibletrees(self, row, col, iterable) -> iter:
        tallest = -1
        for i in iterable:
            if row == -1:
                r = i
                c = col
            else:
                r = row
                c = i
            if self.__grid[r][c] > tallest:
                tallest = self.__grid[r][c]
                yield Coordinate(r, c)
                if tallest == 9:
                    break

    def __setdirectionscores(self, row, col, direction: Direction, iterable) -> None:
        scorelist = [0 for _ in range(10)]
        for i in iterable:
            if row == -1:
                r = i
                c = col
            else:
                r = row
                c = i
            self.__grid_scores[r][c][direction] = scorelist[self.__grid[r][c]]
            for j in range(10):
                scorelist[j] = (scorelist[j] + 1) if j > self.__grid[r][c] else 1

    def getmaxscore(self) -> int:
        currentmax = 0
        for r in range(self.__height):
            self.__setdirectionscores(r, -1, Direction.LEFT, range(len(self.__grid[0])))
            self.__setdirectionscores(r, -1, Direction.RIGHT, reversed(range(len(self.__grid[0]))))
        for c in range(self.__width):
            self.__setdirectionscores(-1, c, Direction.UP, range(len(self.__grid)))
            self.__setdirectionscores(-1, c, Direction.DOWN, reversed(range(len(self.__grid))))
        for r in range(self.__height):
            for c in range(self.__width):
                score = math.prod(self.__grid_scores[r][c].values())
                currentmax = max(score, currentmax)
        return currentmax


def main(aoc_input: str) -> None:
    myforest = Forest(aoc_input)
    print(f"Part 1: {myforest.getvisibletreecount()}")
    print(f"Part 2: {myforest.getmaxscore()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
