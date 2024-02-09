"""
Store the tree map in a grid class, with a method to count the number of trees encountered for a certain input step
pattern. When checking the columns, take the column coordinate of the location mod number of columns in the grid,
in order to handle the expanding grid sideways.
"""
import sys
import math


class TreeMap:
    def __init__(self, rawstr: str):
        self.__grid = rawstr.splitlines()
        self.__height = len(self.__grid)
        self.__width = len(self.__grid[0])

    def counttrees(self, rowstep: int, colstep: int) -> int:
        r, c, count = 0, 0, 0
        while r < self.__height - 1:
            c += colstep
            r += rowstep
            if self.__grid[r][c % self.__width] == '#':
                count += 1
        return count


def main() -> int:
    with open('../Inputfiles/aoc3.txt', 'r') as file:
        treemap = TreeMap(file.read().strip('\n'))
    print("Part 1:", treemap.counttrees(1, 3))
    p2steps = [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
    print("Part 2:", math.prod([treemap.counttrees(r, c) for r, c in p2steps]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
