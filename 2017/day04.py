"""
Part 1: Simply make a set out of the words in every line and compare the lengths - if there are repeated words, the
length of the set will be smaller than the length of the list.

Part 2: For each line, make a set of characters for every word, and check all combinations of those words to see if
there is any overlap.
"""
import sys
from pathlib import Path
from itertools import combinations

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2017/day04.txt')


class PassphraseList:
    def __init__(self, rawstr: str) -> None:
        self.__pwds = [w.split() for w in [line for line in rawstr.splitlines()]]

    def get_valid_count(self, check_anagrams: bool = False) -> int:
        if not check_anagrams:
            return sum([1 for line in self.__pwds if len(line) == len(set(line))])
        else:
            result = 0
            for line in self.__pwds:
                words = [set(w) for w in line]
                for w1, w2 in combinations(words, 2):
                    if w1 == w2:
                        break
                else:
                    result += 1
            return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        pwds = PassphraseList(file.read().strip('\n'))
    print(f"Part 1: {pwds.get_valid_count()}")
    print(f"Part 2: {pwds.get_valid_count(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
