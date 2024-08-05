"""
"""
import sys
from pathlib import Path
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day05.txt')


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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        computer = Computer(file.read().strip('\n'))
    print(f"Part 1: {computer.get_diagnostic_code(1)}")
    print(f"Part 2: {computer.get_diagnostic_code(5)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
