"""
For part 1, the optimal distance will be on the median value, so simply calculate this using the median function
from statistics module, and then determine the total fuel cost at that value.
For part 2, the optimal distance will rather be on the mean value, so similar approach to part 1, but also check
the surrounding values to be safe against rounding errors.
"""
import sys
import statistics


def calibrationcost_p1(nbrlist: list[int], calnbr: int) -> int:
    return sum([abs(nbr - calnbr) for nbr in nbrlist])


def calibrationcost_p2(nbrlist: list[int], calnbr: int) -> int:
    return sum([d * (d + 1) // 2 for d in [abs(nbr - calnbr) for nbr in nbrlist]])


def main() -> int:
    with open('../Inputfiles/aoc7.txt', 'r') as file:
        nbrs = sorted(list(map(int, file.read().strip('\n').split(','))))
        print("Part 1: ", calibrationcost_p1(nbrs, int(statistics.median(nbrs))))
        p2_dist = int(statistics.mean(nbrs))
        p2 = min(calibrationcost_p2(nbrs, p2_dist), calibrationcost_p2(nbrs, p2_dist - 1),
                 calibrationcost_p2(nbrs, p2_dist + 1))
        print("Part 2: ", p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
