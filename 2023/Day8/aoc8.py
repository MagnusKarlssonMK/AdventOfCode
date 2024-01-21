import sys
import re
import math


def main() -> int:
    nodes: dict[str: dict[str]] = {}

    with open('aoc8.txt', 'r') as file:
        seq = file.readline().strip('\n')
        for line in file.readlines():
            if len(line) > 1:
                a, b, c = re.findall(r"\w+", line)
                nodes[a] = {'L': b, 'R': c}

    location_p1 = 'AAA'
    stepcount_p1 = 0

    while location_p1 != 'ZZZ':
        location_p1 = nodes[location_p1][seq[stepcount_p1 % len(seq)]]
        stepcount_p1 += 1

    location_p2 = [strwa for strwa in list(nodes.keys()) if strwa[2] == 'A']
    cycles = []

    for startpoint in location_p2:
        stepcount_p2 = 0
        currentloc = startpoint
        while currentloc[2] != 'Z':
            currentloc = nodes[currentloc][seq[stepcount_p2 % len(seq)]]
            stepcount_p2 += 1
        cycles.append(stepcount_p2)
    result_p2 = math.lcm(*cycles)

    print("Part1: ", stepcount_p1)
    print("Part2: ", result_p2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
