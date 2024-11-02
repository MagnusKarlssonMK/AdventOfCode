"""
Straightforward; just step through the program with a stackpointer, while modifying the program along the way as
described in the instructions. The only difference between part 1 and 2 is the step for the program modification at
each jump.
"""
import time
from pathlib import Path


class CPU:
    def __init__(self, rawstr: str) -> None:
        self.__instr = tuple(map(int, rawstr.splitlines()))

    def get_exit_step_count(self, stranger: bool = False) -> int:
        program = list(self.__instr)
        sp = 0
        count = 0
        while 0 <= sp < len(program):
            count += 1
            val = program[sp]
            step = -1 if (stranger and val >= 3) else 1
            program[sp] += step
            sp += val
        return count


def main(aoc_input: str) -> None:
    cpu = CPU(aoc_input)
    print(f"Part 1: {cpu.get_exit_step_count()}")
    print(f"Part 1: {cpu.get_exit_step_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
