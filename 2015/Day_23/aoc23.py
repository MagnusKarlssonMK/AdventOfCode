"""
Quite straightforward, basically just store the program and then run it by having a stack-pointer walking through
the program according to the instructions.
"""
import sys
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


def main() -> int:
    with open('../Inputfiles/aoc23.txt', 'r') as file:
        computer = Computer(file.read().strip('\n'))
    print(f"Part 1: {computer.get_b_reg()}")
    print(f"Part 2: {computer.get_b_reg(1)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
