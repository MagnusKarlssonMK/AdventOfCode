"""
- Step 1: Parse the input grid into a coordinate dictionary of what possible neighbor points are, and where keys and
doors are. Also treat the start point as a key, as we will need that in the next step.
- Step 2: Use the coordinate map to build a map of how the key locations (including the starting point) are connected;
number of steps and doors to pass. Note that there can in theory exist multiple paths between any two keys, with
different key requirements.
- Step 3: Use the key map to perform a Dijkstra search to find the least nbr of steps required to collect all keys from
the starting point. This will give the answer to Part 1.
- Step 4: Update the grid according to the description, and then pretty much repeat previous steps with the amended map,
with the key difference that there are now 4 start points, and the state space for step 3 contains 4 moving parts
instead of just one. This will give the answer to Part 2.

Note: Quite a bit of duplicated code between Part1 and Part2 functions, can probably be cleaned up a bit.
"""
import time
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from heapq import heappop, heappush
from copy import deepcopy


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


class TileType(Enum):
    OPEN = 0
    KEY = 1
    DOOR = 2


@dataclass
class Tile:
    type: TileType
    value: str
    neighbors: set[Point]


class Vault:
    def __init__(self, rawstr: str) -> None:
        self.__tiles: dict[Point, Tile] = {}
        self.__keys: dict[str, Point] = {}
        startpoint: Point = Point(-1, -1)
        for y, line in enumerate(rawstr.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    continue
                elif c == ".":
                    self.__tiles[Point(x, y)] = Tile(TileType.OPEN, '', set())
                elif c == "@":
                    self.__tiles[Point(x, y)] = Tile(TileType.KEY, c, set())
                    startpoint = Point(x, y)
                    self.__keys[c] = Point(x, y)
                elif c.islower():
                    self.__tiles[Point(x, y)] = Tile(TileType.KEY, c, set())
                    self.__keys[c] = Point(x, y)
                elif c.isupper():
                    self.__tiles[Point(x, y)] = Tile(TileType.DOOR, c, set())

        for point in self.__tiles:
            for n in (Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)):
                if (newpoint := point + n) in self.__tiles:
                    self.__tiles[point].neighbors.add(newpoint)

        # Create an alternative updated map around the starting position for part 2
        self.__four_tiles = deepcopy(self.__tiles)
        self.__four_keys = deepcopy(self.__keys)
        blocked = (startpoint, Point(startpoint.x, startpoint.y - 1), Point(startpoint.x, startpoint.y + 1),
                   Point(startpoint.x - 1, startpoint.y), Point(startpoint.x + 1, startpoint.y))
        for b in blocked:
            self.__four_tiles.pop(b)
        for y in range(startpoint.y - 2, startpoint.y + 3):
            for x in range(startpoint.x - 2, startpoint.x + 3):
                if (p := Point(x, y)) in self.__four_tiles:
                    for b in blocked:
                        if b in self.__four_tiles[p].neighbors:
                            self.__four_tiles[p].neighbors.remove(b)
        self.__four_keys['@'] = Point(startpoint.x - 1, startpoint.y - 1)
        self.__four_tiles[Point(startpoint.x - 1, startpoint.y - 1)] = (
            Tile(TileType.KEY, '@', self.__four_tiles[Point(startpoint.x - 1, startpoint.y - 1)].neighbors))
        self.__four_keys['£'] = Point(startpoint.x + 1, startpoint.y - 1)
        self.__four_tiles[Point(startpoint.x + 1, startpoint.y - 1)] = (
            Tile(TileType.KEY, '£', self.__four_tiles[Point(startpoint.x + 1, startpoint.y - 1)].neighbors))
        self.__four_keys['$'] = Point(startpoint.x - 1, startpoint.y + 1)
        self.__four_tiles[Point(startpoint.x - 1, startpoint.y + 1)] = (
            Tile(TileType.KEY, '$', self.__four_tiles[Point(startpoint.x - 1, startpoint.y + 1)].neighbors))
        self.__four_keys['%'] = Point(startpoint.x + 1, startpoint.y + 1)
        self.__four_tiles[Point(startpoint.x + 1, startpoint.y + 1)] = (
            Tile(TileType.KEY, '%', self.__four_tiles[Point(startpoint.x + 1, startpoint.y + 1)].neighbors))

    def get_steps_all_keys_one_room(self) -> int:
        # Create dict of connections between keys
        keypaths: dict[str, set[tuple[str, int, str]]] = {k: set() for k in self.__keys}  # key : key, steps, doors
        for k in self.__keys:
            seen: set[tuple[Point, str]] = set()
            queue = [(self.__keys[k], '', Point(-1, -1), 0)]
            while queue:
                current, doors, previous, steps = queue.pop(0)
                if (current, doors) in seen:
                    continue
                seen.add((current, doors))
                if self.__tiles[current].type == TileType.KEY and self.__tiles[current].value != k:
                    keypaths[k].add((self.__tiles[current].value, steps, doors))
                    continue
                if self.__tiles[current].type == TileType.DOOR:
                    doors = ''.join(sorted(doors + self.__tiles[current].value.lower()))
                for n in self.__tiles[current].neighbors:
                    if n != previous:
                        queue.append((n, doors, current, steps + 1))
        # Use the key connection dict for a Dijkstra search for shortest way to collect all keys
        visited: dict[tuple[str, str], int] = {}
        pqueue: list[tuple[int, str, str]] = []
        heappush(pqueue, (0, '@', ''))
        while pqueue:
            steps, current_key, have_keys = heappop(pqueue)
            have_keys = ''.join(sorted(set(have_keys + current_key)))
            if len(have_keys) == len(self.__keys):
                return steps
            if (current_key, have_keys) in visited and visited[(current_key, have_keys)] <= steps:
                continue
            visited[(current_key, have_keys)] = steps
            for n, cost, doors in keypaths[current_key]:
                if set(doors).issubset(set(have_keys)):
                    heappush(pqueue, (steps + cost, n, have_keys))
        return -1

    def get_steps_all_keys_four_rooms(self) -> int:
        # Create dict of connections between keys
        keypaths: dict[str, set[tuple[str, int, str]]] = {k: set() for k in self.__four_keys}  # key : key, steps, doors
        for k in self.__four_keys:
            seen: set[tuple[Point, str]] = set()
            queue = [(self.__four_keys[k], '', Point(-1, -1), 0)]
            while queue:
                current, doors, previous, steps = queue.pop(0)
                if (current, doors) in seen:
                    continue
                seen.add((current, doors))
                if self.__four_tiles[current].type == TileType.KEY and self.__four_tiles[current].value != k:
                    keypaths[k].add((self.__four_tiles[current].value, steps, doors))
                    continue
                if self.__four_tiles[current].type == TileType.DOOR:
                    doors = ''.join(sorted(doors + self.__four_tiles[current].value.lower()))
                for n in self.__four_tiles[current].neighbors:
                    if n != previous:
                        queue.append((n, doors, current, steps + 1))
        # Use the key connection dict for a Dijkstra search for shortest way to collect all keys
        visited: dict[tuple[tuple[str, ...], str], int] = {}
        pqueue: list[tuple[int, tuple[str, ...], str]] = []
        heappush(pqueue, (0, ('@', '£', '$', '%'), ''))
        while pqueue:
            steps, current_key, have_keys = heappop(pqueue)
            have_keys = ''.join(sorted(set(have_keys + ''.join(current_key))))
            if len(have_keys) == len(self.__four_keys):
                return steps
            if (current_key, have_keys) in visited and visited[(current_key, have_keys)] <= steps:
                continue
            visited[(current_key, have_keys)] = steps
            for i, ck in enumerate(current_key):
                for n, cost, doors in keypaths[ck]:
                    if set(doors).issubset(set(have_keys)):
                        nextkey = list(current_key)
                        nextkey[i] = n
                        heappush(pqueue, (steps + cost, tuple(nextkey), have_keys))
        return -1


def main(aoc_input: str) -> None:
    vault = Vault(aoc_input)
    print(f"Part 1: {vault.get_steps_all_keys_one_room()}")
    print(f"Part 2: {vault.get_steps_all_keys_four_rooms()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day18.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
