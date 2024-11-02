"""
Using 'summed-area table' algorithm. (https://en.wikipedia.org/wiki/Summed-area_table)
"""
import time
from pathlib import Path


class FuelCellGrid:
    __GRIDSIZE = 300

    def __init__(self, serialnbr: int) -> None:
        self.__serialnbr = serialnbr
        self.__grid = [[0 for _ in range(FuelCellGrid.__GRIDSIZE + 2)] for _ in range(FuelCellGrid.__GRIDSIZE + 2)]
        for y in range(1, FuelCellGrid.__GRIDSIZE + 1):
            for x in range(1, FuelCellGrid.__GRIDSIZE + 1):
                rackid = x + 10
                power = str((rackid * y + self.__serialnbr) * rackid)
                if len(power) >= 3:
                    power = int(power[-3]) - 5
                else:
                    power = -5
                self.__grid[y][x] = power + self.__grid[y - 1][x] + self.__grid[y][x - 1] - self.__grid[y - 1][x - 1]

    def __get_best_fuelcell(self, fuelcell_size: int) -> tuple[int, int, int]:  # [x, y, power]
        max_power = 0
        max_fuelcell_x, max_fuelcell_y = 0, 0
        for y in range(1, FuelCellGrid.__GRIDSIZE + 1 - fuelcell_size):
            for x in range(1, FuelCellGrid.__GRIDSIZE + 1 - fuelcell_size):
                power = (self.__grid[y - 1][x - 1] + self.__grid[y + fuelcell_size - 1][x + fuelcell_size - 1] -
                         self.__grid[y + fuelcell_size - 1][x - 1] - self.__grid[y - 1][x + fuelcell_size - 1])
                if power > max_power:
                    max_power = power
                    max_fuelcell_x, max_fuelcell_y = x, y
        return max_fuelcell_x, max_fuelcell_y, max_power

    def get_maxpower_coord(self) -> str:
        x, y, _ = self.__get_best_fuelcell(3)
        return f"{x},{y}"

    def get_advanced_maxpower_coord(self) -> str:
        max_power = 0
        max_fuelcell_x, max_fuelcell_y, max_fuelcell_size = 0, 0, 0
        for size in range(1, FuelCellGrid.__GRIDSIZE + 1):
            x, y, power = self.__get_best_fuelcell(size)
            if power > max_power:
                max_power = power
                max_fuelcell_x, max_fuelcell_y, max_fuelcell_size = x, y, size
        return f"{max_fuelcell_x},{max_fuelcell_y},{max_fuelcell_size}"


def main(aoc_input: str) -> None:
    grid = FuelCellGrid(int(aoc_input))
    print(f"Part 1: {grid.get_maxpower_coord()}")
    print(f"Part 2: {grid.get_advanced_maxpower_coord()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
