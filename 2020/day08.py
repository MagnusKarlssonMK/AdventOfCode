"""
Store the parsed program instructions in a Console class, which also holds the accumulator value. A method is called
to run the program, which stops either when a loop is encountered or when terminating successfully by reaching the
last row directly after the last instruction in the program.
"""
import time
from pathlib import Path


class Console:
    def __init__(self, rawstr: str) -> None:
        self.__accumulator = 0
        self.__instructions = [(left, int(right)) for left, right in [line.split() for line in rawstr.splitlines()]]

    def __runprogramtoloop(self) -> bool:
        """Returns True if run to completion (reaching the first index after the last row),
        False if loop encountered."""
        seen = set()
        idx = 0
        while True:
            if idx in seen:
                return False
            seen.add(idx)
            cmd, value = self.__instructions[idx]
            if cmd == "jmp":
                idx = idx + value
            else:
                if cmd == "acc":
                    self.__accumulator += value
                idx += 1
            if idx == len(self.__instructions):
                return True
            idx = idx % len(self.__instructions)

    def get_boot_accumulator_value(self) -> int:
        self.__runprogramtoloop()
        return self.__accumulator

    def repair(self) -> int:
        """Tries swapping all nop<->jmp until the program completes and returns the accumulator value once
        successful. Returns -1 if no solution found."""
        swap = {'nop': 'jmp', 'jmp': 'nop'}
        for idx in range(len(self.__instructions)):
            if self.__instructions[idx][0] != "acc":
                self.__instructions[idx] = (swap[self.__instructions[idx][0]], self.__instructions[idx][1])
                if self.__runprogramtoloop():
                    return self.__accumulator
                # else - not successful, reset
                self.__accumulator = 0
                self.__instructions[idx] = (swap[self.__instructions[idx][0]], self.__instructions[idx][1])
        return -1


def main(aoc_input: str) -> None:
    myconsole = Console(aoc_input)
    print(f"Part 1: {myconsole.get_boot_accumulator_value()}")
    print(f"Part 2: {myconsole.repair()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
