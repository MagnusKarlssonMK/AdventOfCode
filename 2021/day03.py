import time
from pathlib import Path


class Diagnostics:
    def __init__(self, rawstr: str) -> None:
        self.__lines = rawstr.splitlines()
        self.__nbrbits = len(self.__lines[0])

    def __get_most_and_least_common(self, inlist: list[str]) -> tuple[str, str]:
        gamma = [0 for _ in range(self.__nbrbits)]
        for line in inlist:
            for i, c in enumerate(line):
                gamma[i] += int(c)
        for bit_idx in range(self.__nbrbits):
            gamma[bit_idx] = min(1, 2 * gamma[bit_idx] // len(inlist))
        epsilon = [(i + 1) % 2 for i in gamma]
        return "".join(list(map(str, gamma))), "".join(list(map(str, epsilon)))

    def getpowerconsumption(self) -> int:
        mostcommon, leastcommon = self.__get_most_and_least_common(self.__lines)
        return int(mostcommon, 2) * int(leastcommon, 2)

    def getlifesupportrating(self) -> int:
        return self.__getrating(0) * self.__getrating(1)

    def __getrating(self, most_least: int) -> int:
        nbrlist = list(self.__lines)
        for bit_idx in range(self.__nbrbits):
            if len(nbrlist) <= 1:
                break
            matchnbrs = self.__get_most_and_least_common(nbrlist)
            nbrlist = [line for line in nbrlist if line[bit_idx] == matchnbrs[most_least][bit_idx]]
        return int(nbrlist[0], 2)


def main(aoc_input: str) -> None:
    mydiag = Diagnostics(aoc_input)
    print(f"Part 1: {mydiag.getpowerconsumption()}")
    print(f"Part 2: {mydiag.getlifesupportrating()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
