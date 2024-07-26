"""
Well this became a mess.
I probably overthought and wound up with an unnecessarily complicated way of representing the tile edges, so when
re-asssembling the image it gets really wonky.

This solution also assumes that all edges are unique, i.e. that all tiles have exactly one possible neighbor in the
directions that a neighbor exists, and none on the border edges.
"""
import sys
from itertools import combinations
from math import prod
from dataclasses import dataclass
from enum import Enum


class Directions(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def get_opposite(self) -> "Directions":
        return Directions((self.value + 2) % 4)


@dataclass
class Edge:
    value: str
    neighbors: set[tuple[int, bool]]    # tile-id, is-mirror-state

    def get_reverse(self) -> str:
        return self.value[::-1]

    def match_edges(self, other: "Edge") -> bool:
        return self.value == other.get_reverse()


class Tile:
    def __init__(self, tileid: int, grid: list[str]) -> None:
        self.__id = tileid
        self.__grid = tuple([grid[line][1:-1] for line in range(1, len(grid) - 1)])
        # self.__grid = tuple([grid[line] for line in range(len(grid))])
        self.__edges: dict[Directions: Edge] = {Directions.UP: Edge(grid[0], set()),
                                                Directions.RIGHT: Edge(''.join([g[-1] for g in grid]), set()),
                                                Directions.DOWN: Edge(grid[-1][::-1], set()),
                                                Directions.LEFT: Edge(''.join([g[0] for g in reversed(grid)]), set())}
        self.__reversed = False

    def add_neighbor(self, other: "Tile") -> None:
        for e1 in self.__edges.values():
            for e2 in other.__edges.values():
                if e1.value == e2.value:
                    e1.neighbors.add((other.__id, False))
                if e1.value == e2.get_reverse():
                    e1.neighbors.add((other.__id, True))

    def get_neighbor(self, direction: Directions) -> tuple[int, bool]:
        for n in self.__edges[direction].neighbors:
            return n
        return -1, False

    def is_edge_match(self, other: "Tile", d: Directions) -> bool:
        return self.__edges[d].match_edges(other.__edges[d.get_opposite()])

    def get_neighbor_count(self) -> int:
        return sum([len(e.neighbors) for e in self.__edges.values()])

    def get_neighbor_directions(self) -> set[Directions]:
        return {e for e in self.__edges if len(self.__edges[e].neighbors) > 0}

    def rotate(self) -> None:
        newgrid = ['' for _ in range(len(self.__grid[0]))]
        for line in self.__grid:
            for i, c in enumerate(line):
                newgrid[i] = c + newgrid[i]
        self.__grid = newgrid
        (self.__edges[Directions.UP], self.__edges[Directions.RIGHT],
         self.__edges[Directions.DOWN], self.__edges[Directions.LEFT]) = \
            (self.__edges[Directions.LEFT], self.__edges[Directions.UP],
             self.__edges[Directions.RIGHT], self.__edges[Directions.DOWN])

    def flip(self) -> None:
        self.__grid = [line[::-1] for line in self.__grid]
        self.__edges[Directions.LEFT], self.__edges[Directions.RIGHT] = \
            (self.__edges[Directions.RIGHT], self.__edges[Directions.LEFT])
        for edge in self.__edges.values():
            edge.value = edge.get_reverse()
            buffer = set()
            for n in edge.neighbors:
                buffer.add((n[0], not n[1]))
            edge.neighbors = buffer
        self.__reversed = not self.__reversed

    def get_grid(self):
        return tuple(self.__grid)


class Image:
    def __init__(self, rawstr: str) -> None:
        self.__tiles: dict[int: Tile] = {}
        for tile in rawstr.split('\n\n'):
            lines = tile.splitlines()
            tileid = int(lines[0].split()[1].strip(':'))
            self.__tiles[tileid] = Tile(tileid, lines[1:])
        for t1, t2 in combinations(self.__tiles, 2):
            self.__tiles[t1].add_neighbor(self.__tiles[t2])
            self.__tiles[t2].add_neighbor(self.__tiles[t1])
        self.__corners = []
        self.__image = []

    def get_corner_checksum(self) -> int:
        for tileid, tile in self.__tiles.items():
            if tile.get_neighbor_count() == 2:
                self.__corners.append(tileid)
        return prod(self.__corners)

    def __generate_image(self) -> int:
        start = self.__tiles[min(self.__corners)]
        while len({Directions.RIGHT, Directions.DOWN} & start.get_neighbor_directions()) < 2:
            start.rotate()

        placed_tiles = [[start]]
        row = 0
        col = 1
        corners = 1
        maxcol = -1
        while corners < 4:
            ndir = Directions.RIGHT if col > 0 else Directions.DOWN
            previous = placed_tiles[row][col - 1] if col > 0 else placed_tiles[row - 1][col]
            n, flip = previous.get_neighbor(ndir)
            nexttile = self.__tiles[n]
            if not flip:  # matching edges need to be opposite
                nexttile.flip()
            while not previous.is_edge_match(nexttile, ndir):
                nexttile.rotate()
            if col > 0:
                placed_tiles[row].append(nexttile)
            else:
                placed_tiles.append([nexttile])
            if nexttile.get_neighbor_count() < 3:
                corners += 1
                if col > 0:
                    maxcol = col
            if 0 < maxcol <= col:
                col = 0
                row += 1
            else:
                col += 1

        for row in placed_tiles:
            tmp = ['' for _ in range(len(row[0].get_grid()))]
            for tile in row:
                for i, gridrow in enumerate(tile.get_grid()):
                    tmp[i] += gridrow
            self.__image += tmp
        return -1

    def get_water_roughness(self) -> int:
        self.__generate_image()
        total_points = sum([line.count('#') for line in self.__image])
        monster_shapes = [['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']]
        # Rotate the monster rather than the image - Generate the 4 different monster rotations
        for _ in range(3):
            newgrid = ['' for _ in range(len(monster_shapes[-1][0]))]
            for line in monster_shapes[-1]:
                for i, c in enumerate(line):
                    newgrid[i] = c + newgrid[i]
            monster_shapes.append(newgrid)
        # ... and the mirrors for each rotation
        for m in range(4):
            monster_shapes.append([line[::-1] for line in monster_shapes[m]])
        # For each monster shape, convert it to a set of coordinates and scan the image, store matching points in set
        monster_points = set()
        for monster in monster_shapes:
            m = [(row, col) for row, line in enumerate(monster) for col, c in enumerate(line) if c == "#"]
            m_width = len(monster[0])
            m_height = len(monster)
            for row in range(len(self.__image) - m_height):
                for col in range(len(self.__image[0]) - m_width):
                    points = [(row + m_r, col + m_c) for m_r, m_c in m]
                    if all([self.__image[r][c] == "#" for r, c in points]):
                        monster_points |= set(points)
        return total_points - len(monster_points)


def main() -> int:
    with open('../Inputfiles/aoc20.txt', 'r') as file:
        img = Image(file.read().strip('\n'))
    print(f"Part 1: {img.get_corner_checksum()}")
    print(f"Part 2: {img.get_water_roughness()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
