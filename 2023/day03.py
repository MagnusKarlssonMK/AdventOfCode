"""
Store the symbols in a dict with the type stored for each symbol, and then a dict for all parts which stores a list
of adjacent symbols for each part.
Then for part 1, simply iterate over the parts and get the sum of the values for the parts that have at least one
symbol in its adjacent list.
For part 2, instead iterate over the symbols and find the gears, and then iterate over the parts to see how many parts
that are adjacent for each gear.
"""
import sys
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    row: int
    col: int
    length: int
    value: int


@dataclass(frozen=True)
class Symbol:
    row: int
    col: int


class Schematic:
    def __init__(self, rawstr: str) -> None:
        self.__parts: dict[Part: list[Symbol]] = {}
        self.__symbols: dict[Symbol: str] = {}
        # Parse input
        for rowidx, row in enumerate(rawstr.splitlines()):
            nbrs = re.finditer(r"(\d+)", row)
            symbs = re.finditer(r"[^.\d]", row)
            for nbr in nbrs:
                self.__parts[Part(rowidx, nbr.start(), nbr.end() - nbr.start(), int(row[nbr.start():nbr.end()]))] = []
            for symb in symbs:
                self.__symbols[Symbol(rowidx, symb.start())] = row[symb.start()]
        # Connect symbols to parts
        for part in self.__parts:
            for rowidx in range(part.row - 1, part.row + 2):
                for colidx in range(part.col - 1, part.col + part.length + 1):
                    if (adj_symb := Symbol(rowidx, colidx)) in self.__symbols:
                        self.__parts[part].append(adj_symb)

    def get_partnumber_sum(self) -> int:
        return sum([part.value for part in self.__parts if len(self.__parts[part]) > 0])

    def get_gearratio_sum(self) -> int:
        retval = 0
        for symbol, symbtype in self.__symbols.items():
            if symbtype == "*":
                adj_parts = [part.value for part in self.__parts if symbol in self.__parts[part]]
                if len(adj_parts) == 2:
                    retval += adj_parts[0] * adj_parts[1]
        return retval


def main() -> int:
    with open('../Inputfiles/aoc3.txt', 'r') as file:
        myschematic = Schematic(file.read().strip('\n'))

    print(f"Part 1 redux: {myschematic.get_partnumber_sum()}")
    print(f"Part 2 redux: {myschematic.get_gearratio_sum()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
