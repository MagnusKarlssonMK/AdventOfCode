"""
Re-use the knot hasher from day 10, and use that to generate a grid of one's and zero's, which in turn is converted
to an adjacency graph of neighboring ones. The answer for part 1 is then the number of keys in that graph / dict.
For part 2, simply traverse through the graph with a simple BFS to identify the groups, similar to the solution for
day 12.
"""
import sys
from pathlib import Path

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2017/day14.txt')


class KnotHasher:
    __NBR_OF_ELEMENTS = 256

    def __init__(self) -> None:
        self.__current_pos = 0
        self.__skipsize = 0

    def __generate_hash(self, input_list: list[int], lengths: list[int]) -> list[int]:
        nbrs = [i for i in input_list]
        for length in lengths:
            if length > len(nbrs):
                continue
            buffer = [nbrs[n % len(nbrs)] for n in range(self.__current_pos, self.__current_pos + length)]
            while buffer:
                nbrs[self.__current_pos] = buffer.pop()
                self.__current_pos = (self.__current_pos + 1) % len(nbrs)
            self.__current_pos = (self.__current_pos + self.__skipsize) % len(nbrs)
            self.__skipsize += 1
        return nbrs

    def get_knot_hash(self, rawstr: str) -> str:
        input_vec = [ord(c) for c in rawstr] + [17, 31, 73, 47, 23]
        sparse = [i for i in range(KnotHasher.__NBR_OF_ELEMENTS)]
        for _ in range(64):
            sparse = self.__generate_hash(sparse, input_vec)
        self.__current_pos = 0
        self.__skipsize = 0
        dense = []
        for block_idx in range(0, 256, 16):
            val = sparse[block_idx]
            for i in range(1, 16):
                val ^= sparse[block_idx + i]
            dense.append(val)
        return ''.join([f"{v:0>2x}" for v in dense])  # Convert to hex representation and enforce two digits


class Disk:
    def __init__(self, rawstr: str) -> None:
        knot = KnotHasher()
        grid = [bin(int(knot.get_knot_hash(rawstr + f'-{i}'), 16)).zfill(130)[2:] for i in range(128)]
        width = len(grid[0])
        height = len(grid)
        self.__adj: dict[tuple[int, int]: set[tuple[int, int]]] = {}
        for r in range(len(grid)):
            for c in range(len(grid)):
                if grid[r][c] == '1':
                    if (r, c) not in self.__adj:
                        self.__adj[(r, c)] = set()
                    for dr, dc in ((0, 1), (1, 0)):
                        if 0 <= r + dr < height and 0 <= c + dc < width and grid[r + dr][c + dc] == '1':
                            self.__adj[(r, c)].add((r + dr, c + dc))
                            if (r + dr, c + dc) not in self.__adj:
                                self.__adj[(r + dr, c + dc)] = set()
                            self.__adj[(r + dr, c + dc)].add((r, c))

    def get_squares_count(self) -> int:
        return len(self.__adj)

    def get_groups_count(self) -> int:
        groups = 0
        squares = list(self.__adj.keys())
        while squares:
            seen = set()
            queue = [squares[0]]
            while queue:
                current = queue.pop(0)
                if current in seen:
                    continue
                seen.add(current)
                for n in self.__adj[current]:
                    queue.append(n)
                squares.remove(current)
            groups += 1
        return groups


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        disk = Disk(file.read().strip('\n'))
    print(f"Part 1: {disk.get_squares_count()}")
    print(f"Part 2: {disk.get_groups_count()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
