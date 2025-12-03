"""
Direct translation of Rust solution
"""

import math
import time
from pathlib import Path


def get_invalid(v1: str, v2: str) -> int:
    start_id = int(v1)
    stop_id = int(v2)
    nbrof_parts = 2

    invalid = 0
    next_part = (
        int(v1[0 : len(v1) // nbrof_parts])
        if len(v1) % nbrof_parts == 0
        else int(pow(10, (len(v1) // nbrof_parts)))
    )

    while True:
        nbrof_part_digits = 1 + int(math.log10(abs(next_part)))
        candidate_id = next_part + next_part * int(pow(10, nbrof_part_digits))
        if candidate_id > stop_id:
            break
        if candidate_id >= start_id:
            invalid += candidate_id
        next_part += 1

    return invalid


def get_multiple_invalid(v1: str, v2: str) -> int:
    start_id = int(v1)
    stop_id = int(v2)
    nbrof_parts = 2
    invalid = set()

    while nbrof_parts <= len(v2):
        next_part = (
            int(v1[0 : len(v1) // nbrof_parts])
            if len(v1) % nbrof_parts == 0
            else int(pow(10, len(v1) // nbrof_parts))
        )

        while True:
            nbrof_part_digits = 1 + int(math.log10(abs(next_part)))
            candidate_id = sum(
                [
                    next_part * int(pow(10, p * nbrof_part_digits))
                    for p in range(nbrof_parts)
                ]
            )
            if candidate_id > stop_id:
                break
            if candidate_id >= start_id:
                invalid.add(candidate_id)
            next_part += 1
        nbrof_parts += 1

    return sum(invalid)


class InputData:
    def __init__(self, s: str) -> None:
        self.__rotations = [
            (v[0], v[1]) for v in [r.split("-", 1) for r in s.split(",")]
        ]

    def get_p1(self) -> int:
        return sum([get_invalid(v1, v2) for (v1, v2) in self.__rotations])

    def get_p2(self) -> int:
        return sum([get_multiple_invalid(v1, v2) for (v1, v2) in self.__rotations])


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day02.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
