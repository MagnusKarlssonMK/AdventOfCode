"""
Store the trench in a class with a dynamically sized grid, i.e. expands as we dig through it.
After the dig commands have been carried out, the results are calculated with shoelace formula and Pick's theorem.
"""
import sys

Directions: dict[str, tuple[int, int]] = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}

DirectionMap = {0: 'R', 1: "D", 2: 'L', 3: 'U'}


class Trench:
    def __init__(self, part: str):
        self.digposition = (0, 0)
        self.grid = [self.digposition]
        self.decoderule = part  # 'A' or 'B'

    def dig(self, command: str) -> None:
        directionstr, stepstr, colstr = command.split()
        if self.decoderule == 'A':
            direction = Directions[directionstr]
            steps = int(stepstr)
        else:
            direction = Directions[DirectionMap[int(colstr[-2])]]
            steps = int(colstr[2:7], 16)
        movesum = (self.digposition[0] + steps * direction[0],
                   self.digposition[1] + steps * direction[1])
        self.digposition = movesum
        self.grid.append(self.digposition)

    def getareapoints(self) -> int:
        areasum = sum([((self.grid[idx][0] * self.grid[idx + 1][1]) - (self.grid[idx + 1][0] * self.grid[idx][1]))
                       for idx in range(len(self.grid) - 1)])
        length = self.getoutlinelength()
        pick_i = abs(areasum // 2) + 1 + (length // 2)
        return pick_i

    def getoutlinelength(self) -> int:
        return sum([abs(self.grid[idx + 1][0] - self.grid[idx][0]) + abs(self.grid[idx + 1][1] - self.grid[idx][1])
                    for idx in range(len(self.grid) - 1)])


def main() -> int:
    mytrench_p1 = Trench("A")
    mytrench_p2 = Trench("B")

    with open("../Inputfiles/aoc18.txt") as file:
        for line in file.read().strip('n').splitlines():
            mytrench_p1.dig(line.strip("\n"))
            mytrench_p2.dig(line.strip("\n"))

    print("Part1:", mytrench_p1.getareapoints())
    print("Part2:", mytrench_p2.getareapoints())
    return 0


if __name__ == "__main__":
    sys.exit(main())
