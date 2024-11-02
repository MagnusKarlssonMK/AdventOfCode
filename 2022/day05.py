"""
Stores the input data in a crateship class, containing the crates and procedures. The answer is provided with a
method running the procedures. This is done on a local copy of the crate data to avoid having to create a copy
of the entire class for Part 2.
"""
import time
from pathlib import Path
import re
from copy import deepcopy


class Crateship:
    def __init__(self, cratestr: str, procedurestr: str):
        self.procedures = [tuple(map(int, re.findall(r'\d+', row))) for row in procedurestr.splitlines()]
        self.crates: dict[int: list[str]] = {}
        cratelines = cratestr.splitlines()
        for idx, line in enumerate(reversed(cratelines)):
            if idx == 0:
                for nbr in re.findall(r'\d', line):
                    self.crates[int(nbr)] = []
            else:
                for m in re.finditer(r'\w', line):
                    self.crates[int(cratelines[-1][m.start()])].append(line[m.start()])

    def run_procedures(self, multicrates: bool = False) -> str:
        crates = deepcopy(self.crates)
        for proc_nbr, proc_from, proc_to in self.procedures:
            for idx in range(proc_nbr):
                if multicrates:
                    movecrate = crates[proc_from].pop(idx - proc_nbr)
                else:
                    movecrate = crates[proc_from].pop()
                crates[proc_to].append(movecrate)
        return ''.join([crates[key][-1] for key in list(crates.keys())])


def main(aoc_input: str) -> None:
    ship = Crateship(*aoc_input.split('\n\n'))
    print(f"Part 1: {ship.run_procedures()}")
    print(f"Part 2: {ship.run_procedures(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2022/day05.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
