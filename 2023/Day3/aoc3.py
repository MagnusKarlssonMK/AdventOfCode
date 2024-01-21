import sys
import re

Part = tuple[int, int, int, int]  # Row, Col, Len, value
Gear = tuple[int, int]  # Row, Col

partlist: dict[Part: list[Gear]] = {}
grid = []


def main() -> int:
    with open('aoc3.txt', 'r') as file:
        [grid.append(line.strip("\n")) for line in file.readlines()]

    symbollist = []

    for rowidx, row in enumerate(grid):
        nbrs = re.finditer(r"(\d+)", row)
        symbs = re.finditer(r"[^.\d]", row)
        for nbr in nbrs:
            partlist[rowidx, nbr.start(), nbr.end() - nbr.start(), int(row[nbr.start():nbr.end()])] = []
        for symb in symbs:
            symbollist.append((rowidx, symb.start()))

    result_p1 = 0

    for key in list(partlist.keys()):
        for rowidx in range(key[0] - 1, key[0] + 2):
            for colidx in range(key[1] - 1, key[1] + key[2] + 1):
                if (rowidx, colidx) in symbollist:
                    partlist[key].append((rowidx, colidx))
        if len(partlist[key]) > 0:
            result_p1 += key[3]

    print("Part1: ", result_p1)

    result_p2 = 0

    for sym in symbollist:
        if grid[sym[0]][sym[1]] == "*":
            keylist = []
            [keylist.append(key) for key in list(partlist.keys()) if sym[0] - 1 <= key[0] <= sym[0] + 1]
            adjacent = []
            for part in keylist:
                if sym in partlist[part]:
                    adjacent.append(part)
            if len(adjacent) == 2:
                result_p2 += adjacent[0][3] * adjacent[1][3]

    print("Part2: ", result_p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
