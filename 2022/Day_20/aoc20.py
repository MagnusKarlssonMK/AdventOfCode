import sys
from collections import deque


class Sequence:
    def __init__(self, startnbrs: list[int]):
        self.startnbrs = list(startnbrs)

    def __mix(self, count: int = 1) -> list[int]:
        nbrs = deque(list(enumerate(list(self.startnbrs))))
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
        return sum([mixed_nbrs[(mixed_nbrs.index(0) + n) % len(mixed_nbrs)] for n in (1000, 2000, 3000)])

    def get_encryptedcoordsum(self) -> int:
        for i, n in enumerate(self.startnbrs):
            self.startnbrs[i] = n * 811589153
        mixed_nbrs = self.__mix(10)
        return sum([mixed_nbrs[(mixed_nbrs.index(0) + n) % len(mixed_nbrs)] for n in (1000, 2000, 3000)])


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        sequence = Sequence([int(n) for n in file.read().strip('\n').splitlines()])
    print(f"Part 1: {sequence.get_coordsum()}")
    print(f"Part 2: {sequence.get_encryptedcoordsum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
