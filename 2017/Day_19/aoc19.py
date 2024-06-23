"""
Pretty much just walking a path and recording letters along the way. Only switch direction when encountering a '+' node,
otherwise keep walking in current direction and record the character if it is not a pipe. Count how many steps it takes
to get to the end.
"""
import sys
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
        self.__start = Point(0, len(self.__grid[0]) - 1)

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


def main() -> int:
    with open('../Inputfiles/aoc19.txt', 'r') as file:
        diagram = Diagram(file.read().strip('\n'))
    path, steps = diagram.get_path()
    print(f"Part 1: {path}")
    print(f"Part 2: {steps}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
