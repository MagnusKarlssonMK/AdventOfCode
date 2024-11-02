"""

"""
import time
from pathlib import Path
import numpy as np


class Signal:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [int(c) for c in rawstr]
        self.__pattern = [0, 1, 0, -1]

    def get_first_eight_digits(self) -> str:
        nbrs = np.array(self.__nbrs)
        base_pattern = np.array(self.__pattern)
        for _ in range(100):
            matrix = np.tile(nbrs, (nbrs.size, 1))
            patterns = np.zeros(matrix.shape, matrix.dtype)
            for i in range(1, nbrs.size + 1):
                count = int(np.ceil(nbrs.size / ((i * base_pattern.size) - 1)))
                patterns[i - 1, :] = np.tile(np.repeat(base_pattern, i), count)[1: 1 + nbrs.size]
            nbrs = np.abs((matrix * patterns).sum(axis=1)) % 10
        return ''.join(map(str, nbrs[:8]))

    def apply_fft(self) -> str:
        nbrs = np.array(self.__nbrs)
        offset = (10 ** np.arange(6, -1, -1) * nbrs[:7]).sum()
        o_s = np.tile(nbrs, 10_000)[offset:]
        for _ in range(100):
            o_s = np.cumsum(o_s[::-1])[::-1] % 10
        return ''.join(map(str, o_s[:8]))


def main(aoc_input: str) -> None:
    sig = Signal(aoc_input)
    print(f"Part 1: {sig.get_first_eight_digits()}")
    print(f"Part 2: {sig.apply_fft()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day16.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
