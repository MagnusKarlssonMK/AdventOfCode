"""
Store the parsed program instructions in a Console class, which also holds the accumulator value. A method is called
to run the program, which stops either when a loop is encountered or when terminating successfully by reaching the
last row directly after the last instruction in the program.
"""
import sys


class Console:
    def __init__(self, instructions: list[tuple[str, int]]):
        self.accumulator = 0
        self.instructions = instructions

    def runprogramtoloop(self) -> bool:
        """Returns True if run to completion (reaching the first index after the last row),
        False if loop encountered."""
        seen = set()
        idx = 0
        while True:
            if idx in seen:
                return False
            seen.add(idx)
            cmd, value = self.instructions[idx]
            if cmd == "jmp":
                idx = idx + value
            else:
                if cmd == "acc":
                    self.accumulator += value
                idx += 1
            if idx == len(self.instructions):
                return True
            idx = idx % len(self.instructions)

    def repair(self) -> int:
        """Tries swapping all nop<->jmp until the program completes and returns the accumulator value once
        successful. Returns -1 if no solution found."""
        swap = {'nop': 'jmp', 'jmp': 'nop'}
        for idx in range(len(self.instructions)):
            if self.instructions[idx][0] != "acc":
                self.instructions[idx] = (swap[self.instructions[idx][0]], self.instructions[idx][1])
                if self.runprogramtoloop():
                    return self.accumulator
                # else - not successful, reset
                self.accumulator = 0
                self.instructions[idx] = (swap[self.instructions[idx][0]], self.instructions[idx][1])
        return -1


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        myconsole = Console([(left, int(right)) for left, right in
                             [line.split() for line in file.read().strip('\n').splitlines()]])
    myconsole.runprogramtoloop()
    print("Part 1:", myconsole.accumulator)
    print("Part 2:", myconsole.repair())
    return 0


if __name__ == "__main__":
    sys.exit(main())
