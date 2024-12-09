import time
from pathlib import Path


class Disk:
    def __init__(self, rawstr: str) -> None:
        self.__diskmap = [int(c) for c in rawstr]

    def get_fragmented_checksum(self) -> int:
        left_idx = 0
        right_idx = len(self.__diskmap) - 1
        if right_idx % 2 == 1:
            right_idx -= 1
        right_counter = self.__diskmap[right_idx]
        target_idx = 0
        checksum = 0
        buffer = self.__diskmap[left_idx]
        while right_idx >= left_idx:
            if buffer > 0:
                if left_idx % 2 == 0:
                    buffer -= 1
                    checksum += target_idx * left_idx // 2
                    target_idx += 1
                elif right_counter > 0:
                    buffer -= 1
                    right_counter -= 1
                    checksum += target_idx * right_idx // 2
                    target_idx += 1
                else:
                    right_idx -= 2
                    right_counter = self.__diskmap[right_idx]
            else:
                left_idx += 1
                buffer = right_counter if left_idx == right_idx else self.__diskmap[left_idx]
        return checksum

    def get_defragmented_checksum(self) -> int:
        emptyblocks = []
        mempos = 0
        for i, v in enumerate(self.__diskmap):
            if i % 2 == 1 and v > 0:
                emptyblocks.append((mempos, v))
            mempos += v
        checksum = 0
        for memid, memlen in reversed(list(enumerate(self.__diskmap))):
            # Note: the memory id is actually half the index, so divide memid by 2 later when used
            mempos -= memlen
            if memid % 2 == 0:
                moved = False
                for eidx, (e_start, e_len) in enumerate(emptyblocks):
                    if e_start >= mempos:
                        break
                    if e_len >= memlen:
                        checksum += sum([i * memid // 2 for i in range(e_start, e_start + memlen)])
                        if e_len - memlen > 0:
                            emptyblocks[eidx] = e_start + memlen, e_len - memlen
                        else:
                            emptyblocks.pop(eidx)
                        moved = True
                        break
                if not moved:
                    checksum += sum([i * memid // 2 for i in range(mempos, mempos + memlen)])
        return checksum


def main(aoc_input: str) -> None:
    p = Disk(aoc_input)
    print(f"Part 1: {p.get_fragmented_checksum()}")
    print(f"Part 2: {p.get_defragmented_checksum()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day09.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
