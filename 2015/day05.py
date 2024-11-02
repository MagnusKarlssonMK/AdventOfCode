"""
Part 1: Just scan each string to see if they follow the rules, quit immediately if one of the naughty words are found.
Part 2: First search each string to check the second rule for repeated with one distance, if not found then quit, else
continue to check the first rule by using the python 'count' function which counts non-overlapping occurrences.
"""
import time
from pathlib import Path


class SantaString:
    def __init__(self, string: str) -> None:
        self.__string = string

    def is_nice(self, newrules: bool) -> bool:
        if not newrules:
            vowels = 0
            previous = ''
            twice_in_a_row = False
            for c in self.__string:
                if previous + c in ('ab', 'cd', 'pq', 'xy'):
                    return False
                if previous == c:
                    twice_in_a_row = True
                if c in ('a', 'e', 'i', 'o', 'u'):
                    vowels += 1
                previous = c
            return twice_in_a_row and vowels >= 3
        else:
            repeated_found = False
            for i in range(2, len(self.__string)):
                if self.__string[i] == self.__string[i - 2]:
                    repeated_found = True
                    break
            if not repeated_found:
                return False
            for i in range(len(self.__string) - 1):
                if self.__string.count(self.__string[i: i + 2]) > 1:
                    return True
            return False


class SantaText:
    def __init__(self, rawstr: str) -> None:
        self.__strings = [SantaString(line) for line in rawstr.splitlines()]

    def get_nice_count(self, new_rules: bool = False) -> int:
        return sum([1 if s.is_nice(new_rules) else 0 for s in self.__strings])


def main(aoc_input: str) -> None:
    textfile = SantaText(aoc_input)
    print(f"Part 1: {textfile.get_nice_count()}")
    print(f"Part 1: {textfile.get_nice_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
