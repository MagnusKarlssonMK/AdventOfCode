import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2022/day06.txt')


class Signal:
    def __init__(self, rawstr: str) -> None:
        self.__buffer = rawstr

    def get_processed_characters(self, start_len: int = 4) -> int:
        for idx in range(len(self.__buffer) - (start_len - 1)):
            if len(set(self.__buffer[idx: idx + start_len])) == start_len:
                return idx + start_len


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        signal = Signal(file.read().strip('\n'))
    print(f"Part 1: {signal.get_processed_characters()}")
    print(f"Part 2: {signal.get_processed_characters(14)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
