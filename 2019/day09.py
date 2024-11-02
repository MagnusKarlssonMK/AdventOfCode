"""
"""
import time
from pathlib import Path
from intcode import Intcode, IntResult


class Boost:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def get_keycode(self, startval: int = 1) -> int:
        self.__cpu.add_input(startval)
        result = 0
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.OUTPUT:
                result = val
            else:
                break
        self.__cpu.reboot()
        return result


def main(aoc_input: str) -> None:
    boost = Boost(aoc_input)
    print(f"Part 1: {boost.get_keycode()}")
    print(f"Part 2: {boost.get_keycode(2)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
