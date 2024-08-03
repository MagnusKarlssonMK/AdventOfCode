"""
Part 1: Trivial, just apply a mod operation on the peek-ahead index for the wraparound at the end.
Part 2: Just change the offset in the peek-ahead from 1 to half the length of the number list.
"""
import sys


class Sequence:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = [int(c) for c in rawstr]

    def get_captcha(self, halfway: bool = False) -> int:
        offset = 1 if not halfway else len(self.__nbrs) // 2
        return sum([nbr for i, nbr in enumerate(self.__nbrs) if nbr == self.__nbrs[(i + offset) % len(self.__nbrs)]])


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        seq = Sequence(file.read().strip('\n'))
    print(f"Part 1: {seq.get_captcha()}")
    print(f"Part 2: {seq.get_captcha(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
