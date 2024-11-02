"""
Solved using the Chinese Remainder Theorem, and making use of the fact that the id:s are pairwise coprime.
"""
import time
from pathlib import Path


class BusSchedule:
    def __init__(self, rawstr: str) -> None:
        estimate, buslist = rawstr.splitlines()
        self.__estimate = int(estimate)
        self.__buslist = [(int(v), i) for i, v in enumerate(buslist.split(',')) if v != 'x']

    def get_minwaitscore(self) -> int:
        bestbus = min([(busid, busid - (self.__estimate % busid)) for busid, _ in self.__buslist], key=lambda x: x[1])
        return bestbus[0] * bestbus[1]

    def get_contesttimestamp(self) -> int:
        remainder = 0
        coefficient = 1
        for busid, idx in self.__buslist:
            for i in range(1, busid):
                if (coefficient * i) % busid == 1:
                    remainder = ((((-idx % busid) - remainder) * i) % busid) * coefficient + remainder
                    coefficient *= busid
                    break
        return remainder


def main(aoc_input: str) -> None:
    myschedule = BusSchedule(aoc_input)
    print(f"Part 1: {myschedule.get_minwaitscore()}")
    print(f"Part 2: {myschedule.get_contesttimestamp()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day13.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
