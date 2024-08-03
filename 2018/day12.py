"""
1D game of life kind of.
Store the pot state as a set of indices containing a plant, to make it a bit easier to deal with the growing sides, and
temporarily convert it to string while creating a new generation.
Part 1: simply generate 20 times and take the sum of the set of pots.
Part 2: the sum increase for each generation will eventually converge to a constant value, so keep looping new
generations and checking the increase, and once it seems to have settled (using 10 times repeated delta here), we can
calculate the final value.
"""
import sys


class Tunnel:
    def __init__(self, rawstr: str) -> None:
        block_a, block_b = rawstr.split('\n\n')
        _, _, pots = block_a.split()
        self.__initialstate = set([i for i, c in enumerate(pots) if c == "#"])
        self.__spread = {left: right for left, right in [line.split(' => ') for line in block_b.splitlines()]}

    def __generate(self, pots: set[int]) -> set[int]:
        result: set[int] = set()
        for i in range(min(pots) - 2, max(pots) + 3):
            if self.__spread[''.join(["#" if j in pots else "." for j in range(i - 2, i + 3)])] == "#":
                result.add(i)
        return result

    def get_pot_sum_small(self) -> int:
        pots = set(self.__initialstate)
        for _ in range(20):
            pots = self.__generate(pots)
        return sum(pots)

    def get_pot_sum_large(self) -> int:
        pots = set(self.__initialstate)
        generations = 0
        delta = 0
        delta_count = 0
        while delta_count < 20:
            potsum = sum(pots)
            pots = self.__generate(pots)
            newpotsum = sum(pots)
            if newpotsum - potsum == delta:
                delta_count += 1
            else:
                delta = newpotsum - potsum
                delta_count = 0
            generations += 1
        return sum(pots) + delta * (50_000_000_000 - generations)


def main() -> int:
    with open('../Inputfiles/aoc12.txt', 'r') as file:
        tunnel = Tunnel(file.read().strip('\n'))
    print(f"Part 1: {tunnel.get_pot_sum_small()}")
    print(f"Part 2: {tunnel.get_pot_sum_large()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
