"""
This intcode program halts after each coordinate, so we need to keep rebooting it after every run.
"""
import time
from pathlib import Path
from intcode import Intcode, IntResult


class TractorBeam:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def __get_drone_status(self, x: int, y: int) -> int:
        while True:
            self.__cpu.add_input(x)
            self.__cpu.add_input(y)
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                self.__cpu.reboot()
                return val
            else:
                break
        self.__cpu.reboot()
        return 0

    def get_nbr_affected_points(self) -> int:
        return sum([self.__get_drone_status(x, y) for x in range(50) for y in range(50)])

    def get_square_val(self) -> int:
        x = y = 0
        while not self.__get_drone_status(x + 99, y):
            y += 1
            while not self.__get_drone_status(x, y + 99):
                x += 1
        return x * 10000 + y


def main(aoc_input: str) -> None:
    tractorbeam = TractorBeam(aoc_input)
    print(f"Part 1: {tractorbeam.get_nbr_affected_points()}")
    print(f"Part 2: {tractorbeam.get_square_val()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day19.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
