"""
Load the opcode functionality into lambda functions mapped in a dict, then for each sample, run through all opcodes
and check which ones result in a matching value. Sum up the number of samples that have at least 3 matches to get the
answer to part 1. For part 2, play a bit of sudoku to generate the mapping between opcode and number, and then run the
test program to find the value of register 0.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day16.txt')


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


@dataclass(frozen=True)
class Instruction:
    r: int
    a: int
    b: int
    c: int


@dataclass(frozen=True)
class Sample:
    before: list[int]
    after: list[int]
    instr: Instruction

    def get_matching_ops(self) -> list[str]:
        return [op for op in OP_CODES
                if OP_CODES[op](self.before, self.instr.a, self.instr.b) == self.after[self.instr.c]]


class Device:
    def __init__(self, rawstr: str) -> None:
        samples, testprogram = rawstr.split('\n\n\n')
        self.__testprogram = [Instruction(*list(map(int, re.findall(r"\d+", line))))
                              for line in testprogram.strip('\n').splitlines()]
        self.__samples = []
        for sample in samples.split('\n\n'):
            s = sample.splitlines()
            self.__samples.append(Sample(list(map(int, re.findall(r"\d+", s[0]))),
                                         list(map(int, re.findall(r"\d+", s[2]))),
                                         Instruction(*list(map(int, re.findall(r"\d+", s[1]))))))

    def get_samples_count(self) -> int:
        return sum([1 for sample in self.__samples if len(sample.get_matching_ops()) >= 3])

    def get_reg_zero_value(self) -> int:
        # Create dict of possible opcode candidates for each number
        candidates = {}
        for sample in self.__samples:
            for m in sample.get_matching_ops():
                if sample.instr.r not in candidates:
                    candidates[sample.instr.r] = set()
                candidates[sample.instr.r].add(m)
        # Figure out the exact mapping sudoku style
        op_mapping = {}
        while candidates:
            for known_nbr in [c for c in candidates if len(candidates[c]) == 1]:
                op_mapping[known_nbr] = candidates[known_nbr].pop()
                del candidates[known_nbr]
                for cand in candidates:
                    if op_mapping[known_nbr] in candidates[cand]:
                        candidates[cand].remove(op_mapping[known_nbr])
        # With the opcodes known, we can now run the program
        registers = [0, 0, 0, 0]
        for instr in self.__testprogram:
            registers[instr.c] = OP_CODES[op_mapping[instr.r]](registers, instr.a, instr.b)
        return registers[0]


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        device = Device(file.read().strip('\n'))
    print(f"Part 1: {device.get_samples_count()}")
    print(f"Part 2: {device.get_reg_zero_value()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
