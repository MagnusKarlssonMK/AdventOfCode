import sys
import re


Directions = ('U', 'R', 'D', 'L')
Facing = {'R': 0, 'D': 1, 'L': 2, 'U': 3}


class MonkeyMap:
    def __init__(self, mapdata: str, path: str):
        self.__rawmapdata = mapdata.splitlines()
        self.__path = re.findall(r"\d+|\w", path)
        self.__direction = 'R'
        self.__graph: dict[tuple[int, int]: dict[str: tuple[int, int]]] = {}
        points_per_row: dict[int: list[int]] = {}
        points_per_col: dict[int: list[int]] = {}
        # Fill the temporary dicts holding the points per row / col with all points (we check later for '#', index
        # needs to be correct for now).
        for row in range(len(self.__rawmapdata)):
            points_per_row[row] = []
            for col in range(len(self.__rawmapdata[row])):
                if col not in points_per_col:
                    points_per_col[col] = []
                if self.__rawmapdata[row][col] in ('.', '#'):
                    points_per_row[row].append(col)
                    points_per_col[col].append(row)
        # Add all non-wall (#) points to the graph and its horisontal neighbors (if any)
        for row in points_per_row:
            for i, col in enumerate(points_per_row[row]):
                if self.__rawmapdata[row][col] == '#':
                    continue
                leftcol = points_per_row[row][(i - 1) % len(points_per_row[row])]
                rightcol = points_per_row[row][(i + 1) % len(points_per_row[row])]
                self.__graph[(row, col)] = {}
                if self.__rawmapdata[row][leftcol] != '#':
                    self.__graph[(row, col)]['L'] = (row, leftcol)
                if self.__rawmapdata[row][rightcol] != '#':
                    self.__graph[(row, col)]['R'] = (row, rightcol)
        # Add the vertical neighbors (if any) to all non-wall points
        for col in points_per_col:
            for i, row in enumerate(points_per_col[col]):
                if self.__rawmapdata[row][col] == '#':
                    continue
                uprow = points_per_col[col][(i - 1) % len(points_per_col[col])]
                downrow = points_per_col[col][(i + 1) % len(points_per_col[col])]
                if self.__rawmapdata[uprow][col] != '#':
                    self.__graph[(row, col)]['U'] = (uprow, col)
                if self.__rawmapdata[downrow][col] != '#':
                    self.__graph[(row, col)]['D'] = (downrow, col)
        # Start position is the left-most point in the first row, we can get that from the 'per-row' dict
        self.__pos: tuple[int, int] = (0, points_per_row[0][0])

    def __rotate(self, newdir: str) -> None:
        if newdir == 'R':
            self.__direction = Directions[(Directions.index(self.__direction) + 1) % len(Directions)]
        elif newdir == 'L':
            self.__direction = Directions[(Directions.index(self.__direction) - 1) % len(Directions)]

    def get_password(self) -> int:
        for instruction in self.__path:
            if instruction.isdigit():
                for _ in range(int(instruction)):
                    if self.__direction not in self.__graph[self.__pos]:
                        break
                    self.__pos = self.__graph[self.__pos][self.__direction]
            else:
                self.__rotate(instruction)
        return (1000 * (self.__pos[0] + 1)) + (4 * (self.__pos[1] + 1)) + Facing[self.__direction]


def main() -> int:
    with open('../Inputfiles/aoc22.txt', 'r') as file:
        mymap = MonkeyMap(*file.read().strip('\n').split('\n\n'))
    print(f"Part 1: {mymap.get_password()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
