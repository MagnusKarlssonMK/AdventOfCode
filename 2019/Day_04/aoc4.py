"""
Valid passwords are generated with an iter function, minimizing the number of numbers to loop though by first finding
the lowest valid password and then for each increment, adjust to follow the rules if necessary before completing
the loop.
"""
import sys


def generate_pwds(lower: int, upper: int) -> iter:
    v_list = [int(c) for c in str(lower)]
    # Find the first valid initial value starting from 'lower'
    tmp = 0
    for i in range(1, len(v_list)):
        if tmp > 0:
            v_list[i] = tmp
        elif v_list[i] < v_list[i - 1]:
            v_list[i] = v_list[i - 1]
            tmp = v_list[i]
    value = int(''.join(map(str, v_list)))

    while value <= upper:
        if any([v_list[i] == v_list[i - 1] for i in range(1, len(v_list))]):
            yield value
        for i in reversed(range(len(v_list))):
            v_list[i] += 1
            if v_list[i] <= 9:
                for j in range(i + 1, len(v_list)):
                    v_list[j] = v_list[i]
                break
        value = int(''.join(map(str, v_list)))


def main() -> int:
    with open('../Inputfiles/aoc4.txt', 'r') as file:
        lower, upper = file.read().strip('\n').split('-')
    print("Part 1:", sum([1 for _ in generate_pwds(int(lower), int(upper))]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
