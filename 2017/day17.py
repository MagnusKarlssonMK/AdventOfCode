"""
Part 1: Just build the buffer while keeping track of the current position.
Part 2: No need to actually build the buffer now, since the value 0 will always be in index 0, i.e. we are only looking
for the number in index 1 after 50M iterations. So all we need to do is to keep track of the current position and
update the current value of index 1 whenever it ends up there.
"""
import time
from pathlib import Path


class Spinlock:
    def __init__(self, rawstr: str) -> None:
        self.__steps = int(rawstr)

    def get_2017_insert(self) -> int:
        buffer = [0]
        current_pos = 0
        for nbr in range(1, 2018):
            current_pos = 1 + (current_pos + self.__steps) % nbr
            buffer.insert(current_pos, nbr)
        return buffer[current_pos + 1]

    def get_50m_pos1(self) -> int:
        pos_1 = -1
        current_pos = 0
        for nbr in range(1, 50_000_001):
            current_pos = 1 + (current_pos + self.__steps) % nbr
            if current_pos == 1:
                pos_1 = nbr
        return pos_1


def main(aoc_input: str) -> None:
    spinlock = Spinlock(aoc_input)
    print(f"Part 1: {spinlock.get_2017_insert()}")
    print(f"Part 2: {spinlock.get_50m_pos1()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day17.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
