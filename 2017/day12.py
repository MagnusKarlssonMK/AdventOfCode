"""
Although the description sort of teases with 'travelling salesman', this actually only comes down to a number of
simple BFS's through the map to find out which nodes are connected.
"""
import time
from pathlib import Path


class Village:
    def __init__(self, rawstr: str) -> None:
        self.__programs: dict[int, set[int]] = {}
        for line in rawstr.splitlines():
            left, right = line.split(' <-> ')
            self.__programs[int(left)] = set(map(int, right.split(', ')))
        self.__unsorted = [i for i in self.__programs]
        self.__sorted: list[set[int]] = []

    def __process_group_containing(self, nbr: int) -> None:
        seen: set[int] = set()
        queue = [nbr]
        while queue:
            current = queue.pop(0)
            if current in seen:
                continue
            seen.add(current)
            for n in self.__programs[current]:
                queue.append(n)
        self.__sorted.append(seen)
        for s in seen:
            self.__unsorted.remove(s)

    def get_group_0_size(self) -> int:
        self.__process_group_containing(0)
        return len(self.__sorted[0])

    def get_groups_count(self) -> int:
        while self.__unsorted:
            self.__process_group_containing(self.__unsorted[0])
        return len(self.__sorted)


def main(aoc_input: str) -> None:
    village = Village(aoc_input)
    print(f"Part 1: {village.get_group_0_size()}")
    print(f"Part 2: {village.get_groups_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day12.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
