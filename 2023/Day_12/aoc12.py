"""
Memoized recursive solution, using the functools cache.
"""
import sys
from functools import lru_cache


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


def main() -> int:
    totalsum_p1 = 0
    totalsum_p2 = 0

    with open("../Inputfiles/aoc12.txt", "r") as file:
        for line in file.read().strip('\n').splitlines():
            springs, keys = line.split()
            keylist_p1 = [int(char) for char in keys.split(",")]
            keylist_p2 = list(keylist_p1) * 5
            springs_p1 = springs.lstrip(".")
            springs_p2 = "?".join([springs] * 5).lstrip(".")
            totalsum_p1 += calculatecombinations(springs_p1, (*keylist_p1,))
            totalsum_p2 += calculatecombinations(springs_p2, (*keylist_p2,))

    print("Part1:", totalsum_p1)
    print("Part2:", totalsum_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
