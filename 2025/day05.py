"""
2025 day 5 - Cafeteria
"""

import time
from pathlib import Path


class InputData:
    def __init__(self, s: str) -> None:
        blocks = s.split("\n\n")
        self.__fresh_id_ranges = [
            (int(r[0]), int(r[1]))
            for r in [line.split("-") for line in blocks[0].splitlines()]
        ]
        self.__available_ids = [int(line) for line in blocks[1].splitlines()]

    def get_p1(self) -> int:
        total = 0
        for a in self.__available_ids:
            for r0, r1 in self.__fresh_id_ranges:
                if a in range(r0, r1 + 1):
                    total += 1
                    break
        return total

    def get_p2(self) -> int:
        processed = []
        queue = self.__fresh_id_ranges.copy()
        while queue:
            r0, r1 = queue.pop(0)
            for i, (p0, p1) in enumerate(processed):
                if (
                    r0 in range(p0, p1 + 1)
                    or r1 in range(p0, p1 + 1)
                    or p0 in range(r0, r1 + 1)
                ):
                    processed.pop(i)
                    queue.append((min(p0, r0), max(p1, r1)))
                    break
            else:
                processed.append((r0, r1))
        return sum([1 + p1 - p0 for p0, p1 in processed])


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day05.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
