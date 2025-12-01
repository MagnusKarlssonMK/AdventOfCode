import time
from pathlib import Path


class InputData:
    def __init__(self, s: str) -> None:
        self.__rotations = [
            int(line[1:]) if line[0] == "R" else -int(line[1:])
            for line in s.splitlines()
        ]

    def get_p1(self) -> int:
        zero_count = 0
        dial = 50
        for v in self.__rotations:
            dial = (dial + v) % 100
            if dial == 0:
                zero_count += 1
        return zero_count

    def get_p2(self) -> int:
        zero_count = 0
        dial = 50
        for v in self.__rotations:
            if v >= 0:
                zero_count += (dial + v) // 100
            elif dial == 0:
                zero_count += abs(v) // 100
            else:
                zero_count += (100 - dial + abs(v)) // 100
            dial = (dial + v) % 100
        return zero_count


def main(aoc_input: str) -> None:
    p = InputData(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2025/day01.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
