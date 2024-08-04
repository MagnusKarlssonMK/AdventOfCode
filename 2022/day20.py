import sys
from pathlib import Path
from collections import deque

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day20.txt')


class Sequence:
    __GROVE_COORDINATES = (1000, 2000, 3000)
    __ENCRYPTION_KEY = 811589153
    __MIX_COUNT = 10

    def __init__(self, rawstr: str) -> None:
        self.__startnbrs = list(map(int, rawstr.splitlines()))

    def __mix(self, count: int = 1) -> list[int]:
        nbrs = deque(list(enumerate(list(self.__startnbrs))))
        nbrs_len = len(nbrs)
        for _ in range(count):
            for idx in range(nbrs_len):
                while nbrs[0][0] != idx:
                    nbrs.rotate(-1)
                i, v = nbrs.popleft()
                nbrs.rotate(-(v % (nbrs_len - 1)))
                nbrs.append((i, v))
        return [v for _, v in nbrs]

    def get_coordsum(self) -> int:
        mixed_nbrs = self.__mix()
        return sum([mixed_nbrs[(mixed_nbrs.index(0) + n) % len(mixed_nbrs)] for n in Sequence.__GROVE_COORDINATES])

    def get_encryptedcoordsum(self) -> int:
        for i, n in enumerate(self.__startnbrs):
            self.__startnbrs[i] = n * Sequence.__ENCRYPTION_KEY
        mixed_nbrs = self.__mix(Sequence.__MIX_COUNT)
        return sum([mixed_nbrs[(mixed_nbrs.index(0) + n) % len(mixed_nbrs)] for n in Sequence.__GROVE_COORDINATES])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        sequence = Sequence(file.read().strip('\n'))
    print(f"Part 1: {sequence.get_coordsum()}")
    print(f"Part 2: {sequence.get_encryptedcoordsum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
