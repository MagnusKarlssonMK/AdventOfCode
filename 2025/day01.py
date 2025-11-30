import time
from pathlib import Path


class Placeholder:
    def __init__(self, rawstr: str) -> None:
        pass

    def get_p1(self) -> int:
        return 1

    def get_p2(self) -> int:
        return 2


def main(aoc_input: str) -> None:
    p = Placeholder(aoc_input)
    print(f"Part 1: {p.get_p1()}")
    print(f"Part 2: {p.get_p2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2024/day06.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
