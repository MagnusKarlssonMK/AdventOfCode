"""
Store the bouncers in a Grid class, along with per-row and per-column dicts for faster lookups and filtering when
looking for the next possible step. Also creates an adjacency list of the bouncers coupled with the incoming direction,
i.e. every bouncer can exist in 2 / 4 entries (depending on the type of bouncer). Then, when a light source is added,
a stripped down BFS is used to traverse the bouncers and record the movement. This traversal needs to keep track of
when entering a bouncer in a direction that has already been seen and then not continue that path, since that would
otherwise likely create an endless loop.
"""
import time
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from collections.abc import Generator


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def rotate_right(self) -> "Point":
        return Point(-self.y, self.x)

    def rotate_left(self) -> "Point":
        return Point(self.y, -self.x)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class Direction(Enum):
    UP = Point(0, -1)
    RIGHT = Point(1, 0)
    DOWN = Point(0, 1)
    LEFT = Point(-1, 0)


class BouncerType(Enum):
    HOR_SPLIT = '-'
    VER_SPLIT = '|'
    FWD_BOUNCE = '/'
    BCK_BOUNCE = '\\'

    def bounce_light(self, indir: Direction) -> Generator[Direction]:
        match self:
            case BouncerType.HOR_SPLIT:
                if indir in (Direction.LEFT, Direction.RIGHT):
                    yield indir
                else:
                    yield Direction.LEFT
                    yield Direction.RIGHT
            case BouncerType.VER_SPLIT:
                if indir in (Direction.UP, Direction.DOWN):
                    yield indir
                else:
                    yield Direction.DOWN
                    yield Direction.UP
            case BouncerType.FWD_BOUNCE:
                if indir in (Direction.UP, Direction.DOWN):
                    yield Direction(indir.value.rotate_right())
                else:
                    yield Direction(indir.value.rotate_left())
            case BouncerType.BCK_BOUNCE:
                if indir in (Direction.UP, Direction.DOWN):
                    yield Direction(indir.value.rotate_left())
                else:
                    yield Direction(indir.value.rotate_right())


class Grid:
    def __init__(self, rawstr: str) -> None:
        self.__bouncers: dict[Point, BouncerType] = {}
        self.__bouncersperrow: dict[int, list[int]] = {}
        self.__bouncerspercol: dict[int, list[int]] = {}
        grid: list[str] = []
        for y, line in enumerate(rawstr.splitlines()):
            grid.append(line)
            for x, c in enumerate(line):
                if c == '.': #not in ['-', '|', '/', '\\']: #BouncerType:
                    continue
                self.__bouncers[Point(x, y)] = BouncerType(c)
                if y in self.__bouncersperrow:
                    self.__bouncersperrow[y].append(x)
                else:
                    self.__bouncersperrow[y] = [x]
                if x in self.__bouncerspercol:
                    self.__bouncerspercol[x].append(y)
                else:
                    self.__bouncerspercol[x] = [y]
        self.__width = len(grid[0])
        self.__height = len(grid)
        self.__lit_tiles: set[Point] = set()
        self.__adj: dict[tuple[Point, Direction], set[tuple[Point, Direction]]] = {}
        for b in self.__bouncers:
            for indir in Direction:
                outdir = [d for d in self.__bouncers[b].bounce_light(indir)]
                if indir not in outdir:
                    if (b, indir) not in self.__adj:
                        self.__adj[(b, indir)] = set()
                    for out in outdir:
                        if (nextpos := self.__get_nextpos(b, out)) != b:
                            self.__adj[(b, indir)].add((nextpos, out))

    def __insert_light(self, pos: Point, direction: Direction) -> int:
        """Inserts a light source at the given position and direction and returns the score."""
        visited: set[tuple[Point, Direction]] = set()
        if pos in self.__bouncers:  # If starting on a bouncer
            lightqueue = [(pos, direction)]
        else:
            nextpos = self.__get_nextpos(pos, direction)
            lightqueue = [(nextpos, direction)]
            visited.add((pos, direction))
            self.__update_lightgrid(pos, nextpos)

        while lightqueue:
            headpos, headdir = lightqueue.pop(0)
            if (headpos, headdir) not in visited:
                if (headpos, headdir) in self.__adj:
                    for n_p, n_d in self.__adj[(headpos, headdir)]:
                        lightqueue.append((n_p, n_d))
                        self.__update_lightgrid(headpos, n_p)
                visited.add((headpos, headdir))
        score = self.__get_lightscore()
        self.__reset_lightgrid()
        return score

    def __get_nextpos(self, pos: Point, direction: Direction) -> Point:
        if direction == Direction.RIGHT:
            cols = sorted(list(filter(lambda x: x > pos.x, self.__bouncersperrow[pos.y])))
            for i in cols:
                bounced = [d for d in self.__bouncers[Point(i, pos.y)].bounce_light(direction)]
                if direction not in bounced:
                    return Point(i, pos.y)
            return Point(self.__width - 1, pos.y)
        elif direction == Direction.LEFT:
            cols = sorted(list(filter(lambda x: x < pos.x, self.__bouncersperrow[pos.y])), reverse=True)
            for i in cols:
                bounced = [d for d in self.__bouncers[Point(i, pos.y)].bounce_light(direction)]
                if direction not in bounced:
                    return Point(i, pos.y)
            return Point(0, pos.y)
        elif direction == Direction.UP:
            rows = sorted(list(filter(lambda x: x < pos.y, self.__bouncerspercol[pos.x])), reverse=True)
            for i in rows:
                bounced = [d for d in self.__bouncers[Point(pos.x, i)].bounce_light(direction)]
                if direction not in bounced:
                    return Point(pos.x, i)
            return Point(pos.x, 0)
        elif direction == Direction.DOWN:
            rows = sorted(list(filter(lambda x: x > pos.y, self.__bouncerspercol[pos.x])))
            for i in rows:
                bounced = [d for d in self.__bouncers[Point(pos.x, i)].bounce_light(direction)]
                if direction not in bounced:
                    return Point(pos.x, i)
            return Point(pos.x, self.__height - 1)
        return Point(-1, -1)

    def __update_lightgrid(self, frompos: Point, topos: Point) -> None:
        startrow = min(frompos.y, topos.y)
        startcol = min(frompos.x, topos.x)
        for drow in range(abs(frompos.y - topos.y) + 1):
            for dcol in range(abs(frompos.x - topos.x) + 1):
                self.__lit_tiles.add(Point(startcol + dcol, startrow + drow))

    def __get_lightscore(self) -> int:
        return len(self.__lit_tiles)

    def __reset_lightgrid(self) -> None:
        self.__lit_tiles = set()

    def get_energized_tiles(self) -> int:
        return self.__insert_light(Point(0, 0), Direction.RIGHT)

    def get_max_energized_tiles(self) -> int:
        result = 0
        for y in range(self.__height):
            result = max(result, self.__insert_light(Point(0, y), Direction.RIGHT))
            result = max(result, self.__insert_light(Point(self.__width - 1, y), Direction.LEFT))
        for x in range(self.__width):
            result = max(result, self.__insert_light(Point(x, 0), Direction.DOWN))
            result = max(result, self.__insert_light(Point(x, self.__height - 1), Direction.UP))
        return result


def main(aoc_input: str) -> None:
    mygrid = Grid(aoc_input)
    print(f"Part 1: {mygrid.get_energized_tiles()}")
    print(f"Part 2: {mygrid.get_max_energized_tiles()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day16.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
