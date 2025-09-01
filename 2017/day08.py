"""
Kind of trivial by mapping the input on the operator functions, and extracting the register names into a set during the
parsing of the input.
Just run through the program and get the answer to part 1 from the register with the max value at that time.
For part 2, simply keep track of the max value during the execution of the program. We can get both answers during
one runthrough of the program.
"""
import time
from pathlib import Path
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
        self.__instr: list[Instr] = []
        self.__regs: set[str] = set()
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


def main(aoc_input: str) -> None:
    cpu = CPU(aoc_input)
    p1, p2 = cpu.get_largest_reg_value()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
