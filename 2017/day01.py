"""
Part 1: Trivial, just apply a mod operation on the peek-ahead index for the wraparound at the end.
Part 2: Just change the offset in the peek-ahead from 1 to half the length of the number list.
"""
import time
from pathlib import Path


class Sequence:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [int(c) for c in rawstr]

    def get_captcha(self, halfway: bool = False) -> int:
        offset = 1 if not halfway else len(self.__nbrs) // 2
        return sum([nbr for i, nbr in enumerate(self.__nbrs) if nbr == self.__nbrs[(i + offset) % len(self.__nbrs)]])


def main(aoc_input: str) -> None:
    seq = Sequence(aoc_input)
    print(f"Part 1: {seq.get_captcha()}")
    print(f"Part 2: {seq.get_captcha(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
