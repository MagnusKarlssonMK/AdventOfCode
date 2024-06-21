"""
Store the program tree in a dict, with each node containig its weight, leafs and parent. The node without a parent
is the answer to Part 1.
For Part 2, make a recursive weight calculation of the tree, where each program checks the weight of its leafs (if any),
and calculates and reports the required correction if discovered.
"""
import sys
from dataclasses import dataclass


@dataclass
class Program:
    weight: int
    leafs: set[str]
    parent: str = None


class Tower:
    def __init__(self, rawstr: str) -> None:
        self.__programs = {}
        self.__root = None
        for line in rawstr.splitlines():
            tokens = line.split()
            leafs = {w.strip(',') for w in tokens[3:]}
            self.__programs[tokens[0]] = Program(int(tokens[1].strip('(').strip(')')), leafs)
        for p, item in self.__programs.items():
            for leaf in item.leafs:
                self.__programs[leaf].parent = p
        for p in self.__programs:
            if not self.__programs[p].parent:
                self.__root = p

    def get_bottom_program_name(self) -> str:
        return self.__root

    def get_correct_weight(self) -> int:
        _, c = self.__get_weight_and_correction(self.__root)
        return c

    def __get_weight_and_correction(self, program: str) -> tuple[int, int]:
        leafweights = {}
        leafcorrections = []
        if not self.__programs[program].leafs:
            # Node without leafs
            return self.__programs[program].weight, 0

        for leaf in self.__programs[program].leafs:
            w, c = self.__get_weight_and_correction(leaf)
            if w not in leafweights:
                leafweights[w] = [leaf]
            else:
                leafweights[w].append(leaf)
            leafcorrections.append(c)

        if (corr := sum(leafcorrections)) > 0:
            # A node further down the tree has reported a correction, just propagate upwards
            return (self.__programs[program].weight + (sum(leafweights) * sum([len(v) for v in leafweights.values()])),
                    corr)
        elif len(leafweights) > 1:
            # These leafs are not balanced; figure out which one is bad and calculate the required correction
            correctweight = -1
            badweight = -1
            badnode = ''
            for w in leafweights:
                if len(leafweights[w]) > 1:
                    correctweight = w
                else:
                    badweight = w
                    badnode = leafweights[w][0]
            return (self.__programs[program].weight + (correctweight * sum([len(v) for v in leafweights.values()])),
                    correctweight - (badweight - self.__programs[badnode].weight))
        # else - all leafs have reported the same weight and are thus balanced
        return self.__programs[program].weight + (sum(leafweights) * sum([len(v) for v in leafweights.values()])), 0


def main() -> int:
    with open('../Inputfiles/aoc7.txt', 'r') as file:
        tower = Tower(file.read().strip('\n'))
    print(f"Part 1: {tower.get_bottom_program_name()}")
    print(f"Part 2: {tower.get_correct_weight()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
