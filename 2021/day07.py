"""
For part 1, the optimal distance will be on the median value, so simply calculate this using the median function
from statistics module, and then determine the total fuel cost at that value.
For part 2, the optimal distance will rather be on the mean value, so similar approach to part 1, but also check
the surrounding values to be safe against rounding errors.
"""
import time
from pathlib import Path
import statistics


class CrabArmy:
    def __init__(self, rawstr: str) -> None:
        self.__crabs = sorted(list(map(int, rawstr.split(','))))

    def get_calibration_cost(self, scaling_fuel_rate: bool = False) -> int:
        if not scaling_fuel_rate:
            # Part 1
            calnbr = int(statistics.median(self.__crabs))
            return sum([abs(crab - calnbr) for crab in self.__crabs])
        else:
            # Part 2
            distance = int(statistics.mean(self.__crabs))
            cost = min(self.__scaling_cost(distance),
                       self.__scaling_cost(distance - 1),
                       self.__scaling_cost(distance + 1))
            return cost

    def __scaling_cost(self, calnbr) -> int:
        return sum([d * (d + 1) // 2 for d in [abs(crab - calnbr) for crab in self.__crabs]])


def main(aoc_input: str) -> None:
    crabs = CrabArmy(aoc_input)
    print(f"Part 1: {crabs.get_calibration_cost()}")
    print(f"Part 2: {crabs.get_calibration_cost(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day07.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
