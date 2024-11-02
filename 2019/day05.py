"""
"""
import time
from pathlib import Path
from intcode import Intcode, IntResult


class Computer:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def get_diagnostic_code(self, inputval: int) -> int:
        self.__cpu.reboot()
        self.__cpu.add_input(inputval)
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.OUTPUT:
                if val != 0:
                    return val
            else:
                break
        return -1


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_diagnostic_code(1)}")
    print(f"Part 2: {computer.get_diagnostic_code(5)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
