"""
Use a recursive generator function to iterate over the possible ingredient mix distributions and find the max scoring
combination.
Takes a couple of seconds to run, could possibly be optimized to run part 1 and 2 simultaneously, since part2 pretty
much just adds a calorie filter to the scoring.
"""
import sys
from pathlib import Path
import re
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day15.txt')


@dataclass(frozen=True)
class Ingredient:
    capacity: int = 0
    durability: int = 0
    flavor: int = 0
    texture: int = 0
    calories: int = 0

    def get_score(self, calorie_limit: int = None) -> int:
        if calorie_limit and self.calories != calorie_limit:
            return 0
        else:
            return max(0, self.capacity) * max(0, self.durability) * max(0, self.flavor) * max(0, self.texture)

    def __add__(self, other: "Ingredient") -> "Ingredient":
        return Ingredient(self.capacity + other.capacity, self.durability + other.durability,
                          self.flavor + other.flavor, self.texture + other.texture,
                          self.calories + other.calories)

    def __mul__(self, other: int) -> "Ingredient":
        return Ingredient(self.capacity * other, self.durability * other, self.flavor * other,
                          self.texture * other, self.calories * other)

    def __rmul__(self, other: int) -> "Ingredient":
        return Ingredient(self.capacity * other, self.durability * other, self.flavor * other,
                          self.texture * other, self.calories * other)


def amounts_generator(ingredients: int, total: int) -> iter:
    if ingredients <= 1:
        yield [total]
    else:
        for i in range(total + 1):
            for rest in amounts_generator(ingredients - 1, total - i):
                yield [i] + rest


class Kitchen:
    __TOTAL_INGREDIENTS = 100
    __CALORIE_MAX = 500

    def __init__(self, rawstr: str) -> None:
        self.__ingredients: dict[str: Ingredient] = {}
        for line in rawstr.splitlines():
            nbrs = list(map(int, re.findall(r"-?\d+", line)))
            self.__ingredients[line.split()[0]] = Ingredient(*nbrs)

    def __get_cookie_score(self, mix: list[int], cal_limited: bool) -> int:
        total = Ingredient()
        for amount, ingredient in zip(mix, self.__ingredients):
            total += amount * self.__ingredients[ingredient]
        if cal_limited:
            return total.get_score(Kitchen.__CALORIE_MAX)
        return total.get_score()

    def get_top_score(self, cal_limited: bool = False) -> int:
        return max([self.__get_cookie_score(mix, cal_limited)
                   for mix in amounts_generator(len(self.__ingredients), Kitchen.__TOTAL_INGREDIENTS)])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        kitchen = Kitchen(file.read().strip('\n'))
    print(f"Part 1: {kitchen.get_top_score()}")
    print(f"Part 2: {kitchen.get_top_score(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
