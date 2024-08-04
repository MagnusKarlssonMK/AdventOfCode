"""
Build a computer class to hold the data and run the program, taking the first two values as input.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day02.txt')


class Intcode:
    __CORRECT_OUTPUT = 19690720

    def __init__(self, rawstr: str) -> None:
        self.__program = [int(nbr) for nbr in rawstr.split(',')]

    def __run_program(self, pos1: int, pos2: int) -> int:
        program = list(self.__program)
        program[1] = pos1
        program[2] = pos2
        head = 0
        while 0 <= head < len(program):
            match program[head]:
                case 1:
                    program[program[head + 3]] = program[program[head + 1]] + program[program[head + 2]]
                    head += 4
                case 2:
                    program[program[head + 3]] = program[program[head + 1]] * program[program[head + 2]]
                    head += 4
                case 99:
                    break
        return program[0]

    def get_alarmstate(self) -> int:
        return self.__run_program(12, 2)

    def find_correct_inputs(self) -> int:
        for noun in range(100):
            for verb in range(100):
                if self.__run_program(noun, verb) == Intcode.__CORRECT_OUTPUT:
                    return noun * 100 + verb
        return -1


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        computer = Intcode(file.read().strip('\n'))
    print(f"Part 1: {computer.get_alarmstate()}")
    print(f"Part 2: {computer.find_correct_inputs()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
