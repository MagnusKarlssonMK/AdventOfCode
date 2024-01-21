# AoC 2023 day 19
import re
from math import prod

Partrating = dict[str: int]   # Parts = ['x', 'm', 'a', 's']
Partratingrange = dict[str: range]
Partgroup = dict[str: Partratingrange]


class Rule:
    def __init__(self, inputstr: str):
        if len(tmp := inputstr.split(":")) > 1:
            self.condpart, self.condoperation, nbrstr = re.findall(r"(\w)(.)(\d+)", tmp[0])[0]
            self.condthrshold = int(nbrstr)
        else:
            self.condpart = None
            self.condthrshold = 0
            self.condoperation = ""
        self.ifpass = tmp[-1]

    def getverdict(self, part: Partrating) -> str:
        if self.condpart:
            if self.condoperation == ">":
                if part[self.condpart] > self.condthrshold:
                    return self.ifpass
                else:
                    return ""
            else:
                if part[self.condpart] < self.condthrshold:
                    return self.ifpass
                else:
                    return ""
        else:
            return self.ifpass

    def getrangesplit(self, newrangelist):
        if self.condpart:
            if self.condthrshold in newrangelist[1][self.condpart]:
                retsetlow = dict(newrangelist[1])
                retsethigh = dict(newrangelist[1])
                thold = self.condthrshold if self.condoperation == "<" else self.condthrshold + 1
                retsetlow[self.condpart] = range(retsetlow[self.condpart].start, thold)
                retsethigh[self.condpart] = range(thold, newrangelist[1][self.condpart].stop)
                if self.condoperation == ">":
                    return ("", retsetlow), (self.ifpass, retsethigh)
                else:
                    return ("", retsethigh), (self.ifpass, retsetlow)
            else:
                print("Rule not in range, TBD")
            return (self.ifpass, newrangelist[1]),
        else:
            return (self.ifpass, newrangelist[1]),

    def __str__(self):
        return f"Condition: {self.condpart} {self.condoperation} {self.condthrshold} If pass: -{self.ifpass}-"


workflows: dict[str: list[Rule]] = {}
result_p1 = 0

with open("aoc19.txt", "r") as file:
    while len(line := file.readline()) > 1:
        label, rules = line.strip("\n").strip("}").split("{")
        rulelist = rules.split(",")
        # print(label, rulelist)
        workflows[label] = []
        for rulestr in rulelist:
            workflows[label].append(Rule(rulestr))

    while len(line := file.readline()) > 1:
        partlist: Partrating = {part: int(count) for part, count in re.findall(r"(.)=(\d+)", line)}
        # print(partlist)
        currentworkflow = "in"
        while currentworkflow not in ("A", "R"):
            for idx in range(len(workflows[currentworkflow])):
                a: Rule = workflows[currentworkflow][idx]
                b = a.getverdict(partlist)
                if b != "":
                    currentworkflow = b
                    break

        if currentworkflow == "A":
            result_p1 += sum(partlist.values())

print("Part1: ", result_p1)

initialpartgroup = ("in", {"x": range(1, 4001), "m": range(1, 4001), "a": range(1, 4001), "s": range(1, 4001)})

outerq = [initialpartgroup]
verdict_A = []
verdict_R = []

while len(outerq) > 0:
    currentgroup = outerq.pop()
    while currentgroup[0] not in ("A", "R"):
        currentworkflow = str(currentgroup[0])
        for idx in range(len(workflows[currentworkflow])):
            a: Rule = workflows[currentworkflow][idx]
            b = a.getrangesplit(currentgroup)
            if len(b) > 1:  # Funkar inte! Räknar inre element, så alltid större än 1
                currentgroup = b[0]
                outerq.append(b[1])
            else:
                currentgroup = b[0]
            if currentgroup[0] != "":
                break
    if currentgroup[0] == "A":
        verdict_A.append(currentgroup[1])
    elif currentgroup[0] == "R":
        verdict_R.append(currentgroup[1])
    else:
        print("Unexpected...???")

result_p2 = 0

for a_ranges in verdict_A:
    result_p2 += prod(r.stop - r.start for r in list(a_ranges.values()))

print("Part2: ", result_p2)

# 167409079868000
# 167807805646283
# 21856640000000
# 96000000000000
