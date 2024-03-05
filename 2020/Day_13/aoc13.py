"""
Solved using the Chinese Remainder Theorem, and making use of the fact that the id:s are pairwise coprime.
"""
import sys


class BusSchedule:
    def __init__(self, buslist: list[str]):
        self.__buslist = [(int(v), i) for i, v in enumerate(buslist) if v != 'x']

    def get_minwaitscore(self, estimate: int) -> int:
        bestbus = min([(busid, busid - (estimate % busid)) for busid, _ in self.__buslist], key=lambda x:x[1])
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
    with open('../Inputfiles/aoc13.txt', 'r') as file:
        lines = file.read().strip('\n').splitlines()
    myschedule = BusSchedule(lines[1].split(','))
    print("Part 1:", myschedule.get_minwaitscore(int(lines[0])))
    print("Part 2:", myschedule.get_contesttimestamp())
    return 0


if __name__ == "__main__":
    sys.exit(main())
