"""
Pretty much just walk through the codes and store the character count in a dictionary for each position. This can then
be sorted (increasing or decreasing depending on part 1 or 2) to generate the result.
Just to make up for the time-consuming problem the previous day, make an unnecessary optimization to an already instant
calculation and generate the answers for both parts in one step.
"""
import time
from pathlib import Path


class Signal:
    def __init__(self, rawstr: str) -> None:
        self.__codes = rawstr.splitlines()

    def decode_signal(self) -> tuple[str, str]:
        counter: list[dict[str, int]] = [{} for _, _ in enumerate(self.__codes[0])]
        for code in self.__codes:
            for i, c in enumerate(code):
                if c not in counter[i]:
                    counter[i][c] = 1
                else:
                    counter[i][c] += 1
        signal = ''
        modified_signal = ''
        for cnt in counter:
            signal += sorted(list(cnt.items()), key=lambda x: x[1], reverse=True)[0][0]
            modified_signal += sorted(list(cnt.items()), key=lambda x: x[1], reverse=False)[0][0]
        return signal, modified_signal


def main(aoc_input: str) -> None:
    signal = Signal(aoc_input)
    p1, p2 = signal.decode_signal()
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2016/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
