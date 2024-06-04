"""
Seems kind of brute-force-y, but performs much better than attempts to build divisor generator solutions.
Basically simulates the present delivery by iterating over the elfs from 1 and up. Small optimization to keep track
of the lowest house found yet reaching the target to avoid iterating further over higher houses that have no chance of
winning.
"""
import sys


def get_lowest_house(target: int) -> int:
    houses = [10 for _ in range(target // 10)]
    # Note 1 - We are guaranteed to hit the target at t/10 since each elf delivers 10 times its number
    # Note 2 - Zero indexing houses, i.e. houses[0] == House_1
    # Note 3 - We know the first elf will visit all houses, so initialize houses to 10 to skip the first iteration
    upper_bound = len(houses)
    for elf in range(2, len(houses) + 1):
        for i in range(elf - 1, upper_bound, elf):
            houses[i] += 10 * elf
            if houses[i] >= target:
                upper_bound = min(upper_bound, i + 1)
    return upper_bound


def get_lowest_house_lazy_elf(target: int) -> int:
    houses = [0 for _ in range(target // 11)]
    upper_bound = len(houses)
    for elf in range(1, len(houses) + 1):
        presents = 0
        for i in range(elf - 1, upper_bound, elf):
            presents += 1
            houses[i] += 11 * elf
            if houses[i] >= target:
                upper_bound = min(upper_bound, i + 1)
            if presents >= 50:
                break
    return upper_bound


def main() -> int:
    target = 36_000_000
    print(f"Part 1: {get_lowest_house(target)}")
    print(f"Part 2: {get_lowest_house_lazy_elf(target)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
