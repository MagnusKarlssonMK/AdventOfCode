"""
Mostly an exercise in string parsing, checking the content after that is pretty straightforward.
"""
import sys


def validatepassword_1(r: list[int], c: str, pwd: str) -> bool:
    return r[0] <= pwd.count(c) <= r[1]


def validatepassword_2(r: list[int], c: str, pwd: str) -> bool:
    count = 0
    if len(pwd) >= r[0]:
        if pwd[r[0] - 1] == c:
            count += 1
        if len(pwd) >= r[1] and pwd[r[1] - 1] == c:
            count += 1
    return count == 1


def main() -> int:
    with open('../Inputfiles/aoc2.txt', 'r') as file:
        lines = [[list(map(int, a[0].split('-'))), a[1].strip(':'), a[2]]
                 for a in [line.split() for line in file.read().strip('\n').splitlines()]]
    print("Part 1:", sum([1 for line in lines if validatepassword_1(*line)]))
    print("Part 2:", sum([1 for line in lines if validatepassword_2(*line)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
