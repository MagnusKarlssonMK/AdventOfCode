"""
Just a simple recursive function to generate the lines until a line of zeroes shows up.
Surprisingly simple part 2, basically just to reverse the input data and run the same function.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2023/day09.txt')


def findnextnumber(nbrs: list[int]) -> int:
    if all(nbr == 0 for nbr in nbrs):
        return 0
    else:
        nextlevellist = [nbrs[i] - nbrs[i - 1] for i in range(1, len(nbrs))]
        return nbrs[-1] + findnextnumber(nextlevellist)


def main() -> int:
    result_p1 = 0
    result_p2 = 0
    with open(INPUT_FILE, 'r') as file:
        for line in file.read().strip('\n').splitlines():
            numbers = list(map(int, line.split()))
            result_p1 += findnextnumber(numbers)
            result_p2 += findnextnumber(list(reversed(numbers)))
    print(f"Part1: {result_p1}")
    print(f"Part2: {result_p2}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
