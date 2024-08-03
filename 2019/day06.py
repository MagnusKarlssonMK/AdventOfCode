"""
Store the orbits in two formats inside an orbit class - one dict to get all the objects orbiting a certain object,
and one 'reversed' variant for Part 2 to get the parent object for each object. From there it's simple recursion
to get the answer for Part 1. For Part 2, recurse through the second dict to get the paths from YOU -> COM and
SAN -> COM, then find where those two paths meet and get the answer from the remaining length of both paths.
"""
import sys


class OrbitMap:
    def __init__(self, indata: list[str]):
        self.__orbits: dict[str: list[str]] = {}
        self.__orbiting: dict[str: str] = {}
        self.__you = ''
        self.__santa = ''
        for line in indata:
            left, right = line.split(')')
            if left not in self.__orbits:
                self.__orbits[left] = [right]
            else:
                self.__orbits[left].append(right)
            if right == 'YOU':
                self.__you = left
            if right == 'SAN':
                self.__santa = left
            self.__orbiting[right] = left

    def get_orbitcount(self) -> int:
        return sum([self.__get_allorbits(x) for x in self.__orbits])

    def __get_allorbits(self, obj: str) -> int:
        if obj not in self.__orbits:
            return 0
        return sum([1 + self.__get_allorbits(x) for x in self.__orbits[obj]])

    def get_santadistance(self) -> int:
        you_path = [self.__you]
        while you_path[-1] != 'COM':
            you_path.append(self.__orbiting[you_path[-1]])
        santa_path = [self.__santa]
        while santa_path[-1] != 'COM':
            santa_path.append(self.__orbiting[santa_path[-1]])
        while you_path[-1] == santa_path[-1]:
            you_path.pop()
            santa_path.pop()
        # Note: we chopped off also the connecting node, so it should have been this +1. But we also want the number
        # of edges, not number of nodes, so it would be number of nodes -1. So it cancels out.
        return len(you_path) + len(santa_path)


def main() -> int:
    with open('../Inputfiles/aoc6.txt', 'r') as file:
        mymap = OrbitMap(file.read().strip('\n').splitlines())
    print(f"Part 1: {mymap.get_orbitcount()}")
    print(f"Part 2: {mymap.get_santadistance()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
