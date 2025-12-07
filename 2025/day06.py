"""
2025 day 6 - Trash Compactor
"""

import time
from math import prod
from pathlib import Path


class InputData:
    def __init__(self, s: str) -> None:
        self.__lines = s.splitlines()
        self.__operations = self.__lines.pop().split()

    def get_p1(self) -> int:
        numbers = [
            list(z) for z in zip(*[[*map(int, line.split())] for line in self.__lines])
        ]

        total = 0
        for i, o in enumerate(self.__operations):
            if o == "+":
                total += sum(numbers[i])
            else:
                total += prod(numbers[i])
        return total

    def get_p2(self) -> int:
        numbers_chars_transposed = [
            list(z) for z in zip(*[list(line) for line in self.__lines])
        ]
        # Extra padding added for the next step
        numbers_chars_transposed.append([" ", " ", " ", " "])
        total = 0
        op_idx = 0
        number_buffer = []
        for col in numbers_chars_transposed:
            if all([c == " " for c in col]):
                if self.__operations[op_idx] == "+":
                    total += sum(number_buffer)
                else:
                    total += prod(number_buffer)
                number_buffer = []
                op_idx += 1
            else:
                number_buffer.append(int("".join(col)))
        return total


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day06.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
