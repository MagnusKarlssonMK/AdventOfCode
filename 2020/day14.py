"""
Bitmask stuff and write into emulated memory. Not much to say.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    MEM = 'mem'
    MASK = 'mask'


@dataclass(frozen=True)
class Instruction:
    action: Action
    val1: str
    val2: str = ''


class Computer:
    def __init__(self, rawstr: str) -> None:
        self.__instr: list[Instruction] = []
        for line in rawstr.splitlines():
            left, right = line.split(' = ')
            if left[:4] == 'mask':
                self.__instr.append(Instruction(Action.MASK, right))
            else:
                self.__instr.append(Instruction(Action.MEM, left[4:].strip(']'), right))

    def get_memorysum(self) -> int:
        memory: dict[int: int] = {}
        bitmask = 0, 0
        for instr in self.__instr:
            if instr.action == Action.MASK:
                mask1 = mask2 = ''
                for c in instr.val1:
                    if c == 'X':
                        mask1 += '1'
                        mask2 += '0'
                    else:
                        mask1 += '0'
                        mask2 += c
                bitmask = int(mask1, 2), int(mask2, 2)
            else:
                addr = int(instr.val1)
                val = int(instr.val2)
                memory[addr] = (val & bitmask[0]) | bitmask[1]
        return sum(list(memory.values()))

    def get_memorysum_v2(self) -> int:
        memory: dict[int: int] = {}
        xmask = 0
        addrmasks = []
        for instr in self.__instr:
            if instr.action == Action.MASK:
                x = ''
                for c in instr.val1:
                    if c == 'X':
                        x += '0'
                    else:
                        x += '1'
                xmask = int(x, 2)
                addrmasks = self.__mask_value(instr.val1)
            elif instr.action == Action.MEM:
                addr = int(instr.val1)
                val = int(instr.val2)
                for mask in addrmasks:
                    memory[(addr & xmask) | mask] = val
        return sum(list(memory.values()))

    def __mask_value(self, val: str) -> list[int]:
        if (idx := val.find('X')) != -1:
            return (self.__mask_value(val[:idx] + '0' + val[idx + 1:]) +
                    self.__mask_value(val[:idx] + '1' + val[idx + 1:]))
        else:
            return [int(val, 2)]


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_memorysum()}")
    print(f"Part 2: {computer.get_memorysum_v2()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day14.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
