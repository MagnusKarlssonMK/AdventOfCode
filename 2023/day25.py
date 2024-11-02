"""
Uses the 'minimum cut' function from nx module to determine the answer.
(Saving it for a rainy day to figure out how this actually works.)
"""
import time
from pathlib import Path
import networkx as nx
import math


class Machine:
    def __init__(self, rawstr: str) -> None:
        self.__graph = nx.Graph()
        for line in rawstr.splitlines():
            left, right = [part.strip() for part in line.split(': ')]
            self.__graph.add_node(left)
            [self.__graph.add_edge(left, r, capacity=1.0) for r in right.split()]

    def get_group_size_multiple(self) -> int:
        left = next(iter(self.__graph.nodes))
        for right in self.__graph.nodes:
            if left != right:
                cut_val, partitions = nx.minimum_cut(self.__graph, left, right)
                if cut_val == 3:
                    return math.prod(len(p) for p in partitions)
        return -1


def main(aoc_input: str) -> None:
    machine = Machine(aoc_input)
    print(f"Part 1: {machine.get_group_size_multiple()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2023/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
