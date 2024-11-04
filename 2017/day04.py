"""
Part 1: Simply make a set out of the words in every line and compare the lengths - if there are repeated words, the
length of the set will be smaller than the length of the list.

Part 2: For each line, make a set of characters for every word, and check all combinations of those words to see if
there is any overlap.
"""
import time
from pathlib import Path
from itertools import combinations


class PassphraseList:
    def __init__(self, rawstr: str) -> None:
        self.__pwds = [w.split() for w in [line for line in rawstr.splitlines()]]

    def get_valid_count(self, check_anagrams: bool = False) -> int:
        if not check_anagrams:
            return sum([1 for line in self.__pwds if len(line) == len(set(line))])
        else:
            result = 0
            for line in self.__pwds:
                sortedwords = [''.join(sorted(word)) for word in line]
                if len(sortedwords) == len(set(sortedwords)):
                    result += 1
            return result


def main(aoc_input: str) -> None:
    pwds = PassphraseList(aoc_input)
    print(f"Part 1: {pwds.get_valid_count()}")
    print(f"Part 2: {pwds.get_valid_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
