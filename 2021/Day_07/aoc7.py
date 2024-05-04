"""
For part 1, the optimal distance will be on the median value, so simply calculate this using the median function
from statistics module, and then determine the total fuel cost at that value.
For part 2, the optimal distance will rather be on the mean value, so similar approach to part 1, but also check
the surrounding values to be safe against rounding errors.
"""
import sys
import statistics


class CrabArmy:
    def __init__(self, rawstr: str):
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


def main() -> int:
    with open('../Inputfiles/aoc7.txt', 'r') as file:
        crabs = CrabArmy(file.read().strip('\n'))
    print(f"Part 1: {crabs.get_calibration_cost()}")
    print(f"Part 2: {crabs.get_calibration_cost(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
