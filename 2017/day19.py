"""
Pretty much just walking a path and recording letters along the way. Only switch direction when encountering a '+' node,
otherwise keep walking in current direction and record the character if it is not a pipe. Count how many steps it takes
to get to the end.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    row: int
    col: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.row + other.row, self.col + other.col)

    def get_left(self) -> "Point":
        return Point(-self.col, self.row)

    def get_right(self) -> "Point":
        return Point(self.col, -self.row)


class Diagram:
    def __init__(self, rawstr: str) -> None:
        self.__grid = rawstr.splitlines()
        self.__start = Point(0, self.__grid[0].find('|'))

    def __get_point(self, p: Point) -> str:
        if not 0 <= p.row < len(self.__grid):
            return ' '
        if not 0 <= p.col < len(self.__grid[p.row]):
            return ' '
        return self.__grid[p.row][p.col]

    def get_path(self) -> tuple[str, int]:
        path = []
        point = self.__start
        direction = Point(1, 0)
        count = 0
        while True:
            count += 1
            point += direction
            match self.__get_point(point):
                case '+':
                    left = point + direction.get_left()
                    if self.__get_point(left) != ' ':
                        direction = direction.get_left()
                    else:
                        direction = direction.get_right()
                case ' ':
                    break
                case '-' | '|':
                    pass
                case _:
                    path.append(self.__get_point(point))
        return ''.join(path), count


def main(aoc_input: str) -> None:
    diagram = Diagram(aoc_input)
    path, steps = diagram.get_path()
    print(f"Part 1: {path}")
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day19.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
