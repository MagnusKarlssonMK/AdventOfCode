"""
Just making a simple iterator and compare the generated values. Takes a fair amount of time to run (~10s for each part),
I couldn't help but wonder if there was some kind of cycle detection to figure out, but couldn't find any.
"""
import time
from pathlib import Path
from collections.abc import Generator


class Duel:
    __FACTORS = (16807, 48271)
    __MULTIPLES = (4, 8)
    __DIVISOR = 2147483647

    def __init__(self, rawstr: str) -> None:
        self.__startvalues = [int(w[-1]) for w in [line.split() for line in rawstr.splitlines()]]

    def __generator(self, idx: int, use_multiples: bool = False) -> Generator[int]:
        v = self.__startvalues[idx]
        m = Duel.__MULTIPLES[idx] if use_multiples else 1
        while True:
            v = v * Duel.__FACTORS[idx] % Duel.__DIVISOR
            if v % m == 0:
                yield v & 0xffff

    def get_final_count(self) -> int:
        generators = [self.__generator(i) for i in range(len(self.__startvalues))]
        return sum([1 for _ in range(40_000_000) if next(generators[0]) == next(generators[1])])

    def get_modified_final_count(self) -> int:
        generators = [self.__generator(i, True) for i in range(len(self.__startvalues))]
        return sum([1 for _ in range(5_000_000) if next(generators[0]) == next(generators[1])])


def main(aoc_input: str) -> None:
    duel = Duel(aoc_input)
    print(f"Part 1: {duel.get_final_count()}")
    print(f"Part 2: {duel.get_modified_final_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day15.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
