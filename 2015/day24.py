"""
Apparently this is a bit of a trick problem, since it turns out that the input is set up in a way that there is no need
to check if the remaining weights can be split evenly once a combination for the first crate has been found. So while I
first started thinking of rather wild recursive algorithms to traverse through, what's really needed is just to find
the list of the shortest combinations for the first crate, and then find the one whose product ('quantum entanglement')
is the smallest.
"""
import time
from pathlib import Path
from itertools import combinations
from math import prod


class Packages:
    def __init__(self, rawstr: str) -> None:
        self.__weights = list(map(int, rawstr.splitlines()))
        self.__totalweight: int = sum(self.__weights)

    def get_first_qe(self, nbr_groups: int = 3) -> int:
        groupsize = self.__totalweight // nbr_groups
        firstgroup_combos: list[int] = []
        for count in range(1, len(self.__weights) - (nbr_groups - 1)):
            for comb in combinations(self.__weights, count):
                if sum(comb) == groupsize:
                    firstgroup_combos.append(prod(comb))
            if firstgroup_combos:
                break
        return sorted(firstgroup_combos)[0]


def main(aoc_input: str) -> None:
    packages = Packages(aoc_input)
    print(f"Part 1: {packages.get_first_qe()}")
    print(f"Part 2: {packages.get_first_qe(4)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day24.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
