"""
Surprisingly straightforward - pretty much just parse the reindeers into a class that gives a method to calculate
distance based on time.
For part 2 we simply need to simulate the race second-for-second and award points along the way. The only minor thing
to keep in mind is that the time loop needs to start at 1 to avoid awarding points on the starting line, and to run
until 2503+1 to compensate for python's range not including the last value.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day14.txt')


@dataclass(frozen=True)
class Reindeer:
    speed: int
    time: int
    rest: int

    def get_distance(self, time: int) -> int:
        cycle_time = (self.time + self.rest)
        cycles = time // cycle_time
        remainder = time % cycle_time
        total = self.speed * ((cycles * self.time) + min(remainder, self.time))
        return total


class Olympics:
    def __init__(self, rawstr: str) -> None:
        self.__reindeers: dict[str: Reindeer] = {}
        for line in rawstr.splitlines():
            nbrs = list(map(int, re.findall(r"\d+", line)))
            name = line.split()[0]
            self.__reindeers[name] = Reindeer(nbrs[0], nbrs[1], nbrs[2])

    def get_winner_distance(self, new_scoring: bool = False, time: int = 2503) -> int:
        if not new_scoring:
            return max([self.__reindeers[r].get_distance(time) for r in self.__reindeers])
        scoretable: dict[str: int] = {r: 0 for r in self.__reindeers}
        for seconds in range(1, time + 1):  # Start on 1, so we don't award points at the starting line!
            leader_dist = 0
            leaders = []
            for r in self.__reindeers:
                newdist = self.__reindeers[r].get_distance(seconds)
                if newdist > leader_dist:
                    leaders = [r]
                    leader_dist = newdist
                elif newdist == leader_dist:
                    leaders.append(r)
            for lead in leaders:
                scoretable[lead] += 1
        return max(scoretable.values())


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        olympics = Olympics(file.read().strip('\n'))
    print(f"Part 1: {olympics.get_winner_distance()}")
    print(f"Part 2: {olympics.get_winner_distance(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
