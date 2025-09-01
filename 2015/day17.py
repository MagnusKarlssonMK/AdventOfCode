"""
Simply use the 'combinations' function to generate combinations for all numbers of containers (1-max), and find the
ones matching the volume. Also store the length of the matches in a list to use for part 2, where that list is
sorted, and we then count number of entries for that length.
"""
import time
from pathlib import Path
from itertools import combinations


class ContainerList:
    def __init__(self, rawstr: str) -> None:
        self.__containers = [int(n) for n in rawstr.splitlines()]
        self.__combinations: list[int] = []

    def get_combination_count(self, amount: int = 150) -> int:
        count = 0
        for comb_count in range(1, len(self.__containers) + 1):
            for c in combinations(self.__containers, comb_count):
                if sum(c) == amount:
                    self.__combinations.append(len(c))
                    count += 1
        return count

    def get_min_combination_count(self) -> int:
        sortlist = sorted(self.__combinations)
        return sortlist.count(sortlist[0])


def main(aoc_input: str) -> None:
    containers = ContainerList(aoc_input)
    print(f"Part 1: {containers.get_combination_count()}")
    print(f"Part 2: {containers.get_min_combination_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
