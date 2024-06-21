"""
Kind of trivial by mapping the input on the operator functions, and extracting the register names into a set during the
parsing of the input.
Just run through the program and get the answer to part 1 from the register with the max value at that time.
For part 2, simply keep track of the max value during the execution of the program. We can get both answers during
one runthrough of the program.
"""
import sys
import operator as op
from dataclasses import dataclass


@dataclass(frozen=True)
class Instr:
    reg: str
    opr: op
    val: int
    cond_reg: str
    cond_opr: op
    cond_val: int


class CPU:
    __OP_MAP = {'inc': op.add, 'dec': op.sub, '>': op.gt, '>=': op.ge,
                '<': op.lt, '<=': op.le, '==': op.eq, '!=': op.ne}

    def __init__(self, rawstr: str) -> None:
        self.__instr = []
        self.__regs = set()
        for line in rawstr.splitlines():
            r, o, v, _, cr, co, cv = line.split()
            self.__instr.append(Instr(r, CPU.__OP_MAP[o], int(v), cr, CPU.__OP_MAP[co], int(cv)))
            self.__regs.update((r, cr))

    def get_largest_reg_value(self) -> tuple[int, int]:
        regs = {r: 0 for r in self.__regs}
        maxval = 0
        for i in self.__instr:
            if i.cond_opr(regs[i.cond_reg], i.cond_val):
                regs[i.reg] = i.opr(regs[i.reg], i.val)
                maxval = max(maxval, regs[i.reg])
        return max(regs.values()), maxval


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        cpu = CPU(file.read().strip('\n'))
    p1, p2 = cpu.get_largest_reg_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
