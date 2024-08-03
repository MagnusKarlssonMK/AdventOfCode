"""
Surprisingly simple, the main challenge is simply understanding the problem.
Basically just parse a list of Sue data and match it with the scanned answer.
For part 2, store an operator with every item in the scanned answer and use that for the comparison.
"""
import sys
import re
import operator as op


class SueList:
    def __init__(self, rawstr: str) -> None:
        self.__sues = []
        for line in rawstr.splitlines():
            nbrs = list(map(int, re.findall(r"\d+", line)))
            items = re.findall(r"[a-z]+:", line)
            self.__sues.append([(items[i].strip(':'), nbrs[i+1]) for i, _ in enumerate(items)])

    def get_correct_sue(self) -> int:
        mfcsam = {'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3, 'akitas': 0, 'vizslas': 0, 'goldfish': 5,
                  'trees': 3, 'cars': 2, 'perfumes': 1}
        for i, s in enumerate(self.__sues):
            for item, count in s:
                if mfcsam[item] != count:
                    break
            else:
                return i + 1  # Note that the Sue's are 1-indexed in the input
        return -1

    def get_real_correct_sue(self) -> int:
        mfcsam = {'children': (3, op.eq), 'cats': (7, op.gt), 'samoyeds': (2, op.eq), 'pomeranians': (3, op.lt),
                  'akitas': (0, op.eq), 'vizslas': (0, op.eq), 'goldfish': (5, op.lt), 'trees': (3, op.gt),
                  'cars': (2, op.eq), 'perfumes': (1, op.eq)}
        for i, s in enumerate(self.__sues):
            for item, count in s:
                if not mfcsam[item][1](count, mfcsam[item][0]):
                    break
            else:
                return i + 1
        return -1


def main() -> int:
    with open('../Inputfiles/aoc16.txt', 'r') as file:
        aunts = SueList(file.read().strip('\n'))
    print(f"Part 1: {aunts.get_correct_sue()}")
    print(f"Part 2: {aunts.get_real_correct_sue()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
