"""
Just a simple recursive function to generate the lines until a line of zeroes shows up.
Surprisingly simple part 2, basically just to reverse the input data and run the same function.
"""

import time
from pathlib import Path


def findnextnumber(nbrs: list[int]) -> int:
    if all(nbr == 0 for nbr in nbrs):
        return 0
    else:
        nextlevellist = [nbrs[i] - nbrs[i - 1] for i in range(1, len(nbrs))]
        return nbrs[-1] + findnextnumber(nextlevellist)


def get_numbers(s: str) -> tuple[int, int]:
    result_p1 = 0
    result_p2 = 0
    for line in s.splitlines():
        numbers = list(map(int, line.split()))
        result_p1 += findnextnumber(numbers)
        result_p2 += findnextnumber(list(reversed(numbers)))
    return result_p1, result_p2


def main(aoc_input: str) -> None:
    p1, p2 = get_numbers(aoc_input)
    print(f"Part1: {p1}")
    print(f"Part2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], "AdventOfCode-Input")
    INPUT_FILE = Path(ROOT_DIR, "2023/day09.txt")

    start_time = time.perf_counter()
    with open(INPUT_FILE, "r") as file:
        main(file.read().strip("\n"))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
