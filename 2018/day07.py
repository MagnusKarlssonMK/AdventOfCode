"""
Store the step rules in a dict, then keep track of which steps are done (and working for part 2) to figure out
which steps are available.
"""
import time
from pathlib import Path


class SleighKit:
    def __init__(self, rawstr: str) -> None:
        self.__steprules: dict[str: set[str]] = {}
        for line in rawstr.splitlines():
            w = line.split()
            if w[1] not in self.__steprules:
                self.__steprules[w[1]] = set()
            if w[7] not in self.__steprules:
                self.__steprules[w[7]] = set()
            self.__steprules[w[7]].add(w[1])

    def get_step_order(self) -> str:
        done = []
        # Sorted list so that we choose alphabetically when multiple steps are available
        not_done = sorted([step for step in self.__steprules])
        while not_done:
            available = None
            for i, step in enumerate(not_done):
                for req in self.__steprules[step]:
                    if req not in done:
                        break
                else:
                    available = not_done.pop(i)
                if available:
                    done.append(available)
                    break
        return ''.join(done)

    def get_step_count(self, additional_workers: int = 4, flatcost: int = 60) -> int:
        done = []
        not_done = sorted([step for step in self.__steprules])
        working: dict[str: int] = {}
        seconds = 0
        while not_done or working:
            isdone = []
            for w in working:
                if working[w] == 0:
                    isdone.append(w)
                else:
                    working[w] -= 1
            for d in isdone:
                done.append(d)
                working.pop(d)
            seconds += 1
            available = []
            for step in not_done:
                for req in self.__steprules[step]:
                    if req not in done:
                        break
                else:
                    available.append(step)
            for a in available:
                if len(working) < 1 + additional_workers:
                    working[a] = flatcost + ord(a) - ord('A')
                    not_done.remove(a)
                else:
                    break
        return seconds - 1


def main(aoc_input: str) -> None:
    sleigh = SleighKit(aoc_input)
    print(f"Part 1: {sleigh.get_step_order()}")
    print(f"Part 2: {sleigh.get_step_count()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2018/day07.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
