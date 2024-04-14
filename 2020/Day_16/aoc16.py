"""
Part 1: pretty much just parse the input and check the content, store only the nearby tickets that are 'valid'.
Part 2: throw the nearby ticket numbers into a list of sets, and build a list of candidate fields for each position.
From there on it's sudoku time sort of. There's probably more elegant ways of solving this with matrices, rather than
this mess.
"""
import sys
import re
import math


class Field:
    def __init__(self, name: str, nbrstring: str):
        self.name = name
        nbrs = list(map(int, re.findall(r'\d+', nbrstring)))
        self.ranges: tuple[range, range] = range(nbrs[0], nbrs[1] + 1), range(nbrs[2], nbrs[3] + 1)

    def is_inrange(self, nbr: int) -> bool:
        return any([nbr in r for r in self.ranges])


class Ticket:
    def __init__(self, nbrs: list[int]):
        self.nbrs = list(nbrs)


class TicketData:
    def __init__(self, fields: list[str], your: list[int], nearby: list[str]):
        self.__fields: list[Field] = [Field(*line.split(': ')) for line in fields]
        self.__your: Ticket = Ticket(your)
        self.__nearby: list[Ticket] = [Ticket(list(map(int, nearby[i].split(',')))) for i in range(1, len(nearby))]

    def get_invalidnearby(self) -> int:
        invalid_nbrs: list[int] = []
        validnearby: list[Ticket] = []
        for ticket in self.__nearby:
            for nbr in ticket.nbrs:
                if not self.__containedinfield(nbr):
                    invalid_nbrs.append(nbr)
                    break
            else:
                validnearby.append(ticket)
        self.__nearby = validnearby
        return sum(invalid_nbrs)

    def __containedinfield(self, nbr: int) -> bool:
        for i in range(len(self.__fields)):
            if self.__fields[i].is_inrange(nbr):
                return True
        return False

    def get_departurescore(self) -> int:
        nbrsets = [set([nt.nbrs[i] for nt in self.__nearby]) for i in range(len(self.__nearby[0].nbrs))]
        possible = []
        for i, nbrset in enumerate(nbrsets):
            possible.append([field.name for field in self.__fields
                             if all([field.is_inrange(nbr) for nbr in nbrset])])
        possible = list(zip([i for i in range(len(possible))], possible))
        possible = sorted(possible, key=lambda x: len(x[1]))
        queue = [[p] for p in possible[0][1]]
        paths = []
        while queue:
            p = queue.pop(0)
            for nxt in possible[len(p)][1]:
                if nxt not in p:
                    n_p = list(p)
                    n_p.append(nxt)
                    if len(n_p) >= len(possible):
                        paths.append(n_p)
                    else:
                        queue.append(n_p)
        if len(paths) != 1:
            return -1
        path = sorted(list(zip([p[0] for p in possible], paths[0])), key=lambda x: x[0])
        return math.prod([self.__your.nbrs[idx] for idx, name in path if 'departure' in name])


def main() -> int:
    with open('../Inputfiles/aoc16.txt', 'r') as file:
        fields, your, nearby = file.read().strip('\n').split('\n\n')
    mydata = TicketData(fields.splitlines(), list(map(int, your.splitlines()[1].split(','))), nearby.splitlines())
    print(f"Part 1: {mydata.get_invalidnearby()}")
    print(f"Part 2: {mydata.get_departurescore()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())