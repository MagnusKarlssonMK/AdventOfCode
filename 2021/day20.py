"""
Converts the image to rows of integer values based on binary representation of '#' and '.', and then performs the
enhancement steps through bitmasking / bitshifting. Adds an extra layer in the map for every step.
Possibly this could be further optimized by pruning the boundaries in case the lit pixels stops growing outwards at
some point.
Also - unlike the example input, the real input toggles the void at each enhancement. So we also need to keep track
of the state of the void and use that for creating the outer buffer to get the correct result at the boundaries.
"""
import time
from pathlib import Path


class Image:
    def __init__(self, rawstr: str) -> None:
        algo, img_input = rawstr.split('\n\n')
        self.__voidvalue = '0'
        self.__algorithm = ['1' if c == "#" else '0' for c in algo]
        self.__x_range = 0
        self.__image = [0, 0]
        for line in img_input.splitlines():
            self.__x_range = len(line) + 4
            self.__image.append(int(''.join(['1' if c == "#" else '0' for c in line]) + '00', 2))
        self.__image.append(0)
        self.__image.append(0)
        self.__y_range = len(self.__image)

    def __enhance_image(self) -> None:
        self.__voidvalue = self.__algorithm[0 if self.__voidvalue == '0' else -1]
        voidrow = 0 if self.__voidvalue == '0' else int(''.join(['1' for _ in range(self.__x_range + 2)]), 2)
        new_image = [voidrow, voidrow]
        # Note: first and last row, and leftmost and rightmost columns just need to be there for the next positions
        # to draw from, but it's easier to just recreate them every round while also adding an extra new layer, rather
        # than converting based on void value. Thus adding buffer rows / cols twice every time.
        for y in range(1, self.__y_range - 1):
            new_row = self.__voidvalue + self.__voidvalue
            for x in range(1, self.__x_range - 1):
                v = ((((self.__image[y - 1] >> (self.__x_range - x - 2)) & 7) << 6) +
                     (((self.__image[y] >> (self.__x_range - x - 2)) & 7) << 3) +
                     ((self.__image[y + 1] >> (self.__x_range - x - 2)) & 7))
                new_row += self.__algorithm[v]
            new_row += self.__voidvalue + self.__voidvalue
            new_image.append(int(new_row, 2))
        new_image.append(voidrow)
        new_image.append(voidrow)
        self.__image = new_image
        self.__x_range += 2
        self.__y_range += 2

    def get_enhancement_count(self, count: int) -> int:
        for _ in range(count):
            self.__enhance_image()
        return sum([line.bit_count() for line in self.__image])


def main(aoc_input: str) -> None:
    myimg = Image(aoc_input)
    print(f"Part 1: {myimg.get_enhancement_count(2)}")
    print(f"Part 2: {myimg.get_enhancement_count(48)}")
    # Note: The state of the image is stored after the first two rounds, so we only need to do another 48 to get to 50.


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day20.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
