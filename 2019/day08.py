"""
Store each layer as an array of numbers, don't convert it to 2D until building the actual image. For solving
part 1, having it as simple lists is easier.
"""
import time
from pathlib import Path
from collections import Counter


class Image:
    def __init__(self, rawstr: str, width: int = 25, height: int = 6) -> None:
        self.__width = width
        self.__height = height
        self.__layers = []
        i = 0
        while i < len(rawstr):
            self.__layers.append([int(c) for c in rawstr[i: i + self.__height * self.__width]])
            i += self.__width * self.__height

    def get_checksum(self) -> int:
        results = []
        for layer in self.__layers:
            c = Counter(layer)
            results.append((c[0], c[1] * c[2]))
        results.sort(key=lambda x: x[0])
        return results[0][1]

    def decode_image(self) -> str:
        img = self.__layers[0]
        for layeridx in range(1, len(self.__layers)):
            for i, nbr in enumerate(self.__layers[layeridx]):
                if img[i] == 2:
                    img[i] = nbr
        result = ''
        for i, n in enumerate(img):
            if i % self.__width == 0:
                result += '\n'
            result += '#' if n == 1 else ' '
        return result


def main(aoc_input: str) -> None:
    img = Image(aoc_input)
    print(f"Part 1: {img.get_checksum()}")
    print(f"Part 2:\n{img.decode_image()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
