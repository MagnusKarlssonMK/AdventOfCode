import sys


class Grid:
    def __init__(self, rawstr: str):
        lines = [[[int(c) for c in coords.split(',')] for coords in line.split(' -> ')] for line in
                 rawstr.split('\n')]
        self.rocks = set()
        for line in lines:
            for i in range(len(line)-1):
                point1, point2 = line[i], line[i+1]
                xrock = range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1)
                yrock = range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1)
                self.rocks.update({(x, y) for x in xrock for y in yrock})

    def dropsand(self) -> [int, int]:
        start_x, start_y = 500, 0
        x, y = start_x, start_y
        max_y = max((y for _, y in self.rocks))
        count = p1 = p2 = 0
        while True:
            if (x, y) in self.rocks:
                x, y = start_x, start_y
            if y > max_y and p1 == 0:  # abyss part 1
                p1 = count
            if (x, y + 1) not in self.rocks and y < max_y + 1:  # Try drop down
                y += 1
            elif (x - 1, y + 1) not in self.rocks and y < max_y + 1:  # Try left-down
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in self.rocks and y < max_y + 1:  # Try right-down
                x += 1
                y += 1
            else:
                count += 1
                self.rocks.add((x, y))
            if (x, y) == (start_x, start_y):
                p2 = count
                break
        return [p1, p2]


def main() -> int:
    with open('../Inputfiles/aoc14.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))

    p1, p2 = mygrid.dropsand()
    print("Part1: ", p1)
    print("Part2: ", p2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
