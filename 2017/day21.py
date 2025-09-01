"""
Parts 1 & 2 are basically the same, Part 2 is pretty much just a stress test to see if the solution scales well with
larger numbers.
Takes the input and expands it into a dictionary of all possible combinations of 2- and 3-sized input blocks, and from
there it's mostly down to doing the necessary transformations for each step.
For a rainy day: a bit curious if it could run even faster by using recursion instead and expanding the dictionary
sort of like a memo cache along the way for larger block sizes?
"""
import time
from pathlib import Path


def flipblock(inblock: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([''.join(reversed(b)) for b in inblock])


def rotateblock(inblock: tuple[str, ...]) -> tuple[str, ...]:
    return tuple([''.join([inblock[row][col] for row in range(len(inblock))])
                  for col in reversed(range(len(inblock)))])


class ImageConverter:
    __START_IMAGE = ('.#.', '..#', '###')

    def __init__(self, rawstr: str) -> None:
        self.__transforms: dict[tuple[str, ...], tuple[str, ...]] = {}
        for line in rawstr.splitlines():
            left, right = line.split(' => ')
            inp1 = tuple(left.split('/'))  # Work with tuples to make it hashable and possible to use as dict key
            # Pre-compute the possible permutations of the left side
            inp2 = flipblock(inp1)
            out = right.split('/')
            self.__transforms[inp1] = out
            self.__transforms[inp2] = out
            for _ in range(3):
                inp1 = rotateblock(inp1)
                inp2 = rotateblock(inp2)
                self.__transforms[inp1] = out
                self.__transforms[inp2] = out

    def get_pixel_count(self, iterations: int) -> int:
        image = list(ImageConverter.__START_IMAGE)
        for _ in range(iterations):
            new_image: list[str] = []
            stepsize = 2 if len(image) % 2 == 0 else 3
            for row in range(0, len(image), stepsize):
                for _ in range(0, stepsize + 1):
                    new_image.append('')
                for col in range(0, len(image), stepsize):
                    block = [image[row + i][col: col + stepsize] for i in range(stepsize)]
                    transformed_block = self.__transforms[tuple(block)]
                    target_row = (row // stepsize) * (stepsize + 1)
                    for i in range(stepsize + 1):
                        new_image[target_row + i] += transformed_block[i]
            image = new_image
        return ''.join(image).count('#')


def main(aoc_input: str) -> None:
    converter = ImageConverter(aoc_input)
    print(f"Part 1: {converter.get_pixel_count(5)}")
    print(f"Part 1: {converter.get_pixel_count(18)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day21.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
