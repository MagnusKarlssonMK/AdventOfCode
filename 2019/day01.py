"""
Very basic calculation for Part 1. Include a bit of recursion for Part 2.
"""
import sys


def calc_mass(mass: int, countfuel: bool = False) -> int:
    fuel_own_mass = max(0, (mass // 3) - 2)
    if fuel_own_mass == 0 or not countfuel:
        return fuel_own_mass
    return fuel_own_mass + calc_mass(fuel_own_mass, countfuel)


def main() -> int:
    with open("../Inputfiles/aoc1.txt", 'r') as file:
        nbrs = list(map(int, file.read().strip('\n').splitlines()))
    print("Part 1:", sum([calc_mass(nbr) for nbr in nbrs]))
    print("Part 2:", sum([calc_mass(nbr, True) for nbr in nbrs]))
    return 0


if __name__ == "__main__":
    sys.exit((main()))
