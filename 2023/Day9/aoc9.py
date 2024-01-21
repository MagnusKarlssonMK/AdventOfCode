import sys


def findnextnumber(inputlist: list[int]) -> int:
    if all(nbr == 0 for nbr in inputlist):
        return 0
    else:
        nextlevellist = [inputlist[i] - inputlist[i - 1] for i in range(1, len(inputlist))]
        return inputlist[-1] + findnextnumber(nextlevellist)


def main() -> int:
    result_p1 = 0
    result_p2 = 0
    with open('aoc9.txt', 'r') as file:
        for line in file.readlines():
            numbers = list(map(int, line.strip('\n').split()))
            result_p1 += findnextnumber(numbers)
            result_p2 += findnextnumber(list(reversed(numbers)))
    print("Part1: ", result_p1)
    print("Part2: ", result_p2)

    return 0


if __name__ == '__main__':
    sys.exit(main())
