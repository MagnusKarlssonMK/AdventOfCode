"""

"""
import sys
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


def main() -> int:
    with open('../Inputfiles/aoc16.txt', 'r') as file:
        sig = Signal(file.read().strip('\n'))
    print(f"Part 1: {sig.get_first_eight_digits()}")
    print(f"Part 2: {sig.apply_fft()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())