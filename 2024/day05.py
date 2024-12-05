import time
from pathlib import Path


class SafetyManual:
    def __init__(self, rawstr: str) -> None:
        rules, updates = rawstr.split("\n\n")
        self.__rules: set[tuple[int, int]] = set([(int(left), int(right)) for left, right in
                                                  [line.split('|') for line in rules.splitlines()]])
        self.__updates: list[list[int]] = [[int(n) for n in line.split(',')]
                                           for line in updates.splitlines()]

    def get_order_scores(self) -> tuple[int, int]:
        p1 = p2 = 0
        for update in self.__updates:
            sorted_update = sorted(update, key=lambda n1: 
                                   sum([(n2, n1) in self.__rules for n2 in update]))
            if update == sorted_update:
                p1 += update[len(update) // 2]
            else:
                p2 += sorted_update[len(update) // 2]
        return p1, p2


def main(aoc_input: str) -> None:
    manual = SafetyManual(aoc_input)
    p1, p2 = manual.get_order_scores()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
