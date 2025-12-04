"""
2025 day 4 - Printing Department
"""

import time
from pathlib import Path

# Just a placeholder for now.
#
# I can't be bothered to transfer this solution right now; saving it for when I've figured out
# how to make a common utility library for grid/point work in python.


class InputData:
    def __init__(self, s: str) -> None:
        self.__banks = [line for line in s.splitlines()]

    def get_p1(self) -> int:
        return 1

    def get_p2(self) -> int:
        return 2


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day04.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
