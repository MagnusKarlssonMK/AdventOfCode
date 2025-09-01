"""
Gets the answer to both parts in one go by playing rounds until nothing moves, and records the scores for each round
in a dict along the way. Elf positions are stored in a dict with a mapped integer corresponding to bitmasked
neighbors.
NOT a fast solution, but gets the job done (completes in about 10s). Not sure how it can be further optimized.
"""
import time
from pathlib import Path


class MapScan:
    def __init__(self, gridinput: str) -> None:
        self.__elfs: dict[tuple[int, int], int] = {(x, y): 0 for y, row in enumerate(gridinput.splitlines())
                                                   for x, col in enumerate(row) if col == "#"}
        self.__directionmasks = [int('11100000', 2), int('00000111', 2), int('10010100', 2), int('00101001', 2)]
        xy = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.__dxdy: dict[int, tuple[int, int]] = {mask: xy[i] for i, mask in enumerate(self.__directionmasks)}
        self.__surroundings = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        self.__surroundmasks = [2**x for x in reversed(range(len(self.__surroundings)))]
        self.__scoretable: dict[int, int] = {0: self.__get_currentscore()}

    def __update_elf_neighbors(self) -> None:
        for elf_x, elf_y in self.__elfs:
            self.__elfs[(elf_x, elf_y)] = 0
            for i, (dx, dy) in enumerate(self.__surroundings):
                if (elf_x + dx, elf_y + dy) in self.__elfs:
                    self.__elfs[(elf_x, elf_y)] |= self.__surroundmasks[i]

    def get_roundscore(self, rounds: int) -> int:
        if rounds in self.__scoretable:
            return self.__scoretable[rounds]
        return self.__scoretable[len(self.__scoretable) - 1]

    def get_stablerounds(self) -> int:
        return max(self.__scoretable.keys())

    def run_simulation(self) -> None:
        stable = False
        i = 1
        while not stable:
            stable = self.__play_round()
            self.__scoretable[i] = self.__get_currentscore()    # Record the score
            self.__directionmasks.append(self.__directionmasks.pop(0))  # Rotate the prio list
            i += 1

    def __play_round(self) -> bool:
        proposed: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self.__update_elf_neighbors()
        for elf in self.__elfs:
            if self.__elfs[elf] > 0:
                for dm in self.__directionmasks:
                    if self.__elfs[elf] & dm == 0:
                        x, y = elf
                        dx, dy = self.__dxdy[dm]
                        if (x + dx, y + dy) in proposed:
                            proposed[(x + dx, y + dy)].append((x, y))
                        else:
                            proposed[(x + dx, y + dy)] = [(x, y)]
                        break
        changed = False
        for p in proposed:
            if len(proposed[p]) == 1:
                self.__elfs[p] = 0
                self.__elfs.pop(proposed[p][0])
                changed = True
        return not changed

    def __get_currentscore(self) -> int:
        x_min = min(self.__elfs, key=lambda x: x[0])[0]
        x_max = max(self.__elfs, key=lambda x: x[0])[0]
        y_min = min(self.__elfs, key=lambda x: x[1])[1]
        y_max = max(self.__elfs, key=lambda x: x[1])[1]
        return sum((x, y) not in self.__elfs for y in range(y_min, y_max + 1) for x in range(x_min, x_max + 1))


def main(aoc_input: str) -> None:
    elfs = MapScan(aoc_input)
    elfs.run_simulation()
    print(f"Part 1: {elfs.get_roundscore(10)}")
    print(f"Part 2: {elfs.get_stablerounds()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day23.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
