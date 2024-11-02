"""
"""
import time
from pathlib import Path


class FoodInfo:
    def __init__(self, rawstr: str) -> None:
        self.__ingredient_list: list[list[str]] = []
        self.__allergens: dict[str: list[str]] = {}
        self.__ingredients: set[str] = set()
        self.__known: dict[str: str] = {}
        for line in rawstr.splitlines():
            left, right = line.strip(')').split('(contains ')
            self.__ingredient_list.append(left.split())
            i = set(self.__ingredient_list[-1])
            self.__ingredients.update(i)
            for a in right.split(', '):
                if a not in self.__allergens:
                    self.__allergens[a] = i
                else:
                    self.__allergens[a] = i & self.__allergens[a]

    def get_non_allergens_count(self) -> int:
        changed = True
        while changed:
            changed = False
            newallergens = {}
            for allergen in self.__allergens:
                if len(self.__allergens[allergen]) == 1:
                    self.__known[list(self.__allergens[allergen])[0]] = allergen
                    changed = True
                else:
                    newallergens[allergen] = set()
                    for i in self.__allergens[allergen]:
                        if i in self.__known:
                            changed = True
                        else:
                            newallergens[allergen].add(i)
            if changed:
                self.__allergens = dict(newallergens)
        non_allergens = self.__ingredients ^ set(self.__known.keys())
        return sum([len(set(i) & non_allergens) for i in self.__ingredient_list])

    def get_dangerous_list(self) -> str:
        result = ''
        for k, _ in sorted(list(self.__known.items()), key=lambda x: x[1]):
            result += ',' + k
        return result.strip(',')


def main(aoc_input: str) -> None:
    food = FoodInfo(aoc_input)
    print(f"Part 1: {food.get_non_allergens_count()}")
    print(f"Part 2: {food.get_dangerous_list()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day21.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
