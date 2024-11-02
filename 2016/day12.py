"""
Straightforward, simply store the program in a computer class, and then run the program according to the definitions
of the instructions. For Part 2, simply change the initial value for register C to 1 instead of 0.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Instruction:
    instr: str
    arg1: str
    arg2: str = None


class Computer:
    def __init__(self, rawstr: str) -> None:
        self.__program = [Instruction(*line.split()) for line in rawstr.splitlines()]

    def get_a_register(self, initialize_c: bool = False) -> int:
        sp = 0
        regs = {reg: 0 for reg in ['a', 'b', 'c', 'd']}
        if initialize_c:
            regs['c'] = 1

        while 0 <= sp < len(self.__program):
            match self.__program[sp].instr:
                case 'cpy':
                    if self.__program[sp].arg2 in regs:
                        if self.__program[sp].arg1 in regs:
                            regs[self.__program[sp].arg2] = regs[self.__program[sp].arg1]
                        else:
                            regs[self.__program[sp].arg2] = int(self.__program[sp].arg1)
                case 'inc':
                    if self.__program[sp].arg1 in regs:
                        regs[self.__program[sp].arg1] += 1
                case 'dec':
                    if self.__program[sp].arg1 in regs:
                        regs[self.__program[sp].arg1] -= 1
                case 'jnz':
                    a1 = (regs[self.__program[sp].arg1] if self.__program[sp].arg1 in regs
                          else int(self.__program[sp].arg1))
                    a2 = (regs[self.__program[sp].arg2] if self.__program[sp].arg2 in regs
                          else int(self.__program[sp].arg2))
                    if a1 != 0:
                        sp += a2
                        continue
            sp += 1
        return regs['a']


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_a_register()}")
    print(f"Part 2: {computer.get_a_register(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
