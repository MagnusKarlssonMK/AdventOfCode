"""
Store the reactions in a dict to be able to look up the yield and requirements for each chemical.
Then start from fuel and add to a shopping list what's needed, add and subtract from it as needed until only ore is
left.
For part 2, re-use the function from part 1 by gradually increasing the fuel amount and check whether the output ore
has reached the goal.
"""
import sys
import re
from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class Chemical:
    amount: int
    name: str


@dataclass(frozen=True)
class Reaction:
    result: int
    requires: list[Chemical]


class NanoFactory:
    def __init__(self, rawstr: str) -> None:
        self.__reactions = {}
        for line in rawstr.splitlines():
            reactions = re.findall(r"(\d+) (\w+)", line)
            self.__reactions[reactions[-1][1]] = Reaction(int(reactions[-1][0]),
                                                          [Chemical(int(n), c) for n, c in reactions[0:-1]])

    def get_minimum_ore_req(self, fuel_amount: int = 1) -> int:
        shopping_list: dict[str: int] = {'FUEL': fuel_amount}
        while any((name := k) for k in shopping_list if k != 'ORE' and shopping_list[k] > 0):
            multiplier = ceil(shopping_list[name] / self.__reactions[name].result)
            for c in self.__reactions[name].requires:
                if c.name not in shopping_list:
                    shopping_list[c.name] = multiplier * c.amount
                else:
                    shopping_list[c.name] += multiplier * c.amount
            shopping_list[name] -= self.__reactions[name].result * multiplier
        return shopping_list['ORE']

    def get_maximum_fuel(self) -> int:
        ore_amount = 1_000_000_000_000
        fuel = 2
        while (ore_needed := self.get_minimum_ore_req(fuel)) < ore_amount:
            fuel = 1 + max(fuel, fuel * ore_amount // ore_needed)
        return fuel - 1


def main() -> int:
    with open('../Inputfiles/aoc14.txt', 'r') as file:
        factory = NanoFactory(file.read().strip('\n'))
    print(f"Part 1: {factory.get_minimum_ore_req()}")
    print(f"Part 2: {factory.get_maximum_fuel()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())