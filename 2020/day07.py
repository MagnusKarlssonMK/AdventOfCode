"""
Even more string parsing gymnastics. Extract the data into a dictionary, BFS to expand all reachable bags from the
starting bag until either the golden bag is found or list runs out, which gives the answer to Part 1.
For Part 2, make a recursive call on the dictionary to count the bags in the bag in the bag...
I added a memo cache for the recursion just in case, since I suspected that there would be a lot of repeated
calls for the same bag, but it doesn't seem to make much of a performance difference.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day07.txt')


class BagRules:
    def __init__(self, rawstr: str) -> None:
        lines = [[i[0], i[1].split(', ')] for i in [line.split(' bags contain ') for line in rawstr.splitlines()]]
        self.__rules: dict[str: list[tuple[str, int]]] = {}
        for line in lines:
            self.__rules[line[0]] = []
            for content in line[1]:
                if 'no other' in content:
                    break
                nbr, bag_p1, bag_p2, _ = content.split()
                self.__rules[line[0]].append((int(nbr), bag_p1 + ' ' + bag_p2))
        self.__bagcontentcache: dict[str: int] = {}

    def countcontainedin(self, bag: str) -> int:
        count = 0
        for key in self.__rules:
            content = list(self.__rules[key])
            while content:
                _, color = content.pop(0)
                if color == bag:
                    count += 1
                    break
                for m in self.__rules[color]:
                    content.append(m)
        return count

    def countbagscontainedin(self, bag: str) -> int:
        return self.__countcontent(bag) - 1  # -1 to not count the input bag itself

    def __countcontent(self, bag: str) -> int:
        if bag in self.__bagcontentcache:
            return self.__bagcontentcache[bag]
        count = 1  # +1 to include the bag itself too, not just its content.
        for nbr, color in self.__rules[bag]:
            count += nbr * self.__countcontent(color)
        self.__bagcontentcache[bag] = count
        return count


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        rules = BagRules(file.read().strip('\n'))
    print(f"Part 1: {rules.countcontainedin("shiny gold")}")
    print(f"Part 2: {rules.countbagscontainedin("shiny gold")}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
