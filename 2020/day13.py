"""
Solved using the Chinese Remainder Theorem, and making use of the fact that the id:s are pairwise coprime.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day13.txt')


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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myschedule = BusSchedule(file.read().strip('\n'))
    print(f"Part 1: {myschedule.get_minwaitscore()}")
    print(f"Part 2: {myschedule.get_contesttimestamp()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
