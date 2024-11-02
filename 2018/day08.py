"""
Recursive solution for both parts.
"""
import time
from pathlib import Path


class NavigationSystem:
    def __init__(self, rawstr: str) -> None:
        self.__nbrs = list(map(int, rawstr.split()))

    def __decode_node(self, idx: int) -> tuple[int, int]:
        child_count, meta_count = self.__nbrs[idx], self.__nbrs[idx + 1]
        next_idx = idx + 2
        meta_sum = 0
        for _ in range(child_count):
            next_idx, child_meta = self.__decode_node(next_idx)
            meta_sum += child_meta
        meta_sum += sum(self.__nbrs[next_idx: next_idx + meta_count])
        return next_idx + meta_count, meta_sum

    def __get_node_value(self, idx: int) -> tuple[int, int]:
        child_count, meta_count = self.__nbrs[idx], self.__nbrs[idx + 1]
        next_idx = idx + 2
        child_metas = []
        for _ in range(child_count):
            next_idx, child_meta = self.__get_node_value(next_idx)
            child_metas.append(child_meta)
        meta_values = self.__nbrs[next_idx: next_idx + meta_count]
        if child_count == 0:
            return next_idx + meta_count, sum(meta_values)
        # Note: the meta values as child references are 1-indexed; our local list is not.
        meta_sum = sum([child_metas[mv - 1] for mv in meta_values if 1 <= mv <= len(child_metas)])
        return next_idx + meta_count, meta_sum

    def get_metadata_sum(self) -> int:
        return self.__decode_node(0)[1]

    def get_root_value(self) -> int:
        return self.__get_node_value(0)[1]


def main(aoc_input: str) -> None:
    navigationsystem = NavigationSystem(aoc_input)
    print(f"Part 1: {navigationsystem.get_metadata_sum()}")
    print(f"Part 2: {navigationsystem.get_root_value()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
