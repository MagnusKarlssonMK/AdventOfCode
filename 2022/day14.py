import time
from pathlib import Path


class Grid:
    def __init__(self, rawstr: str) -> None:
        lines = [[[int(c) for c in coords.split(',')] for coords in line.split(' -> ')] for line in
                 rawstr.split('\n')]
        self.__rocks: set[tuple[int, int]] = set()
        for line in lines:
            for i in range(len(line)-1):
                point1, point2 = line[i], line[i+1]
                xrock = range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1)
                yrock = range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1)
                self.__rocks.update({(x, y) for x in xrock for y in yrock})

    def dropsand(self) -> tuple[int, int]:
        start_x, start_y = 500, 0
        x, y = start_x, start_y
        max_y = max((y for _, y in self.__rocks))
        count = p1 = 0
        while True:
            if (x, y) in self.__rocks:
                x, y = start_x, start_y
            if y > max_y and p1 == 0:  # abyss part 1
                p1 = count
            if (x, y + 1) not in self.__rocks and y < max_y + 1:  # Try drop down
                y += 1
            elif (x - 1, y + 1) not in self.__rocks and y < max_y + 1:  # Try left-down
                x -= 1
                y += 1
            elif (x + 1, y + 1) not in self.__rocks and y < max_y + 1:  # Try right-down
                x += 1
                y += 1
            else:
                count += 1
                self.__rocks.add((x, y))
            if (x, y) == (start_x, start_y):
                return p1, count


def main(aoc_input: str) -> None:
    mygrid = Grid(aoc_input)
    p1, p2 = mygrid.dropsand()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day14.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
