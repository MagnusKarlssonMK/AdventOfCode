"""
Part 1: Mostly just re-use the code from day 18 with some modifications.
Part 2: A lot of manual work to try to de-compile the assemply to see what's going on. In short, the program seems to
try to count the number of non-prime numbers in the range between what the B and C registers are initialized with, and
jumps with a stepsize defined in the second last row. Rather than trying to patch the assembly, I wound up just
writing that calculation directly instead, trying to extract the numbers from the input rather than direct hard coding
it. But since I don't know if all inputs are structured exactly like this, it might not work for other inputs.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Instr:
    op: str
    attr1: str = None
    attr2: str = None


class Register:
    def __init__(self, regs: set[str], a_init: int = 0) -> None:
        self.__regs: dict[str: int] = {r: 0 for r in regs}
        self.__regs['a'] = a_init

    def get_value(self, attr: str) -> int:
        if attr in self.__regs:
            return self.__regs[attr]
        return int(attr)

    def set_value(self, reg: str, val: int) -> None:
        self.__regs[reg] = val

    def sub_value(self, reg: str, val: int) -> None:
        self.__regs[reg] -= val

    def mul_value(self, reg: str, val: int) -> None:
        self.__regs[reg] *= val


class Coprocessor:
    def __init__(self, rawstr: str) -> None:
        self.__registers = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
        self.__instr = []
        for line in rawstr.splitlines():
            t = line.split()
            self.__instr.append(Instr(*t))

    def get_mul_count(self) -> int:
        sp = 0
        regs = Register(self.__registers)
        mulcount = 0
        while 0 <= sp < len(self.__instr):
            i = self.__instr[sp]
            match i.op:
                case 'set':
                    regs.set_value(i.attr1, regs.get_value(i.attr2))
                case 'sub':
                    regs.sub_value(i.attr1, regs.get_value(i.attr2))
                case 'mul':
                    regs.mul_value(i.attr1, regs.get_value(i.attr2))
                    mulcount += 1
                case 'jnz':
                    if regs.get_value(i.attr1) != 0:
                        sp += regs.get_value(i.attr2)
                        continue
            sp += 1
        return mulcount

    def get_h_reg(self) -> int:
        sp = 0
        regs = Register(self.__registers, 1)
        # Run the program just to get the initial values for B and C, then stop.
        while 0 <= sp < len(self.__instr):
            i = self.__instr[sp]
            if i.attr1 not in ('a', 'b', 'c'):
                break
            match i.op:
                case 'set':
                    regs.set_value(i.attr1, regs.get_value(i.attr2))
                case 'sub':
                    regs.sub_value(i.attr1, regs.get_value(i.attr2))
                case 'mul':
                    regs.mul_value(i.attr1, regs.get_value(i.attr2))
                case 'jnz':
                    if regs.get_value(i.attr1) != 0:
                        sp += regs.get_value(i.attr2)
                        continue
            sp += 1

        # b_jump grabbed directly from the input, this assumes that the jump is located on this specific row
        b_jump = abs(int(self.__instr[-2].attr2))
        h = 0
        for b in range(regs.get_value('b'), regs.get_value('c') + 1, b_jump):
            for i in range(2, b):
                if b % i == 0:
                    h += 1
                    break
        return h


def main(aoc_input: str) -> None:
    cpu = Coprocessor(aoc_input)
    print(f"Part 1: {cpu.get_mul_count()}")
    print(f"Part 2: {cpu.get_h_reg()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day23.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
