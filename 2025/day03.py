"""
2025 day 03 - Lobby
"""

import time
from pathlib import Path


class InputData:
    def __init__(self, s: str) -> None:
        self.__banks = [line for line in s.splitlines()]

    def __get_jolt(self, nbrof_digits: int) -> int:
        total = 0
        for bank in self.__banks:
            new_number = 0
            start_idx = 0
            for digit_idx in reversed(range(nbrof_digits)):
                next_digit = 0
                i = start_idx
                for x in range(i, len(bank) - digit_idx):
                    new_digit = int(bank[x])
                    if next_digit < new_digit:
                        next_digit = new_digit
                        start_idx = x + 1
                        if next_digit == 9:
                            break
                new_number += next_digit * pow(10, digit_idx)
            total += new_number
        return total

    def get_p1(self) -> int:
        return self.__get_jolt(2)

    def get_p2(self) -> int:
        return self.__get_jolt(12)


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day03.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
