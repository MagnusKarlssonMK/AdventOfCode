"""
Taking an easy approach - simply storing the lines on a grid quite literally as in the example.
Not very efficient, as compared to a more advanced approach like trying to detect and count intersection points,
but since the coordinate numbers are relatively small we can get away with a simple solution.
"""

import sys
import re

XY = tuple[int, int]


class Seabottom:
    def __init__(self, points: list[tuple[XY, XY]]):
        self.__points = points
        self.__x_max = 0
        self.__y_max = 0
        for p in self.__points:
            self.__x_max = max(p[0][0], p[1][0], self.__x_max)
            self.__y_max = max(p[0][1], p[1][1], self.__y_max)
        self.__x_max += 1
        self.__y_max += 1
        self.__grid = [[0 for _ in range(self.__x_max)] for _ in range(self.__y_max)]
        for p in self.__points:
            dx = (p[1][0] - p[0][0]) // max(abs(p[1][0] - p[0][0]), abs(p[1][1] - p[0][1]), 1)
            dy = (p[1][1] - p[0][1]) // max(abs(p[1][0] - p[0][0]), abs(p[1][1] - p[0][1]), 1)
            # Note - '1' as third max argument in divider in case of start point == stop point
            x = p[0][0]
            y = p[0][1]
            while True:
                self.__grid[y][x] += 1
                if (x, y) == p[1]:
                    break
                x += dx
                y += dy

    def getscore(self) -> int:
        retval = 0
        for y in self.__grid:
            for x in y:
                if x > 1:
                    retval += 1
        return retval


def main() -> int:
    lines: list[tuple[XY, XY]] = []
    with open('../Inputfiles/aoc5.txt') as file:
        for line in file.read().strip('\n').splitlines():
            x1, y1, x2, y2 = list(map(int, re.findall(r"\d+", line)))
            lines.append(((x1, y1), (x2, y2)))
    p1_lines = []
    for line in lines:
        if line[0][0] == line[1][0] or line[0][1] == line[1][1]:
            p1_lines.append(line)
    p1_bottom = Seabottom(p1_lines)
    print("Part 1: ", p1_bottom.getscore())

    p2_bottom = Seabottom(lines)
    print("Part 2: ", p2_bottom.getscore())
    return 0


if __name__ == "__main__":
    sys.exit(main())
