"""
Start with the code from day 23 as base.
Then add an operation for the 'out' transmission.
Now instead of starting with a specific value for the 'a' register, we need to loop until we find a working value and
return that. If the transmitted value doesn't follow the '0,1,0,1...' pattern, break and try the next a-value.
As long as it does follow that pattern, store the program state in a list and check if we have reached a state we have
seen before. If so, we know that we have a loop that will repeat, i.e. the exit condition have been met, so we have
found the answer.

** NOTE - the program optimization done in day 23 doesn't work with this input for some reason, so I disabled that for
now, it doesn't seem to make any major performance difference with this program.
I will need to come back and debug it later. **
"""
import sys
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
        # self.__optimize_program()  # TBD figure out why this doesn't work here!! Only getting match in the 5-argument
        # condition, so probably somehow related to the multiplication operation that replaces it...?

    def get_a_register(self) -> int:
        i = 0
        while True:
            sp = 0
            regs = {reg: 0 for reg in ['a', 'b', 'c', 'd']}
            regs['a'] = i
            program = list(deepcopy(self.__program))
            program_states = []

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
                    case 'out':
                        transmitted = regs[program[sp].arg1] if program[sp].arg1 in regs else int(program[sp].arg1)
                        if transmitted != (len(program_states) % 2):
                            break
                        p_state = (sp, tuple(program), tuple(regs.values()))
                        if p_state in program_states:
                            return i
                        program_states.append(p_state)
                sp += 1
            i = i + 1

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


def main() -> int:
    with open('../Inputfiles/aoc25.txt', 'r') as file:
        computer = Computer(file.read().strip('\n'))
    print(f"Part 1: {computer.get_a_register()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
