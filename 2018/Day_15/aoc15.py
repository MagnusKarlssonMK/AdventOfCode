"""
Small rant - 2018 AoC was already kind of annoying, and day 15 didn't help; easily my least favorite puzzle I've come
across yet. Mainly because of the incredibly verbose description, and yet making it really hard to understand the rules.

Certainly not a fast solution, I just can't be bothered to try to improve it right now, and a better solution would
kill fewer elfs in the simulation, which wouldn't feel like much of a win.
"""
import sys
from dataclasses import dataclass
from heapq import heappop, heappush
from copy import deepcopy


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def get_adjacent(self) -> list["Point"]:
        return [self + Point(dx, dy) for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1))]

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:  # This does the heavy lifting to do the 'reading order' sorting
        return self.y < other.y if self.y != other.y else self.x < other.x


@dataclass
class Unit:
    position: Point
    team: str
    power: int = 3
    hp: int = 200

    def __lt__(self, other: "Unit") -> bool:
        return self.position < other.position


class Cavern:
    def __init__(self, rawstr: str) -> None:
        self.__cavern = set()
        self.__units = []
        for y, line in enumerate(rawstr.splitlines()):
            for x, char in enumerate(line):
                if char != "#":
                    self.__cavern.add(Point(x, y))
                    if char in ("E", "G"):
                        self.__units.append(Unit(Point(x, y), char))
        self.__start_units = deepcopy(self.__units)

    def __reset_units(self, elfpower: int = 3):
        self.__units = deepcopy(self.__start_units)
        for u in self.__units:
            if u.team == 'E':
                u.power = elfpower

    def __move(self, unit: Unit) -> bool:
        """Returns False if there are no targets left, otherwise true."""
        unit_points = {u.position for u in self.__units if u.position != unit.position and u.hp > 0}
        targets = [t for t in self.__units if t.team != unit.team and t.hp > 0]
        if not targets:
            return False
        available_points = self.__cavern ^ unit_points
        target_points = set()
        for target in targets:
            for adj in target.position.get_adjacent():
                if adj in available_points:
                    target_points.add(adj)
        if not target_points or unit.position in target_points:
            return True
        shortest_paths = []  # Store as list in case there are multiple paths with the same shortest length
        seen = set()
        queue = [(0, [unit.position])]
        while queue:
            steps, path = heappop(queue)
            if len(shortest_paths) > 0 and len(path) > len(shortest_paths[0]):
                continue
            if path[-1] in target_points:
                shortest_paths.append(path)
                continue
            if len(path) > 1:  # Couple seen points with the first point in the path, as we need to select that later
                if (path[-1], path[1]) in seen:
                    continue
                seen.add((path[-1], path[1]))
            for nextpoint in path[-1].get_adjacent():
                if nextpoint in available_points and nextpoint not in path:
                    heappush(queue, (steps + 1, path + [nextpoint]))
        if len(shortest_paths) > 0:
            found_targets = {t[-1] for t in shortest_paths}
            selected_target = sorted(list(found_targets))[0]
            newpoints = {t[1] for t in shortest_paths if t[-1] == selected_target}
            unit.position = sorted(list(newpoints))[0]
        return True

    def __attack(self, unit: Unit) -> None:
        targets = [t for t in self.__units if t.team != unit.team and t.hp > 0]
        if not targets:
            return
        target_points = set()
        for target in targets:
            for adj in target.position.get_adjacent():
                target_points.add(adj)
        if unit.position in target_points:
            # Find the target unit(s), sort if more than one, and smack it
            surrounding_points = unit.position.get_adjacent()
            enemies = sorted([(e.hp, e) for e in targets if e.position in surrounding_points])
            # Note: stored as tuple with hp so that it gets sorted according to HP first and reading order second
            if enemies:
                enemies[0][1].hp -= unit.power

    def __playround(self) -> bool:
        """Returns False if round ended before all units made their move, otherwise True."""
        game_ended = False
        for unit in sorted(self.__units):
            if unit.hp <= 0:
                continue
            if not self.__move(unit):
                game_ended = True
                break
            self.__attack(unit)
        # Remove dead units
        self.__units = [unit for unit in self.__units if unit.hp > 0]
        return not game_ended

    def __printgrid(self):
        """Only for temporary debugging, kept here for posterity."""
        x_max = max([p.x for p in self.__cavern])
        y_max = max([p.y for p in self.__cavern])
        grid = [['#' for _ in range(x_max + 2)] for _ in range(y_max + 2)]
        for n in self.__cavern:
            grid[n.y][n.x] = ' '
        for u in self.__units:
            grid[u.position.y][u.position.x] = u.team
        [print(''.join(line)) for line in grid]
        [print(u) for u in sorted(self.__units)]
        print()

    def __game_over(self) -> bool:
        return len({unit.team for unit in self.__units}) < 2

    def get_combat_outcome(self) -> tuple[int, str]:
        # self.__printgrid()
        rounds = 0
        while not self.__game_over():
            if self.__playround():
                rounds += 1
            # print(rounds)
            # self.__printgrid()
        return rounds * sum([u.hp for u in self.__units]), self.__units[0].team

    def get_boosted_elfs_outcome(self) -> int:
        power = 4
        self.__reset_units(power)
        elfcount = sum([1 for u in self.__units if u.team == 'E'])
        while True:
            outcome, winner = self.get_combat_outcome()
            if winner == 'E' and sum([1 for u in self.__units if u.team == 'E']) == elfcount:
                # This could probably be made quite a bit faster by aborting each combat as soon as a single elf dies
                # At this point, I just can't move on from this puzzle fast enough, and will happily sacrifice a
                # few elfs.
                return outcome
            power += 1
            self.__reset_units(power)


def main() -> int:
    with open('../Inputfiles/aoc15.txt', 'r') as file:
        cavern = Cavern(file.read().strip('\n'))
    print(f"Part 1: {cavern.get_combat_outcome()[0]}")
    print(f"Part 2: {cavern.get_boosted_elfs_outcome()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
