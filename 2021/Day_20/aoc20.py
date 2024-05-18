"""
Store the input image as a dict(?) of rows (y), each pointing to a set of cols (x) where the point is 'light' (#).
Top left of the first input image is (0, 0), x+ -> right, y+ -v down.
BUT - unlike the example input, the real input toggles the void at each enhancement. So we also need to keep track
of the state of the void to get the correct result at the boundaries.
"""
import sys
from collections import defaultdict


class Image:
    def __init__(self, rawstr: str) -> None:
        algo, input_img = rawstr.split('\n\n')
        self.__image = defaultdict(set)
        self.__x_range: list[int] = [0, 0]
        self.__y_range: list[int] = [0, 0]
        self.__algorithm = ''.join(['1' if c == '#' else '0' for c in algo])
        self.__voidvalue = '0'
        for y, row in enumerate(input_img.splitlines()):
            for x, col in enumerate(row):
                if col == "#":
                    self.__image[y].add(x)
                    self.__x_range[1] = max(self.__x_range[1], x)
                    self.__y_range[1] = max(self.__y_range[1], y)

    def __get_coordvalue(self, x: int, y: int) -> str:
        if not self.__y_range[0] <= y <= self.__y_range[1] or not self.__x_range[0] <= x <= self.__x_range[1]:
            return self.__voidvalue
        if y in self.__image and x in self.__image[y]:
            return '1'
        return '0'

    def __apply_algorithm(self) -> None:
        new_layer = defaultdict(set)
        new_x_range = list(self.__x_range)
        new_y_range = list(self.__y_range)
        for x in range(self.__x_range[0] - 1, self.__x_range[1] + 2):
            for y in range(self.__y_range[0] - 1, self.__y_range[1] + 2):
                nbr = ''
                for i in range(-1, 2):
                    nbr += (self.__get_coordvalue(x - 1, y + i) + self.__get_coordvalue(x, y + i) +
                            self.__get_coordvalue(x + 1, y + i))
                if self.__algorithm[int(nbr, 2)] == '1':
                    new_layer[y].add(x)
                    new_x_range = [min(new_x_range[0], x), max(new_x_range[1], x)]
                    new_y_range = [min(new_y_range[0], y), max(new_y_range[1], y)]
        self.__image = new_layer
        self.__x_range = list(new_x_range)
        self.__y_range = list(new_y_range)
        self.__voidvalue = self.__algorithm[0 if self.__voidvalue == '0' else -1]

    def get_tworounds_count(self) -> int:
        self.__apply_algorithm()
        self.__apply_algorithm()
        count = 0
        for y in self.__image:
            count += len(self.__image[y])
        return count


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        myimg = Image(file.read().strip('\n'))
    print(f"Part 1: {myimg.get_tworounds_count()}")
    return 0

# ! 5464


if __name__ == "__main__":
    sys.exit(main())
