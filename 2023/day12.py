"""
Memoized recursive solution, using the functools cache.
"""
import sys
from pathlib import Path
from functools import lru_cache

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day12.txt')


@lru_cache()
def calculatecombinations(springstring: str, inputkeys: tuple[int]) -> int:
    if not inputkeys:  # empty list
        return int("#" not in springstring)  # return 1 if there are no '#' in the string, 0 otherwise
    springlength = len(springstring)
    keylength = inputkeys[0]
    if springlength - sum(inputkeys) - len(inputkeys) + 1 < 0:
        return 0
    issubstrings = any(springstring[x] == "." for x in range(keylength))
    if springlength == keylength:
        return 0 if issubstrings else 1
    can_use = not issubstrings and (springstring[keylength] != "#")
    if springstring[0] == "#":
        return calculatecombinations(springstring[keylength + 1:].lstrip("."), tuple(inputkeys[1:])) if can_use else 0
    skip = calculatecombinations(springstring[1:].lstrip("."), inputkeys)
    if not can_use:
        return skip
    return skip + calculatecombinations(springstring[keylength + 1:].lstrip("."), tuple(inputkeys[1:]))


class SpringRecord:
    def __init__(self, rawstr: str) -> None:
        self.__rows = []
        for line in rawstr.splitlines():
            springs, keystr = line.split()
            keys = [int(c) for c in keystr.split(',')]
            self.__rows.append((springs, keys))

    def get_arrangement_sum(self, foldcount: int = 0) -> int:
        retval = 0
        for springs, keys in self.__rows:
            tmpkeys = list(keys) if foldcount == 0 else list(keys) * foldcount
            tmpsprings = springs.lstrip('.') if foldcount == 0 else '?'.join([springs] * foldcount).lstrip('.')
            retval += calculatecombinations(tmpsprings, (*tmpkeys,))
        return retval


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        myrecord = SpringRecord(file.read().strip('\n'))
    print(f"Part 1: {myrecord.get_arrangement_sum()}")
    print(f"Part 2: {myrecord.get_arrangement_sum(5)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
