"""
Solution - rather than storing each and every lantern fish individually, simply store a list of internal timer states
0 - 8 and how many fish are in each state. When stepping a day, simply pop the first element in the list corresponding
to state-0 and add that number to state-6 and also append that number to state-8.
"""
import sys


class Fishies:
    def __init__(self, rawstr: str):
        nbrs = list(map(int, rawstr.split(',')))
        self.__states = [0 for _ in range(9)]
        for nbr in nbrs:
            self.__states[nbr] += 1

    def get_answers(self) -> tuple[int, int]:
        p1 = 0
        for n in range(256):
            state_0 = self.__states.pop(0)
            self.__states[6] += state_0
            self.__states.append(state_0)
            if n == 79:
                p1 = sum(self.__states)
        return p1, sum(self.__states)


def main() -> int:
    with open('../Inputfiles/aoc6.txt', 'r') as file:
        fishies = Fishies(file.read().strip('\n'))
    p1, p2 = fishies.get_answers()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
