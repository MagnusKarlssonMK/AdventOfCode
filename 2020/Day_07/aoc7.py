"""
Even more string parsing gymnastics. Extract the data into a dictionary, reverse that dictionary to get a directed
adjaceny list of 'bag contained by...'. BFS to get a visited list of all reachable bags from the starting bag, which
gives the answer to Part 1. For Part 2, make a recursive call on the first dictionary to count the bags in the bag in
the bag... I added a cache for the recursion just in case since I suspected that there would be a lot of repeated
calls for the same bag, but it doesn't seem to make much of a performance difference.
"""
import sys


class BagRules:
    def __init__(self):
        self.rules: dict[str: list[tuple[str, int]]] = {}
        self.invertedrules: dict[str: set[str]] = {}
        self.bagcontentcache: dict[str: int] = {}

    def addrule(self, rulekey: str, rulelist: list[str]):
        if rulekey not in self.rules:
            self.rules[rulekey] = []
        if rulekey not in self.invertedrules:
            self.invertedrules[rulekey] = set()
        if len(rulelist) > 0:
            self.rules[rulekey].append((rulelist[1], rulelist[0]))
            if rulelist[1] not in self.invertedrules:
                self.invertedrules[rulelist[1]] = set()
            self.invertedrules[rulelist[1]].add(rulekey)

    def countcontainedin(self, bag: str) -> int:
        if bag not in self.invertedrules:
            return 0
        seen: set[str] = set()
        bfsq = [bag]
        while bfsq:
            current = bfsq.pop(0)
            if current not in seen:
                for n in self.invertedrules[current]:
                    if n not in seen:
                        bfsq.append(n)
                seen.add(current)
        return len(seen) - 1  # -1 to subtract the starting bag color

    def countbagscontainedin(self, bag: str) -> int:
        if bag not in self.rules:
            return 0
        count = 0
        for rule in self.rules[bag]:
            if rule[0] not in self.bagcontentcache:
                result = self.countbagscontainedin(rule[0])
                count += rule[1] * (result + 1)  # +1 to include the rule[0] bag itself too, not just its content.
                self.bagcontentcache[rule[0]] = result
            else:
                count += rule[1] * (self.bagcontentcache[rule[0]] + 1)
        return count


def main() -> int:
    with open('../Inputfiles/aoc7.txt', 'r') as file:
        lines = [[i[0], i[1].split(', ')] for i in [line.split(' bags contain ')
                                                    for line in file.read().strip('\n').splitlines()]]
    rules = BagRules()
    for line in lines:
        for i in line[1]:
            if "no other" in i:
                rules.addrule(line[0], [])
                break
            content = i.split()
            rules.addrule(line[0], [int(content[0]), content[1] + " " + content[2]])

    print("Part 1:", rules.countcontainedin("shiny gold"))
    print("Part 2:", rules.countbagscontainedin("shiny gold"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
