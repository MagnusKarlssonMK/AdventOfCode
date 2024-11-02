"""
Part 1: Simply parse the input a store it in a list sorted by total calories, and the largest value is the answer.
Part 2: From the same list, just take the sum of the top three.
"""
import time
from pathlib import Path


class Elf:
    def __init__(self, calories: list[int]) -> None:
        self.calories = calories
        self.totalcalories = sum(calories)

    def __str__(self):
        return f"{self.calories}"


class ElfGroup:
    def __init__(self, rawstr: str) -> None:
        blocks = rawstr.split('\n\n')
        self.__elfs = sorted([Elf(list(map(int, elf.splitlines()))) for elf in blocks],
                             key=lambda tot: tot.totalcalories, reverse=True)

    def get_maxcal(self) -> int:
        return self.__elfs[0].totalcalories

    def get_topthree(self) -> int:
        return sum([self.__elfs[num].totalcalories for num in range(3)])


def main(aoc_input: str) -> None:
    elfgroup = ElfGroup(aoc_input)
    print(f"Part1: {elfgroup.get_maxcal()}")
    print(f"Part2: {elfgroup.get_topthree()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
