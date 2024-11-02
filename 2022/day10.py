import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class Instruction(Enum):
    NOOP = 'noop'
    ADDX = 'addx'


@dataclass(frozen=True)
class Line:
    instr: Instruction
    value: int = -1


class CPU:
    def __init__(self, rawstr: str) -> None:
        self.__program = []
        for line in rawstr.splitlines():
            s = line.split()
            if len(s) == 1:
                self.__program.append(Line(Instruction(s[0])))
            else:
                self.__program.append(Line(Instruction(s[0]), int(s[1])))

    def get_signal_strength_sum(self) -> int:
        def increment(cycle: int) -> int:
            intervals = [20, 60, 100, 140, 180, 220]
            return cycle if cycle in intervals else 0
        result = 0
        reg_x = 1
        cyclenbr = 0
        for p in self.__program:
            if p.instr == Instruction.NOOP:
                cyclenbr += 1
                result += reg_x * increment(cyclenbr)
            elif p.instr == Instruction.ADDX:
                cyclenbr += 1
                result += reg_x * increment(cyclenbr)
                cyclenbr += 1
                result += reg_x * increment(cyclenbr)
                reg_x += p.value
        return result

    def get_crt_output(self) -> str:
        crt = [['' for _ in range(40)] for _ in range(6)]

        def update_crt(cycle: int, x: int) -> None:
            crt[cycle // 40][cycle % 40] = '#' if abs(x - (cycle % 40)) <= 1 else ' '
        reg_x = 1
        cyclenbr = 0
        for p in self.__program:
            if p.instr == Instruction.NOOP:
                update_crt(cyclenbr, reg_x)
                cyclenbr += 1
            elif p.instr == Instruction.ADDX:
                update_crt(cyclenbr, reg_x)
                cyclenbr += 1
                update_crt(cyclenbr, reg_x)
                cyclenbr += 1
                reg_x += p.value
        return ''.join([''.join(line + ['\n']) for line in crt])


def main(aoc_input: str) -> None:
    cpu = CPU(aoc_input)
    print(f"Part 1: {cpu.get_signal_strength_sum()}")
    print(f"Part 2:\n{cpu.get_crt_output()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day10.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
