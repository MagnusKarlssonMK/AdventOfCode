"""
The instructions are a bit of a bait to implement an emulator, but that isn't actually very helpful. Instead, we need
to inspect the program and try to reverse engineer what it is doing. The monad program consists of 14 identical chunks
of instructions with slightly different numbers as arguments, i.e. each chunk represents one calculcation per digit in
the model number.
"""
import time
from pathlib import Path
from enum import Enum
from dataclasses import dataclass


class Op(Enum):
    INC = 1
    MOD = 2


@dataclass(frozen=True)
class Chunk:
    op: Op
    val: int


class ALU:
    __MIN_DIGIT = 1
    __MAX_DIGIT = 9

    def __init__(self, rawstr: str) -> None:
        self.__monad = []
        for chunk in rawstr.strip('inp w\n').split('inp w\n'):
            lines = chunk.splitlines()
            if lines[3][-1] == '1':
                self.__monad.append(Chunk(Op.INC, int(lines[-3].split()[-1])))
            else:
                self.__monad.append(Chunk(Op.MOD, int(lines[4].split()[-1])))

    def get_model_nbr(self, smallest: bool = False) -> int:
        modelnbr = [0 for _, _ in enumerate(self.__monad)]
        buffer = []
        for i, chunk in enumerate(self.__monad):
            match chunk.op:
                case Op.INC:
                    buffer.append((i, chunk.val))
                case Op.MOD:
                    idx, val = buffer.pop()
                    delta = val + chunk.val
                    if not smallest:
                        modelnbr[idx] = ALU.__MAX_DIGIT if delta < 0 else ALU.__MAX_DIGIT - delta
                        modelnbr[i] = ALU.__MAX_DIGIT if delta > 0 else ALU.__MAX_DIGIT + delta
                    else:
                        modelnbr[idx] = ALU.__MIN_DIGIT if delta > 0 else ALU.__MIN_DIGIT - delta
                        modelnbr[i] = ALU.__MIN_DIGIT if delta < 0 else ALU.__MIN_DIGIT + delta
        return int(''.join(map(str, modelnbr)))


def main(aoc_input: str) -> None:
    alu = ALU(aoc_input)
    print(f"Part 1: {alu.get_model_nbr()}")
    print(f"Part 2: {alu.get_model_nbr(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day24.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
