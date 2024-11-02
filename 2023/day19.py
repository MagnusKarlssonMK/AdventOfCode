"""
Part 1 - Fairly straightforward, just set up a way to organize the workflows and rules and run the input through and
see what comes out the other end.
Part 2 - Yet another challenge in handling splitting ranges, mainly a headache trying to keep track of the layers of
dicts, ranges, lists etc.
"""
import time
from pathlib import Path
import re
import operator
from math import prod


Partrating = dict[str: int]   # Parts = ['x', 'm', 'a', 's']
Partratingrange = dict[str: range]


class Rule:
    __OPMAP = {'<': operator.lt, '>': operator.gt}

    def __init__(self, rulestr: str) -> None:
        if len(tmp := rulestr.split(":")) > 1:
            self.__condpart, self.__condoperation, nbrstr = re.findall(r"(\w)(.)(\d+)", tmp[0])[0]
            self.__condthrshold = int(nbrstr)
        else:
            self.__condpart = None
            self.__condthrshold = 0
            self.__condoperation = ""
        self.__ifpass = tmp[-1]

    def getverdict(self, part: Partrating) -> str:
        if self.__condpart:
            if Rule.__OPMAP[self.__condoperation](part[self.__condpart], self.__condthrshold):
                return self.__ifpass
            else:
                return ""
        else:
            return self.__ifpass

    def getrangesplit(self, inranges: Partratingrange) -> iter:
        if self.__condpart:
            thrshold = self.__condthrshold if self.__condoperation == "<" else self.__condthrshold + 1
            if self.__condthrshold in inranges[self.__condpart]:
                outrangeslow: Partratingrange = dict(inranges)
                outrangeshigh: Partratingrange = dict(inranges)
                outrangeslow[self.__condpart] = range(outrangeslow[self.__condpart].start, thrshold)
                outrangeshigh[self.__condpart] = range(thrshold, inranges[self.__condpart].stop)
                if self.__condoperation == ">":
                    yield "", outrangeslow
                    yield self.__ifpass, outrangeshigh
                else:
                    yield "", outrangeshigh
                    yield self.__ifpass, outrangeslow
            else:
                yield self.__ifpass, inranges
        else:
            yield self.__ifpass, inranges

    def __repr__(self):
        return f"{self.__condpart}-{self.__condoperation}-{self.__condthrshold}-{self.__ifpass}"


class System:
    def __init__(self, rawstr: str) -> None:
        wf, rt = rawstr.split('\n\n')
        self.__workflows: dict[str: list[Rule]] = {}
        for flow in wf.splitlines():
            label, rls = flow.strip('}').split('{')
            self.__workflows[label] = [Rule(r) for r in rls.split(',')]
        self.__ratings: list[Partrating] = \
            [{part: int(count) for part, count in re.findall(r"(.)=(\d+)", rating)}
             for rating in rt.splitlines()]

    def __process_workflow(self, rating: Partrating) -> int:
        currentworkflow = "in"
        while currentworkflow not in ("A", "R"):
            for rule in self.__workflows[currentworkflow]:
                if (verdict := rule.getverdict(rating)) != "":
                    currentworkflow = verdict
                    break
        if currentworkflow == "A":
            return sum(rating.values())
        return 0

    def get_accepted_sum(self) -> int:
        return sum([self.__process_workflow(rating) for rating in self.__ratings])

    def get_combinationcount(self) -> int:
        initialpartgroup: tuple[str, Partratingrange] = ("in", {"x": range(1, 4001), "m": range(1, 4001),
                                                                "a": range(1, 4001), "s": range(1, 4001)})
        queue: list[tuple[str, Partratingrange]] = [initialpartgroup]
        verdict_a = []
        while queue:
            currentworkflow, ranges = queue.pop(0)
            if currentworkflow not in ("A", "R"):
                for rule in self.__workflows[currentworkflow]:
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


def main(aoc_input: str) -> None:
    system = System(aoc_input)
    print(f"Part 1: {system.get_accepted_sum()}")
    print(f"Part 2: {system.get_combinationcount()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day19.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
