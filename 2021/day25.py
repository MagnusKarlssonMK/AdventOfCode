"""
Yet another variant of game-of-life. Storing the cucumbers in separate dictionaries per movement direction, so we can
first move the east-moving ones, and then process the south-moving cucumbers based on that intermittent result. Also
stores in dictionaries per x/y coordinate rather than dumping it all in giant sets of x/y coordinates, which makes it a
bit more complicated but seems to speed up the execution quite a bit.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2021/day25.txt')


class Seabottom:
    def __init__(self, rawstr: str) -> None:
        lines = rawstr.splitlines()
        self.__x_max = len(lines[0])
        self.__y_max = len(lines)
        self.__east: dict[int: set[int]] = {}
        self.__south: dict[int: set[int]] = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '>':
                    if y not in self.__east:
                        self.__east[y] = {x}
                    else:
                        self.__east[y].add(x)
                elif c == 'v':
                    if x not in self.__south:
                        self.__south[x] = {y}
                    else:
                        self.__south[x].add(y)

    def get_rounds_stop_moving(self) -> int:
        steps = 0
        while True:
            changed = False
            steps += 1
            next_east: dict[int: set[int]] = {}
            next_south: dict[int: set[int]] = {}
            for y in self.__east:
                if y not in next_east:
                    next_east[y] = set()
                for x in self.__east[y]:
                    if ((east_x := (x + 1) % self.__x_max) not in self.__east[y] and
                            (east_x not in self.__south or y not in self.__south[east_x])):
                        next_east[y].add(east_x)
                        changed = True
                    else:
                        next_east[y].add(x)
            for x in self.__south:
                if x not in next_south:
                    next_south[x] = set()
                for y in self.__south[x]:
                    if (((south_y := (y + 1) % self.__y_max) not in next_east or x not in next_east[south_y]) and
                            south_y not in self.__south[x]):
                        next_south[x].add(south_y)
                        changed = True
                    else:
                        next_south[x].add(y)
            if not changed:
                return steps
            self.__east = next_east
            self.__south = next_south


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        bottom = Seabottom(file.read().strip('\n'))
    print(f"Part 1: {bottom.get_rounds_stop_moving()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
