"""
For part 1, simply running the program is enough.

But for part 2, the program needs to be optimized. The problematic area is between lines 2-12 (in my input), which
is doing some sort of modulo operation extremely inefficiently. So insert a piece of code that effectively replaces
those lines and does the same job. I've tried to make it reasonably generic by extracting the used registers from the
input, but it will not work for other inputs if the specific lines in the program doing this work are different.

The same optimization can be used in the common function for both parts, and seems to give quite a large performance
boost also for part 1.
"""
import time
from pathlib import Path


OP_CODES = {
    "addr": lambda r, a, b: r[a] + r[b],
    "addi": lambda r, a, b: r[a] + b,
    "mulr": lambda r, a, b: r[a] * r[b],
    "muli": lambda r, a, b: r[a] * b,
    "banr": lambda r, a, b: r[a] & r[b],
    "bani": lambda r, a, b: r[a] & b,
    "borr": lambda r, a, b: r[a] | r[b],
    "bori": lambda r, a, b: r[a] | b,
    "setr": lambda r, a, b: r[a],
    "seti": lambda r, a, b: a,
    "gtir": lambda r, a, b: 1 if a > r[b] else 0,
    "gtri": lambda r, a, b: 1 if r[a] > b else 0,
    "gtrr": lambda r, a, b: 1 if r[a] > r[b] else 0,
    "eqir": lambda r, a, b: 1 if a == r[b] else 0,
    "eqri": lambda r, a, b: 1 if r[a] == b else 0,
    "eqrr": lambda r, a, b: 1 if r[a] == r[b] else 0
}


class Device:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__ip_reg = int(lines[0].split()[1])
        self.__program = [(OP_CODES[r], int(a), int(b), int(c)) for r, a, b, c in [line.split() for line in lines[1:]]]

    def get_reg_zero_val(self, startvalue: int = 0) -> int:
        registers = [0 for _ in range(6)]
        registers[0] = startvalue
        patchreg1 = self.__program[3][1]
        patchreg2 = self.__program[4][2]
        patchreg3 = self.__program[7][2]
        ip = 0
        while 0 <= ip < len(self.__program):
            registers[self.__ip_reg] = ip
            r, a, b, c = self.__program[ip]
            registers[c] = r(registers, a, b)
            ip = registers[self.__ip_reg] + 1

            # Patching the really slow part of the program - this assumes that the troublesome lines are in the
            # area between lines 2 - 12 in the program
            if ip == 2 and registers[patchreg1] != 0:
                while registers[patchreg1] <= registers[patchreg2]:
                    if registers[patchreg2] % registers[patchreg1] == 0:
                        registers[patchreg3] += registers[patchreg1]
                    registers[patchreg1] += 1
                ip = 13

        return registers[0]


def main(aoc_input: str) -> None:
    device = Device(aoc_input)
    print(f"Part 1: {device.get_reg_zero_val()}")
    print(f"Part 2: {device.get_reg_zero_val(1)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day19.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
