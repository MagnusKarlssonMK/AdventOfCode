"""
To avoid having to continuously update the list of blizzards, instead store the blizzards in a per-direction dict,
and calculate dynamically whether a certain point will be occupied by at least one blizzard at a certain minute.
Use BFS to traverse the map. We need to allow backtracking, but have a check that we only evaluate a certain point
once at a specific time (it doesn't matter how we got there).
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day24.txt')


class Valley:
    def __init__(self, inputgrid: str) -> None:
        directions = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
        self.__startpoint = -1, -1
        self.__exitpoint = -1, -1
        self.__walls = set()
        self.__blizzards: dict[tuple[int, int]: set[tuple[int, int]]] = {directions[d]: set() for d in directions}
        lines = inputgrid.splitlines()
        self.__width = len(lines[0]) - 2  # Don't include the walls
        self.__height = len(lines) - 2
        for r, row in enumerate(lines):
            for c, col in enumerate(row):
                if col == "#":
                    self.__walls.add((r, c))
                elif r == 0 and col == ".":
                    self.__startpoint = (r, c)
                elif r == len(lines) - 1 and col == ".":
                    self.__exitpoint = (r, c)
                elif col in directions:
                    self.__blizzards[directions[col]].add((r, c))

    def __is_occupied_at_step(self, point_row: int, point_col: int, step: int) -> bool:
        for bliz_dir_row, bliz_dir_col in self.__blizzards:
            start_row = 1 + (point_row - 1 - (step * bliz_dir_row)) % self.__height
            start_col = 1 + (point_col - 1 - (step * bliz_dir_col)) % self.__width
            if (start_row, start_col) in self.__blizzards[bliz_dir_row, bliz_dir_col]:
                return True
        return False

    def __bfs(self, start: tuple[int, int], end: tuple[int, int], startstep: int = 0) -> int:
        queue = [(start, startstep)]
        seen = set()
        while queue:
            point, steps = queue.pop(0)
            if (point, steps) in seen:
                continue
            seen.add((point, steps))
            point_row, point_col = point
            for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]:
                new_row = point_row + d_row
                new_col = point_col + d_col
                new_point = (new_row, new_col)
                next_step = steps + 1
                if new_point == start and (d_row, d_col) != start:
                    # The start point won't pass the boundary check below, and the occupied check won't work for it
                    # either. So just put it on the queue directly as a workaround.
                    queue.append((new_point, next_step))
                    continue
                if new_point == end:
                    return next_step
                if 0 < new_row <= self.__height and 0 < new_col <= self.__width:
                    if not self.__is_occupied_at_step(new_row, new_col, next_step):
                        queue.append((new_point, next_step))
        return -1

    def get_there(self) -> int:
        return self.__bfs(self.__startpoint, self.__exitpoint)

    def get_there_and_back_again(self) -> int:
        a = self.__bfs(self.__startpoint, self.__exitpoint, 0)
        # Could have perhaps cached the 'a' value from the part 1 run
        b = self.__bfs(self.__exitpoint, self.__startpoint, a)
        c = self.__bfs(self.__startpoint, self.__exitpoint, b)
        return c


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        valley = Valley(file.read().strip('\n'))
    print(f"Part 1: {valley.get_there()}")
    print(f"Part 2: {valley.get_there_and_back_again()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
