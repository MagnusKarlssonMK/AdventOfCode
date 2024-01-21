import sys
import networkx as nx
import math


def main() -> int:
    graph = nx.Graph()

    with open("aoc25.txt", "r") as file:
        for line in file:
            left, right = (part.strip() for part in line.split(":"))
            right_parts = right.split()
            graph.add_node(left)
            [graph.add_edge(left, r, capacity=1.0) for r in right_parts]

    result_p1 = None
    print(graph)
    left = next(iter(graph.nodes))
    for right in graph.nodes:
        if left != right:
            cut_val, partitions = nx.minimum_cut(graph, left, right)
            if cut_val == 3:
                print(partitions)
                result_p1 = math.prod(len(partition) for partition in partitions)
                break

    print("Part1: ", result_p1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
