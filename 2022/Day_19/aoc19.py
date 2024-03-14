"""Putting this on hold and shelving for now, can't get it to work..."""
import sys


class Blueprint:
    def __init__(self, rawstr: str):
        bpid, costs = rawstr.split(': ')
        self.id = int(bpid.strip('Blueprint '))
        self.costs: dict[str: list[tuple[int, str]]] = {}
        self.maxcosts: dict[str: int] = {}
        for cost in costs.strip('.').split('. '):
            dest, source = cost.split(' robot costs ')
            dest = dest.split()[1]
            self.costs[dest] = []
            for s in source.split(' and '):
                nbr, material = s.split()
                self.costs[dest].append((int(nbr), material))
                if material in self.maxcosts:
                    self.maxcosts[material] = max(self.maxcosts[material], int(nbr))
                else:
                    self.maxcosts[material] = int(nbr)

    def get_canafford(self, resources: dict[str: int]) -> iter:
        for robottype in self.costs:
            if (all([resources[mat] >= count for count, mat in self.costs[robottype]]) and
                    any([resources[mat] == count for count, mat in self.costs[robottype]])):
                yield robottype

    def get_maxcost(self, mat: str) -> int:
        if mat in self.maxcosts:
            return self.maxcosts[mat]
        return 0


class Factory:
    def __init__(self, rawstr: str):
        self.__blueprints = [Blueprint(line) for line in rawstr.splitlines()]
        self.__materials: dict[str: int] = {}
        self.__robots: dict[str: int] = {}
        for material in self.__blueprints[0].costs:
            self.__materials[material] = 0
            if material == 'ore':
                self.__robots[material] = 1
            else:
                self.__robots[material] = 0

    def get_total_bp_qualitylevel(self) -> int:
        qualitylevels = []
        for bp in self.__blueprints:
            robots: dict[str:int] = dict(self.__robots)
            materials: dict[str:int] = dict(self.__materials)
            queue = [(robots, materials, 24)]
            seen = set()
            maxq = 0

            while queue:
                oldrobots, oldmaterials, time = queue.pop(0)
                if time <= 0:
                    maxq = max(maxq, oldmaterials['geode'])
                else:
                    newmaterials = dict(oldmaterials)
                    newrobots = dict(oldrobots)
                    for r in newrobots:
                        if r != 'geode':
                            newrobots[r] = min(oldrobots[r], bp.get_maxcost(r))
                            newmaterials[r] = min(oldmaterials[r],
                                                  (time * bp.get_maxcost(r)) - (newrobots[r] * (time - 1)))
                    state = (tuple(newrobots.values()), tuple(newmaterials.values()), time)
                    if state in seen:
                        continue
                    seen.add(state)
                    time -= 1
                    for m in newmaterials:
                        newmaterials[m] += newrobots[m]
                    queue.append((dict(newrobots), dict(newmaterials), time))
                    for robottype in bp.get_canafford(newmaterials):
                        mats = dict(newmaterials)
                        for n, c in bp.costs[robottype]:
                            mats[c] -= n
                        robs = dict(newrobots)
                        robs[robottype] += 1
                        queue.append((robs, mats, time))
            print(maxq)
            qualitylevels.append(maxq)
        return sum(qualitylevels)


def main() -> int:
    with open('../Inputfiles/aoc19_example.txt', 'r') as file:
        myfactory = Factory(file.read().strip('\n'))
    print("Part 1:", myfactory.get_total_bp_qualitylevel())
    return 0


if __name__ == "__main__":
    sys.exit(main())
