"""
"""
import sys
from pathlib import Path
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day21.txt')


class Springdroid:
    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def __run_program(self, springcode: str) -> int:
        inst = list(map(ord, springcode))
        output = None
        for i in inst:
            self.__cpu.add_input(i)
        while True:
            val, res = self.__cpu.run_program()
            if res == IntResult.WAIT_INPUT:
                break
            elif res == IntResult.OUTPUT:
                output = val
            else:
                break
        self.__cpu.reboot()
        return output

    def get_hull_damage(self) -> int:
        program = "OR A T\nAND B T\nAND C T\nNOT T J\nAND D J\nWALK\n"
        return self.__run_program(program)

    def get_hulldamage_increased_range(self) -> int:
        program = "NOT B J\nNOT C T\nOR T J\nAND D J\nAND H J\nNOT A T\nOR T J\nRUN\n"
        return self.__run_program(program)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        droid = Springdroid(file.read().strip('\n'))
    print(f"Part 1: {droid.get_hull_damage()}")
    print(f"Part 2: {droid.get_hulldamage_increased_range()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
