"""
Part 1 - Fairly straightforward, just set up a way to organize the workflows and rules and run the input through and
see what comes out the other end.
Part 2 - Yet another challenge in handling splitting ranges, mainly a headache trying to keep track of the layers of
dicts, ranges, lists etc.
"""
import sys
import re
import operator
from math import prod


Partrating = dict[str: int]   # Parts = ['x', 'm', 'a', 's']
Partratingrange = dict[str: range]
Op = {'<': operator.lt, '>': operator.gt}


class Rule:
    def __init__(self, rulestr: str):
        if len(tmp := rulestr.split(":")) > 1:
            self.condpart, self.condoperation, nbrstr = re.findall(r"(\w)(.)(\d+)", tmp[0])[0]
            self.condthrshold = int(nbrstr)
        else:
            self.condpart = None
            self.condthrshold = 0
            self.condoperation = ""
        self.ifpass = tmp[-1]

    def getverdict(self, part: Partrating) -> str:
        if self.condpart:
            if Op[self.condoperation](part[self.condpart], self.condthrshold):
                return self.ifpass
            else:
                return ""
        else:
            return self.ifpass

    def getrangesplit(self, inranges: Partratingrange) -> iter:
        if self.condpart:
            thrshold = self.condthrshold if self.condoperation == "<" else self.condthrshold + 1
            if self.condthrshold in inranges[self.condpart]:
                outrangeslow: Partratingrange = dict(inranges)
                outrangeshigh: Partratingrange = dict(inranges)
                outrangeslow[self.condpart] = range(outrangeslow[self.condpart].start, thrshold)
                outrangeshigh[self.condpart] = range(thrshold, inranges[self.condpart].stop)
                if self.condoperation == ">":
                    yield "", outrangeslow
                    yield self.ifpass, outrangeshigh
                else:
                    yield "", outrangeshigh
                    yield self.ifpass, outrangeslow
            else:
                yield self.ifpass, inranges
        else:
            yield self.ifpass, inranges

    def __repr__(self):
        return f"{self.condpart}-{self.condoperation}-{self.condthrshold}-{self.ifpass}"


class System:
    def __init__(self, wfstr: str):
        self.workflows: dict[str: list[Rule]] = {}
        for flow in wfstr.splitlines():
            label, rls = flow.strip('}').split('{')
            self.workflows[label] = [Rule(r) for r in rls.split(',')]

    def process_workflow(self, rating: Partrating) -> int:
        currentworkflow = "in"
        while currentworkflow not in ("A", "R"):
            for rule in self.workflows[currentworkflow]:
                if (verdict := rule.getverdict(rating)) != "":
                    currentworkflow = verdict
                    break
        if currentworkflow == "A":
            return sum(rating.values())
        return 0

    def get_combinationcount(self) -> int:
        initialpartgroup: tuple[str, Partratingrange] = ("in", {"x": range(1, 4001), "m": range(1, 4001),
                                                                "a": range(1, 4001), "s": range(1, 4001)})
        queue: list[tuple[str, Partratingrange]] = [initialpartgroup]
        verdict_a = []

        while len(queue) > 0:
            currentworkflow, ranges = queue.pop(0)
            if currentworkflow not in ("A", "R"):
                for rule in self.workflows[currentworkflow]:
                    done = True
                    for newranges in rule.getrangesplit(ranges):
                        if newranges[0] != "":
                            queue.append(newranges)
                        else:
                            done = False
                            ranges = newranges[1]
                    if done:
                        break
            elif currentworkflow == "A":
                verdict_a.append(ranges)

        return sum([prod([r.stop - r.start for r in list(a_ranges.values())]) for a_ranges in verdict_a])


def main() -> int:
    with open('../Inputfiles/aoc19.txt') as file:
        wf, rt = file.read().strip('\n').split('\n\n')
    system = System(wf)
    ratings: list[Partrating] = [{part: int(count) for part, count in re.findall(r"(.)=(\d+)", rating)}
                                 for rating in rt.splitlines()]
    print("Part 1:", sum([system.process_workflow(rating) for rating in ratings]))
    print("Part 2:", system.get_combinationcount())
    return 0


if __name__ == "__main__":
    sys.exit(main())
