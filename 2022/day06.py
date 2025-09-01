import time
from pathlib import Path


class Signal:
    def __init__(self, rawstr: str) -> None:
        self.__buffer = rawstr

    def get_processed_characters(self, start_len: int = 4) -> int:
        for idx in range(len(self.__buffer) - (start_len - 1)):
            if len(set(self.__buffer[idx: idx + start_len])) == start_len:
                return idx + start_len
        return -1


def main(aoc_input: str) -> None:
    signal = Signal(aoc_input)
    print(f"Part 1: {signal.get_processed_characters()}")
    print(f"Part 2: {signal.get_processed_characters(14)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
