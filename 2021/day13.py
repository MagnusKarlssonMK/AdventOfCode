"""
Solution: store the parsed coordinates in a Paper class, in a set rather than a list to easier handle overlapping
points when folding the paper later.
"""
import sys


class Paper:
    def __init__(self, rawstr: str) -> None:
        c, f = rawstr.split('\n\n')
        # Flip the coordinates so x,y -> row, col
        self.__coordinates = set([(int(b), int(a)) for a, b in [coord.split(',') for coord in c.splitlines()]])
        self.__folding = [(j, int(k)) for j, k in [i.strip('fold along ').split('=') for i in f.splitlines()]]
        self.__height = -1
        self.__width = -1

    def __fold(self, axis: str, value: int) -> None:
        if axis == 'x':  # Col
            coords = [c for c in self.__coordinates]
            for row, col in coords:
                if col > value:
                    self.__coordinates.remove((row, col))
                    self.__coordinates.add((row, 2 * value - col))
            self.__width = value
        elif axis == 'y':  # Row
            coords = [c for c in self.__coordinates]
            for row, col in coords:
                if row > value:
                    self.__coordinates.remove((row, col))
                    self.__coordinates.add((2 * value - row, col))
            self.__height = value

    def fold_and_get_dots(self) -> int:
        retval = -1
        for idx, fold in enumerate(self.__folding):
            self.__fold(*fold)
            if idx == 0:
                retval = len(self.__coordinates)
        return retval

    def __str__(self):
        grid = [['.' for _ in range(self.__width)] for _ in range(self.__height)]
        for r, c in self.__coordinates:
            grid[r][c] = "#"
        return f"{''.join([line + '\n' for line in [''.join(s) for s in grid]])}"


def main() -> int:
    with open('../Inputfiles/aoc13.txt', 'r') as file:
        mypaper = Paper(file.read().strip('\n'))
    print(f"Part 1: {mypaper.fold_and_get_dots()}")
    print(f"Part 2: \n{mypaper}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
