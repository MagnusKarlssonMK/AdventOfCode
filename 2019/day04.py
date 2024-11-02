"""
Valid passwords are generated with an iter function, minimizing the number of numbers to loop though by first finding
the lowest valid password and then for each increment, adjust to follow the rules if necessary before completing
the loop.
"""
import time
from pathlib import Path


class PasswordGenerator:
    def __init__(self, rawstr: str) -> None:
        self.__lower, self.__upper = list(map(int, rawstr.split('-')))

    def __generate_pwds(self, exactlytwo) -> iter:
        v_list = [int(c) for c in str(self.__lower)]
        # Find the first valid initial value starting from 'lower' - the value never decreases
        tmp = 0
        for i in range(1, len(v_list)):
            if tmp > 0:
                v_list[i] = tmp
            elif v_list[i] < v_list[i - 1]:
                v_list[i] = v_list[i - 1]
                tmp = v_list[i]
        value = int(''.join(map(str, v_list)))

        while value <= self.__upper:
            # valid pwd if two adjacent digits are the same
            tmp = v_list[0]
            counts = [1]
            for i in range(1, len(v_list)):
                if v_list[i] == tmp:
                    counts[-1] += 1
                else:
                    counts.append(1)
                    tmp = v_list[i]

            if not exactlytwo:
                if any([c > 1 for c in counts]):
                    yield value
            else:
                if any([c == 2 for c in counts]):
                    yield value

            # step the value, make sure to follow the 'never decreases' rule
            for i in reversed(range(len(v_list))):
                v_list[i] += 1
                if v_list[i] <= 9:
                    for j in range(i + 1, len(v_list)):
                        v_list[j] = v_list[i]
                    break
            value = int(''.join(map(str, v_list)))

    def get_password_count(self, exactlytwo: bool = False) -> int:
        return sum([1 for _ in self.__generate_pwds(exactlytwo)])


def main(aoc_input: str) -> None:
    pwdgen = PasswordGenerator(aoc_input)
    print(f"Part 1: {pwdgen.get_password_count()}")
    print(f"Part 2: {pwdgen.get_password_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
