"""
"""
import sys
from pathlib import Path
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day09.txt')


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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        boost = Boost(file.read().strip('\n'))
    print(f"Part 1: {boost.get_keycode()}")
    print(f"Part 2: {boost.get_keycode(2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
