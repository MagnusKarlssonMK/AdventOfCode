"""
Stores the node input in a dict in a class, which provides methods to calculate the corresponding answers to Part 1
and Part 2, with the sequence as input. Uses LCM from the math module to calculate the value for part 2.
"""
import sys
import re
import math


class NodeNetwork:
    def __init__(self, rawinput: str):
        self.nodes: dict[str: dict[str: str]] = {}
        for line in rawinput.splitlines():
            if len(line) > 1:
                a, b, c = re.findall(r"\w+", line)
                self.nodes[a] = {'L': b, 'R': c}

    def stepcount_zzz(self, seq: str) -> int:
        location = 'AAA'
        stepcount = 0
        while location != 'ZZZ':
            location = self.nodes[location][seq[stepcount % len(seq)]]
            stepcount += 1
        return stepcount

    def stepcount_atoz(self, seq: str) -> int:
        location = [strwa for strwa in list(self.nodes.keys()) if strwa[2] == 'A']
        cycles = []
        for startpoint in location:
            stepcount = 0
            currentloc = startpoint
            while currentloc[2] != 'Z':
                currentloc = self.nodes[currentloc][seq[stepcount % len(seq)]]
                stepcount += 1
            cycles.append(stepcount)
        return math.lcm(*cycles)


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        sequence, lines = file.read().strip('\n').split('\n\n')
        mynodes = NodeNetwork(lines)

    print("Part1: ", mynodes.stepcount_zzz(sequence))
    print("Part2: ", mynodes.stepcount_atoz(sequence))
    return 0


if __name__ == "__main__":
    sys.exit(main())
