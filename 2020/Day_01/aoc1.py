"""
Simply loop through the list of numbers with 2/3 indices to check all combinations until a match is found.
"""
import sys


def find2020pair(numbers: list[int]) -> int:
    for i in range(len(numbers) - 1):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == 2020:
                return numbers[i] * numbers[j]
    return -1


def find2020triad(numbers: list[int]) -> int:
    for i in range(len(numbers) - 2):
        for j in range(i + 1, len(numbers) - 1):
            if (v := numbers[i] + numbers[j]) > 2020:
                continue
            for k in range(j + 1, len(numbers)):
                if v + numbers[k] == 2020:
                    return numbers[i] * numbers[j] * numbers[k]
    return -1


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        numbers = list(map(int, file.read().strip('\n').splitlines()))
    print("Part 1:", find2020pair(numbers))
    print("Part 2:", find2020triad(numbers))
    return 0


if __name__ == "__main__":
    sys.exit(main())
