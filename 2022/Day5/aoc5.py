import sys
import re
import copy


def main() -> int:
    with open('aoc5.txt', 'r') as file:
        cratelines, procedureslines = file.read().strip('\n').split('\n\n')
    procedures = [list(map(int, re.findall(r'\d+', row))) for row in procedureslines.splitlines()]
    cratelines = cratelines.splitlines()
    crates: dict[int: list[str]] = {}
    for idx, line in enumerate(reversed(cratelines)):
        if idx == 0:
            for nbr in re.findall(r'\d', line):
                crates[int(nbr)] = []
        else:
            for m in re.finditer(r'\w', line):
                crates[int(cratelines[-1][m.start()])].append(line[m.start()])

    crates_b = copy.deepcopy(crates)

    for proc in procedures:  # Procedures: Nbr - from - to
        for _ in range(proc[0]):
            movecrate = crates[proc[1]].pop()
            crates[proc[2]].append(movecrate)
    result_p1 = ""
    for key in list(crates.keys()):
        result_p1 += crates[key][-1]
    print("Part1: ", result_p1)

    for proc in procedures:
        for idx in range(proc[0]):
            movecrate = crates_b[proc[1]].pop(idx - proc[0])
            crates_b[proc[2]].append(movecrate)

    result_p2 = ""
    for key in list(crates_b.keys()):
        result_p2 += crates_b[key][-1]
    print("Part2: ", result_p2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
