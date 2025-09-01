"""
Part 1: Re-use the computer class created in Day 12, and add the toggle operation. Two things to note:
- Since the new operation modifies the program, the instruction class can't be frozen (alternatively we would need to
re-create the instance every time we run the toggle op)
- We need to deepcopy the program so those modifications don't carry over to part 2.

Part 2: Simply change the start value and then wait. Or, maybe don't wait, this will take forever. We need to
implement some optimizations as hinted by the problem description, since some of the loops in the program are
essentially performing multiplication and addition of enormuous number by adding +1 at a time. So we create two new
operations to add and multiply two arguments into a register, and update the program in the identified specific
patterns to use these instead. The 'jnz'_0_0 operation is used as a filler 'nop' operation, since we need to retain the
same number of lines to make the offsets in the program still work. With this optimization the time to complete
part 2 goes from 99999999 (probably hours) to near instant.

This optimization could potentially also be back-ported to the solution for Day-12, since that was running fairly slow
as well, probably for the same reasons.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Instruction:
    instr: str
    arg1: str
    arg2: str = None
    arg3: str = None


class Computer:
    def __init__(self, rawstr: str) -> None:
        self.__program = tuple(Instruction(*line.split()) for line in rawstr.splitlines())
        self.__optimize_program()

    def get_a_register(self, colored_eggs: bool = False) -> int:
        sp = 0
        regs = {reg: 0 for reg in ['a', 'b', 'c', 'd']}
        if colored_eggs:
            regs['a'] = 12
        else:
            regs['a'] = 7
        program = list(deepcopy(self.__program))

        while 0 <= sp < len(program):
            match program[sp].instr:
                case 'cpy':
                    if program[sp].arg2 in regs:
                        if program[sp].arg1 in regs:
                            regs[program[sp].arg2] = regs[program[sp].arg1]
                        else:
                            regs[program[sp].arg2] = int(program[sp].arg1)
                case 'inc':
                    if program[sp].arg1 in regs:
                        regs[program[sp].arg1] += 1
                case 'dec':
                    if program[sp].arg1 in regs:
                        regs[program[sp].arg1] -= 1
                case 'jnz':
                    a1 = regs[program[sp].arg1] if program[sp].arg1 in regs else int(program[sp].arg1)
                    a2 = regs[program[sp].arg2] if program[sp].arg2 in regs else int(program[sp].arg2)
                    if a1 != 0:
                        sp += a2
                        continue
                case 'tgl':
                    x = regs[program[sp].arg1] if program[sp].arg1 in regs else int(program[sp].arg1)
                    x += sp
                    if 0 <= x < len(program):
                        if program[x].arg2:
                            program[x].instr = 'cpy' if program[x].instr == 'jnz' else 'jnz'
                        else:
                            program[x].instr = 'dec' if program[x].instr == 'inc' else 'inc'
                case 'mul':
                    if program[sp].arg1 in regs:
                        a2 = regs[program[sp].arg2] if program[sp].arg2 in regs else int(program[sp].arg2)
                        a3 = regs[program[sp].arg3] if program[sp].arg3 in regs else int(program[sp].arg3)
                        regs[program[sp].arg1] = a2 * a3
                case 'add':
                    if program[sp].arg1 in regs:
                        a2 = regs[program[sp].arg2] if program[sp].arg2 in regs else int(program[sp].arg2)
                        a3 = regs[program[sp].arg3] if program[sp].arg3 in regs else int(program[sp].arg3)
                        regs[program[sp].arg1] = a2 + a3
                case _:
                    pass
            sp += 1
        return regs['a']

    def __optimize_program(self) -> None:
        opt: list[Instruction] = list(self.__program)
        for i in range(len(opt) - 5):
            if all((opt[i].instr == 'inc',
                    opt[i+1].instr == 'dec',
                    opt[i+2].instr == 'jnz' and opt[i+2].arg2 == '-2' and opt[i+2].arg1 == opt[i+1].arg1,
                    opt[i+3].instr == 'dec',
                    opt[i+4].instr == 'jnz' and opt[i+4].arg2 == '-5' and opt[i+4].arg1 == opt[i+3].arg1)):
                opt[i] = Instruction('mul', opt[i].arg1, opt[i+1].arg1, opt[i+3].arg1)
                opt[i+1] = Instruction('cpy', '0', opt[i+1].arg1)
                opt[i+2] = Instruction('cpy', '0', opt[i+3].arg1)
                opt[i+3] = Instruction('jnz', '0', '0')
                opt[i+4] = Instruction('jnz', '0', '0')
        for i in range(len(opt) - 3):
            if all((opt[i].instr == 'inc',
                    opt[i+1].instr == 'dec' or opt[i+1].instr == 'inc',
                    opt[i+2].instr == 'jnz' and opt[i+2].arg1 == opt[i+1].arg1 and opt[i+2].arg2 == '-2')):
                opt[i] = Instruction('add', opt[i].arg1, opt[i+1].arg1, opt[i].arg1)
                opt[i+1] = Instruction('cpy', '0', opt[i+1].arg1)
                opt[i+2] = Instruction('jnz', '0', '0')
            elif all((opt[i].instr == 'dec',
                      opt[i+1].instr == 'inc',
                      opt[i+2].instr == 'jnz' and opt[i+2].arg1 == opt[i].arg1 and opt[i+2].arg2 == '-2')):
                opt[i] = Instruction('add', opt[i+1].arg1, opt[i].arg1, opt[i+1].arg1)
                opt[i+1] = Instruction('cpy', '0', opt[i+2].arg1)
                opt[i+2] = Instruction('jnz', '0', '0')
        self.__program = tuple(opt)


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_a_register()}")
    print(f"Part 2: {computer.get_a_register(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day23.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
