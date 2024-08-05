"""
This intcode program halts after each coordinate, so we need to keep rebooting it after every run.
"""
import sys
from pathlib import Path
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day19.txt')


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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        tractorbeam = TractorBeam(file.read().strip())
    print(f"Part 1: {tractorbeam.get_nbr_affected_points()}")
    print(f"Part 2: {tractorbeam.get_square_val()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
