"""
For part 2, we actually only need to compare the first element of the first window with the last element of the
second window, since all the elements in between are shared by both. So by making use of that logic, the answer
for both part 1 and 2 can be calculated with one function, taking the window length as an input.
"""
import time
from pathlib import Path


class Report:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = list(map(int, rawstr.splitlines()))

    def count_depth_increase(self, windowsize: int) -> int:
        return sum([1 for i in range(windowsize, len(self.__nbrs)) if self.__nbrs[i] > self.__nbrs[i - windowsize]])


def main(aoc_input: str) -> None:
    report = Report(aoc_input)
    print(f"Part 1: {report.count_depth_increase(1)}")
    print(f"Part 2: {report.count_depth_increase(3)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
