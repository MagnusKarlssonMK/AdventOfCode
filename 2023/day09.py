"""
Just a simple recursive function to generate the lines until a line of zeroes shows up.
Surprisingly simple part 2, basically just to reverse the input data and run the same function.
"""
import sys


def findnextnumber(nbrs: list[int]) -> int:
    if all(nbr == 0 for nbr in nbrs):
        return 0
    else:
        nextlevellist = [nbrs[i] - nbrs[i - 1] for i in range(1, len(nbrs))]
        return nbrs[-1] + findnextnumber(nextlevellist)


def main() -> int:
    result_p1 = 0
    result_p2 = 0
    with open('../Inputfiles/aoc9.txt', 'r') as file:
        for line in file.read().strip('\n').splitlines():
            numbers = list(map(int, line.split()))
            result_p1 += findnextnumber(numbers)
            result_p2 += findnextnumber(list(reversed(numbers)))
    print("Part1:", result_p1)
    print("Part2:", result_p2)
    return 0


if __name__ == '__main__':
    sys.exit(main())
