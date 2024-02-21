import sys
import re


def main() -> int:
    with open('../Inputfiles/aoc4.txt', 'r') as file:
        lines = [list(map(int, re.split('[,-]', line))) for line in file.read().strip('\n').splitlines()]

    result_p1 = sum([1 for a, b, c, d in lines if a <= c <= d <= b or c <= a <= b <= d])
    result_p2 = sum([1 for a, b, c, d in lines if a <= d and c <= b])

    print("Part1:", result_p1)
    print("Part2:", result_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
