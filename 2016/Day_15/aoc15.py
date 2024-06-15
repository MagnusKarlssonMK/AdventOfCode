"""
All divisors (nbr of positions for each disc) are pairwise coprime -> yep, it's Chinese remainder time.
"""
import sys
import re
from dataclasses import dataclass
import math


def chinese_remainder(num: list[int], rem: list[int]) -> int:
    result = 0
    prod = math.prod(num)
    for n, r in zip(num, rem):
        p = prod // n
        result += r * inv(p, n) * p
    return result % prod


def inv(a: int, b: int) -> int:
    if b == 1:
        return 1
    b0 = b
    x0, x1 = 0, 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


@dataclass
class Disc:
    nbr_positions: int
    start_position: int


class Sculpture:
    def __init__(self, rawstr: str) -> None:
        nbrs = [list(map(int, [nbrs for nbrs in re.findall(r"\d+", line)])) for line in rawstr.splitlines()]
        self.__discs = {i: Disc(n, p) for i, n, _, p in nbrs}

    def get_buttonpress_time(self, extra_disc: bool = False) -> int:
        if extra_disc:  # A bit lazy, the added disc should ideally be cleaned up before exiting the function...
            self.__discs[1 + len(self.__discs)] = Disc(11, 0)
        a = [self.__discs[d].nbr_positions for d in self.__discs]
        b = [self.__discs[d].nbr_positions - (self.__discs[d].start_position + d) % self.__discs[d].nbr_positions
             for d in self.__discs]
        return chinese_remainder(a, b)


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        sculpture = Sculpture(file.read().strip('\n'))
    print(f"Part 1: {sculpture.get_buttonpress_time()}")
    print(f"Part 2: {sculpture.get_buttonpress_time(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())