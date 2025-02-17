"""
Quite straightforward, basically just store the program and then run it by having a stack-pointer walking through
the program according to the instructions.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    instr: str
    attr1: str
    attr2: str = None


class Computer:
    def __init__(self, rawstr: str) -> None:
        self.__program = [Instruction(*[w.strip(',') for w in line.split()]) for line in rawstr.splitlines()]
        self.__program_end = len(self.__program)
        self.__registers: dict[str: int] = {'a': 0, 'b': 0}

    def __run_program(self) -> None:
        """Runs the program. Ends when stack pointer goes out of range of the program."""
        s_p = 0
        while s_p < self.__program_end:
            nextinstr = self.__program[s_p]
            match nextinstr.instr:
                case 'hlf':     # 'Half'
                    self.__registers[nextinstr.attr1] //= 2
                case 'tpl':     # 'Triple'
                    self.__registers[nextinstr.attr1] *= 3
                case 'inc':     # 'Increment'
                    self.__registers[nextinstr.attr1] += 1
                case 'jmp':     # 'Jump'
                    s_p += int(nextinstr.attr1)
                    continue
                case 'jie':     # 'Jump if even'
                    if self.__registers[nextinstr.attr1] % 2 == 0:
                        s_p += int(nextinstr.attr2)
                        continue
                case 'jio':     # 'Jump if one' (NOT jump if odd...)
                    if self.__registers[nextinstr.attr1] == 1:
                        s_p += int(nextinstr.attr2)
                        continue
            s_p += 1

    def get_b_reg(self, a_start_value: int = 0) -> int:
        """Triggers the program with the given start value and returns the value of the B-register."""
        self.__registers['a'] = a_start_value
        self.__registers['b'] = 0
        self.__run_program()
        return self.__registers['b']


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_b_reg()}")
    print(f"Part 2: {computer.get_b_reg(1)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day23.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
