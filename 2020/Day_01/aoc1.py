"""
Simply loop through the list of numbers with 2/3 indices to check all combinations until a match is found.
"""
import sys


class ExpenseReport:
    __TARGET = 2020

    def __init__(self, rawstr: str) -> None:
        self.__numbers = [int(line) for line in rawstr.splitlines()]

    def get_2020_pair(self) -> int:
        for i in range(len(self.__numbers) - 1):
            for j in range(i + 1, len(self.__numbers)):
                if self.__numbers[i] + self.__numbers[j] == ExpenseReport.__TARGET:
                    return self.__numbers[i] * self.__numbers[j]
        return -1

    def get_2020_triplet(self) -> int:
        for i in range(len(self.__numbers) - 2):
            for j in range(i + 1, len(self.__numbers) - 1):
                if (pairsum := self.__numbers[i] + self.__numbers[j]) < ExpenseReport.__TARGET:
                    for k in range(j + 1, len(self.__numbers)):
                        if pairsum + self.__numbers[k] == ExpenseReport.__TARGET:
                            return self.__numbers[i] * self.__numbers[j] * self.__numbers[k]
        return -1


def main() -> int:
    with open('../Inputfiles/aoc1.txt', 'r') as file:
        report = ExpenseReport(file.read().strip('\n'))
    print(f"Part 1: {report.get_2020_pair()}")
    print(f"Part 2: {report.get_2020_triplet()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
