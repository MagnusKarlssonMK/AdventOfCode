"""
2023 day 4 - Scratchcards
"""

import time
from pathlib import Path


class Card:
    def __init__(self, s: str) -> None:
        all_numbers = s.split(": ")[1]
        parts = all_numbers.split(" | ")
        winning_numbers = set([int(p) for p in parts[0].split()])
        draw_numbers = set([int(c) for c in parts[1].split()])
        self.wincount = len(winning_numbers & draw_numbers)
        self.score = 0 if self.wincount <= 0 else pow(2, self.wincount - 1)


class InputData:
    def __init__(self, s: str) -> None:
        self.__scratchcards = [Card(line) for line in s.splitlines()]

    def solve_part1(self) -> int:
        return sum([card.score for card in self.__scratchcards])

    def solve_part2(self) -> int:
        copylist = [1 for _ in range(0, len(self.__scratchcards))]
        for i, card in enumerate(self.__scratchcards):
            for j in range(1, card.wincount + 1):
                copylist[i + j] += copylist[i]
        return sum(copylist)


def main(aoc_input: str) -> None:
    i = InputData(aoc_input)
    print(f"Part 1: {i.solve_part1()}")
    print(f"Part 2: {i.solve_part2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2023/day04.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
