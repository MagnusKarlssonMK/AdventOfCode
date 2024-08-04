"""
Simple BFS solution, and implementing the neighbor generator function in a point class.
The only difference between Part 1 & 2 is in the stop condition for the search function; in part 1 we are looking
for a specific target node, while for part 2 we want to walk 50 steps and then check number of seen nodes.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2016/day13.txt')


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self, keyval: int) -> iter:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x = self.x + dx
            y = self.y + dy
            if x < 0 or y < 0:
                continue
            val = (x * x) + (3 * x) + (2 * x * y) + y + (y * y) + keyval
            if bin(val).count('1') % 2 == 0:
                yield Point(x, y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class CubicleMaze:
    def __init__(self, nbr: int) -> None:
        self.__favorite_nbr = nbr

    def get_count(self, targetpoint: Point = Point(31, 39), steplimit: int = 0) -> int:
        """BFS to find either the least number of steps to reach the target point (steplimit = 0), or count the
        number of reachable nodes within [steplimit > 0] steps."""
        currentpoint = Point(1, 1)
        seen = set()
        queue: list[tuple[Point, int]] = [(currentpoint, 0)]
        while queue:
            currentpoint, steps = queue.pop(0)
            if not steplimit and currentpoint == targetpoint:
                return steps
            if currentpoint in seen or (steplimit and steps > steplimit):
                continue
            seen.add(currentpoint)
            for p in currentpoint.get_neighbors(self.__favorite_nbr):
                queue.append((p, steps + 1))
        return len(seen)


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        maze = CubicleMaze(int(file.read().strip('\n')))
    print(f"Part 1: {maze.get_count()}")
    print(f"Part 2: {maze.get_count(Point(0, 0), 50)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
