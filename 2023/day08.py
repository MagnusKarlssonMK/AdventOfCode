"""
Stores the node input in a dict in a class, which provides methods to calculate the corresponding answers to Part 1
and Part 2, with the sequence as input. Uses LCM from the math module to calculate the value for part 2.
"""
import time
from pathlib import Path
import re
import math


class NodeNetwork:
    def __init__(self, rawstr: str) -> None:
        self.__nodes: dict[str: dict[str: str]] = {}
        self.__sequence, lines = rawstr.split('\n\n')
        for line in lines.splitlines():
            if len(line) > 1:
                a, b, c = re.findall(r"\w+", line)
                self.__nodes[a] = {'L': b, 'R': c}

    def stepcount_zzz(self) -> int:
        location = 'AAA'
        stepcount = 0
        while location != 'ZZZ':
            location = self.__nodes[location][self.__sequence[stepcount % len(self.__sequence)]]
            stepcount += 1
        return stepcount

    def stepcount_atoz(self) -> int:
        location = [node for node in self.__nodes if node[-1] == 'A']
        cycles = []
        for startpoint in location:
            stepcount = 0
            currentloc = startpoint
            while currentloc[-1] != 'Z':
                currentloc = self.__nodes[currentloc][self.__sequence[stepcount % len(self.__sequence)]]
                stepcount += 1
            cycles.append(stepcount)
        return math.lcm(*cycles)


def main(aoc_input: str) -> None:
    mynodes = NodeNetwork(aoc_input)
    print(f"Part 1: {mynodes.stepcount_zzz()}")
    print(f"Part 2: {mynodes.stepcount_atoz()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
