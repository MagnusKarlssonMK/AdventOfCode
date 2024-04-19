"""
Gets the job done, but definitely not fast. Attempts to optimize the state branches by
- Only continuing a branch if it can theoretically improve the current best
- Don't build anything in the last minute, and only build geode robots (if possible) in the second last minute,
  as there won't be any time left to use the additional resources.
- Keep track of when choosing not to build anything even when we could, and don't build that robot again until we
  spend a resource it uses to build something else ('skip flag' in state).
- Throw away robots and resources that won't be of any use with the remaining time, to increase the chances of finding
  overlap with already seen branches.
"""
import sys
from enum import Enum
from dataclasses import dataclass
from collections import deque
import math


class Minerals(Enum):
    ORE = 'ore'
    CLAY = 'clay'
    OBSIDIAN = 'obsidian'
    GEODE = 'geode'


class Blueprint:
    def __init__(self, rawstr: str):
        bpid, costs = rawstr.split(': ')
        self.id = int(bpid.strip('Blueprint '))
        self.costs: dict[str: list[tuple[int, str]]] = {}
        self.maxcosts: dict[str: int] = {}
        for cost in costs.strip('.').split('. '):
            dest, source = cost.split(' robot costs ')
            dest = Minerals(dest.split()[1])
            self.costs[dest] = []
            for s in source.split(' and '):
                nbr, mineral = s.split()
                nbr = int(nbr)
                mineral = Minerals(mineral)
                self.costs[dest].append((nbr, mineral))
                if mineral in self.maxcosts:
                    self.maxcosts[mineral] = max(self.maxcosts[mineral], nbr)
                else:
                    self.maxcosts[mineral] = nbr

    def get_affordable(self, resources: dict[str: int]) -> iter:
        for robottype in self.costs:
            if all([resources[mat] >= count for count, mat in self.costs[robottype]]):
                yield robottype

    def get_maxcost(self, mineral: Minerals) -> int:
        if mineral in self.maxcosts:
            return self.maxcosts[mineral]
        return 0


@dataclass(frozen=True)
class MiniState:
    time_remaining: int = 0
    ore: tuple[int, int] = (0, 1)  # Mineral count, robot count
    clay: tuple[int, int] = (0, 0)
    obsidian: tuple[int, int] = (0, 0)
    geode: tuple[int, int] = (0, 0)


@dataclass(frozen=True)
class State:
    time_remaining: int = 0
    ore: tuple[int, int, bool] = (0, 1, False)  # Mineral count, robot count, skip indicator
    clay: tuple[int, int, bool] = (0, 0, False)
    obsidian: tuple[int, int, bool] = (0, 0, False)
    geode: tuple[int, int, bool] = (0, 0, False)

    def get_ministate(self) -> MiniState:
        return MiniState(self.time_remaining,
                         (self.ore[0], self.ore[1]),
                         (self.clay[0], self.clay[1]),
                         (self.obsidian[0], self.obsidian[1]),
                         (self.geode[0], self.geode[1]))

    def trim_state(self, bp: Blueprint) -> "State":
        # Yank any overflowing minerals and robots that can't be used with the remaining time, not including geodes.
        ore_robots = min(self.ore[1], bp.maxcosts[Minerals.ORE])
        clay_robots = min(self.clay[1], bp.maxcosts[Minerals.CLAY])
        obs_robots = min(self.obsidian[1], bp.maxcosts[Minerals.OBSIDIAN])
        ore_count = min(self.ore[0],
                        self.time_remaining * bp.maxcosts[Minerals.ORE] - ore_robots * (self.time_remaining - 1))
        clay_count = min(self.clay[0],
                         self.time_remaining * bp.maxcosts[Minerals.CLAY] - clay_robots * (self.time_remaining - 1))
        obs_count = min(self.obsidian[0],
                        self.time_remaining * bp.maxcosts[Minerals.OBSIDIAN] - obs_robots * (self.time_remaining - 1))
        ore_flag = self.ore[2] or ore_robots < self.ore[1]
        clay_flag = self.clay[2] or clay_robots < self.clay[1]
        obs_flag = self.obsidian[2] or obs_robots < self.obsidian[1]
        return State(self.time_remaining,
                     (ore_count, ore_robots, ore_flag),
                     (clay_count, clay_robots, clay_flag),
                     (obs_count, obs_robots, obs_flag),
                     self.geode)

    def generate_next_states(self, bp: Blueprint) -> iter:
        if self.time_remaining > 0:
            per_resource = {Minerals.ORE: self.ore, Minerals.CLAY: self.clay,
                            Minerals.OBSIDIAN: self.obsidian, Minerals.GEODE: self.geode}
            can_afford_robot = [robot for robot in Minerals
                                if all([per_resource[mat][0] >= count for count, mat in bp.costs[robot]])]
            # Option 1 - don't build anything, mark any mineral where we could afford a robot as 'skipped'
            yield State(self.time_remaining - 1,
                        (self.ore[0] + self.ore[1], self.ore[1], Minerals.ORE in can_afford_robot),
                        (self.clay[0] + self.clay[1], self.clay[1], Minerals.CLAY in can_afford_robot),
                        (self.obsidian[0] + self.obsidian[1], self.obsidian[1], Minerals.OBSIDIAN in can_afford_robot),
                        (self.geode[0] + self.geode[1], self.geode[1], Minerals.GEODE in can_afford_robot))
            # Option 2 - build the things we can afford
            if self.time_remaining == 1:  # Don't bother building anything with only 1 minute left
                return
            for build_robot in can_afford_robot:
                if (per_resource[build_robot][2] or  # Check skip indicator
                        (self.time_remaining == 2 and build_robot != Minerals.GEODE)):  # Only build geode robot with
                    continue                                                            # 2 minutes left
                # Move the state data to a temporary dict to more easily keep track of updated values
                tmp = {m: [per_resource[m][0] + per_resource[m][1], per_resource[m][1], per_resource[m][2]]
                       for m in per_resource}
                consumed_minerals = set()
                for amount, mineral in bp.costs[build_robot]:
                    tmp[mineral][0] -= amount
                    consumed_minerals.add(mineral)
                tmp[build_robot][1] += 1
                # Reset any skip flags for minerals whose robots costs minerals that were consumed
                for m in tmp:
                    costs = [c for _, c in bp.costs[m]]
                    if any(x in costs for x in consumed_minerals):
                        tmp[m][2] = False
                yield State(self.time_remaining - 1,
                            (tmp[Minerals.ORE][0], tmp[Minerals.ORE][1], tmp[Minerals.ORE][2]),
                            (tmp[Minerals.CLAY][0], tmp[Minerals.CLAY][1], tmp[Minerals.CLAY][2]),
                            (tmp[Minerals.OBSIDIAN][0], tmp[Minerals.OBSIDIAN][1], tmp[Minerals.OBSIDIAN][2]),
                            (tmp[Minerals.GEODE][0], tmp[Minerals.GEODE][1], tmp[Minerals.GEODE][2]))


class Factory:
    def __init__(self, rawstr: str):
        self.__blueprints = [Blueprint(line) for line in rawstr.splitlines()]

    def get_total_bp_qualitylevel(self, timeleft: int) -> int:
        qualitylevels = []
        for i, bp in enumerate(self.__blueprints):
            geodes = self.__get_bp_quantity(i, timeleft)
            qualitylevels.append(geodes * bp.id)
        return sum(qualitylevels)

    def get_topthree_product(self, timeleft: int) -> int:
        quantities = []
        for bpidx in range(3):
            quantities.append(self.__get_bp_quantity(bpidx, timeleft))
        return math.prod(quantities)

    def __get_bp_quantity(self, bpidx: int, time: int) -> int:
        init_state = State(time_remaining=time)
        queue = deque([init_state])
        seen = set()
        max_geode = 0
        while queue:
            currentstate = queue.pop()
            if currentstate.time_remaining <= 0:
                max_geode = max(max_geode, currentstate.geode[0])
                continue
            currentstate = currentstate.trim_state(self.__blueprints[bpidx])
            ministate = currentstate.get_ministate()
            if ministate in seen:  # Use the state representation without skip indicator for 'seen' check
                continue
            seen.add(ministate)
            if max_geode > 0:
                theoretical_best = (currentstate.geode[0] + currentstate.time_remaining * currentstate.geode[1] +
                                    (currentstate.time_remaining * (currentstate.time_remaining - 1)) // 2)
                if theoretical_best <= max_geode:
                    continue
            for nextstate in currentstate.generate_next_states(self.__blueprints[bpidx]):
                queue.append(nextstate)
        return max_geode


def main() -> int:
    with open('../Inputfiles/aoc19.txt', 'r') as file:
        myfactory = Factory(file.read().strip('\n'))
    print(f"Part 1: {myfactory.get_total_bp_qualitylevel(24)}")
    print(f"Part 2: {myfactory.get_topthree_product(32)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
