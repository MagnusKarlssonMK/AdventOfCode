"""
Very basic calculation for Part 1. Include a bit of recursion for Part 2.
"""
import time
from pathlib import Path


def calc_mass(mass: int, countfuel: bool = False) -> int:
    fuel_own_mass = max(0, (mass // 3) - 2)
    if fuel_own_mass == 0 or not countfuel:
        return fuel_own_mass
    return fuel_own_mass + calc_mass(fuel_own_mass, countfuel)


def main(aoc_input: str) -> None:
    nbrs = list(map(int, aoc_input.splitlines()))
    print("Part 1:", sum([calc_mass(nbr) for nbr in nbrs]))
    print("Part 2:", sum([calc_mass(nbr, True) for nbr in nbrs]))


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day01.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
