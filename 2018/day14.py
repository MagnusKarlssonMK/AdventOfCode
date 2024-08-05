"""
Brute force, kinda slow part 2. Not sure if there is some kind of repeating pattern in the generation that could be
exploited, couldn't really find any after some quick experimentation.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2018/day14.txt')


class RecipeGenerator:
    __START_POSITIONS = (0, 1)
    __START_RECIPES = (3, 7)

    def __init__(self, nbr: str) -> None:
        self.__inputnbr = nbr
        self.__scoreboard = list(RecipeGenerator.__START_RECIPES)
        self.__elfs = list(RecipeGenerator.__START_POSITIONS)

    def __reset(self) -> None:
        self.__scoreboard = list(RecipeGenerator.__START_RECIPES)
        self.__elfs = list(RecipeGenerator.__START_POSITIONS)

    def __make_recipes(self) -> int:
        newcount = 1
        current_sum = sum([self.__scoreboard[e] for e in self.__elfs])
        if current_sum > 9:
            newcount = 2  # Return the number of new recipes, so we can avoid making unnecessary comparisons in part 2
            self.__scoreboard.append(1)
        self.__scoreboard.append(current_sum % 10)
        self.__elfs = [(e + self.__scoreboard[e] + 1) % len(self.__scoreboard) for e in self.__elfs]
        return newcount

    def get_scores(self) -> int:
        limit = int(self.__inputnbr)
        while len(self.__scoreboard) < limit + 10:
            self.__make_recipes()
        result = int(''.join([str(i) for i in self.__scoreboard[limit: limit + 10]]))
        self.__reset()
        return result

    def get_scores_left_side(self) -> int:
        nbrlist = [int(c) for c in self.__inputnbr]
        nbrlistlen = len(nbrlist)
        while True:
            if self.__make_recipes() > 1:
                # If two new recipes were added, we need to check also -1 from the end
                if self.__scoreboard[-nbrlistlen - 1: -1] == nbrlist:
                    result = len(self.__scoreboard) - nbrlistlen - 1
                    break
            if self.__scoreboard[-nbrlistlen:] == nbrlist:
                result = len(self.__scoreboard) - nbrlistlen
                break
        self.__reset()
        return result


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        generator = RecipeGenerator(file.read().strip('\n'))
    print(f"Part 1: {generator.get_scores()}")
    print(f"Part 2: {generator.get_scores_left_side()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
