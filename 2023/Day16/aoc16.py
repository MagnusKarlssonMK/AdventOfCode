import sys
import re
import timeit

RowCol = tuple[int, int]
Directions: dict[str: RowCol] = {'u': (-1, 0), 'r': (0, 1), 'd': (1, 0), 'l': (0, -1)}


class Bouncer:
    def __init__(self, mchar: str):
        self.mtype = mchar  # |, -, /, \

    def bouncelight(self, indir: Directions) -> iter:
        match self.mtype:
            case '-':
                if indir == Directions['l'] or indir == Directions['r']:
                    yield indir
                else:
                    yield Directions['l']
                    yield Directions['r']
            case '|':
                if indir == Directions['u'] or indir == Directions['d']:
                    yield indir
                else:
                    yield Directions['d']
                    yield Directions['u']
            case '/':
                if indir == Directions['r']:
                    yield Directions['u']
                elif indir == Directions['u']:
                    yield Directions['r']
                elif indir == Directions['l']:
                    yield Directions['d']
                elif indir == Directions['d']:
                    yield Directions['l']
            case '\\':
                if indir == Directions['r']:
                    yield Directions['d']
                elif indir == Directions['d']:
                    yield Directions['r']
                elif indir == Directions['l']:
                    yield Directions['u']
                elif indir == Directions['u']:
                    yield Directions['l']

    def __repr__(self):
        return self.mtype


class Grid:
    def __init__(self, rawstr: str):
        self.__bouncers: dict[RowCol: Bouncer] = {}
        self.__bouncersperrow: dict[int: list[int]] = {}
        self.__bouncerspercol: dict[int: list[int]] = {}
        grid = []
        for row, line in enumerate(rawstr.splitlines()):
            grid.append(line)
            for c in re.finditer(r"[^.]", line):
                self.__bouncers[(row, int(c.start()))] = Bouncer(c.group(0))
                try:
                    self.__bouncersperrow[row].append(int(c.start()))
                except KeyError:
                    self.__bouncersperrow[row] = [int(c.start())]
                try:
                    self.__bouncerspercol[int(c.start())].append(row)
                except KeyError:
                    self.__bouncerspercol[int(c.start())] = [row]
        self.width = len(grid)
        self.height = len(grid[0])
        self.__lightgrid: list[list[int]] = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.__adj: dict[tuple[RowCol, Directions]: set[tuple[RowCol, Directions]]] = {}
        for vertex in list(self.__bouncers.keys()):
            for indir in list(Directions.values()):
                outdir = []
                [outdir.append(d) for d in self.__bouncers[vertex].bouncelight(indir)]
                if indir not in outdir:
                    if (vertex, indir) not in self.__adj:
                        self.__adj[(vertex, indir)] = set()
                    [self.__adj[(vertex, indir)].add((self.__getnextpos(vertex, out), out)) for out in outdir]

    def insertlight(self, pos: RowCol, direction: Directions) -> int:
        """Inserts a light source at the given position and direction, returns the score and resets the grid."""
        visited: set[tuple[RowCol, Directions]] = set()
        if pos in list(self.__bouncers.keys()):  # If starting on a bouncer
            lightqueue = [(pos, direction, 0)]
        else:
            nextpos = self.__getnextpos(pos, direction)
            lightqueue = [(nextpos, direction, 1)]
            visited.add((pos, direction))
            self.__updatelightgrid(pos, nextpos)

        while len(lightqueue) > 0:
            headpos, headdir, headdist = lightqueue.pop(0)
            if (headpos, headdir) not in visited:
                try:
                    for adj in self.__adj[(headpos, headdir)]:
                        lightqueue.append((adj[0], adj[1], headdist))
                        self.__updatelightgrid(headpos, adj[0])
                except KeyError:  # Happens if we run into the grid edge - do nothing
                    pass
                visited.add((headpos, headdir))
        score = self.__getlightscore()
        for line in self.__lightgrid:
            print(line)
        self.__resetlightgrid()
        return score

    def __getnextpos(self, pos: RowCol, direction: Directions) -> RowCol:
        if direction == Directions['r']:
            cols = sorted(list(filter(lambda x: x > pos[1], self.__bouncersperrow[pos[0]])))
            for i in cols:
                bounced = []
                [bounced.append(d) for d in self.__bouncers[(pos[0], i)].bouncelight(direction)]
                if direction not in bounced:
                    return pos[0], i
            return pos[0], self.width - 1
        elif direction == Directions['l']:
            cols = sorted(list(filter(lambda x: x < pos[1], self.__bouncersperrow[pos[0]])), reverse=True)
            for i in cols:
                bounced = []
                [bounced.append(d) for d in self.__bouncers[(pos[0], i)].bouncelight(direction)]
                if direction not in bounced:
                    return pos[0], i
            return pos[0], 0
        elif direction == Directions['u']:
            rows = sorted(list(filter(lambda x: x < pos[0], self.__bouncerspercol[pos[1]])), reverse=True)
            for i in rows:
                bounced = []
                [bounced.append(d) for d in self.__bouncers[(i, pos[1])].bouncelight(direction)]
                if direction not in bounced:
                    return i, pos[1]
            return 0, pos[1]
        elif direction == Directions['d']:
            rows = sorted(list(filter(lambda x: x > pos[0], self.__bouncerspercol[pos[1]])))
            for i in rows:
                bounced = []
                [bounced.append(d) for d in self.__bouncers[(i, pos[1])].bouncelight(direction)]
                if direction not in bounced:
                    return i, pos[1]
            return self.height - 1, pos[1]
        return -1, -1

    def __updatelightgrid(self, frompos: RowCol, topos: RowCol) -> None:
        startrow = min(frompos[0], topos[0])
        startcol = min(frompos[1], topos[1])
        for drow in range(abs(frompos[0] - topos[0]) + 1):
            for dcol in range(abs(frompos[1] - topos[1]) + 1):
                self.__lightgrid[startrow + drow][startcol + dcol] = 1

    def __getlightscore(self) -> int:
        return sum([sum(row) for row in self.__lightgrid])

    def __resetlightgrid(self) -> None:
        self.__lightgrid = [[0 for _ in range(self.width)] for _ in range(self.height)]


def main() -> int:
    starttime = timeit.default_timer()
    with open('aoc16.txt', 'r') as file:
        mygrid = Grid(file.read().strip('\n'))
        inittime = timeit.default_timer()
    print("Init time: ", inittime - starttime)
    p1 = mygrid.insertlight((0, 0), Directions['r'])
    p1time = timeit.default_timer()
    print("Insert time: ", p1time - inittime)
    print("Part1: ", p1)
    """
    # Part 2
    p2 = 0
    for row in range(mygrid.height):
        p2 = max(p2, mygrid.insertlight((row, 0), Directions['r']))
        p2 = max(p2, mygrid.insertlight((row, mygrid.width - 1), Directions['l']))
    for col in range(mygrid.width):
        p2 = max(p2, mygrid.insertlight((0, col), Directions['d']))
        p2 = max(p2, mygrid.insertlight((mygrid.height - 1, col), Directions['u']))
    p2time = timeit.default_timer()
    print("P2 time: ", p2time - p1time)
    print("Part2: ", p2) """
    return 0


if __name__ == "__main__":
    sys.exit(main())
