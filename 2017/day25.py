"""
Mostly just a bit of parsing headache. It would probably have been much easier to just manually hard code the input,
but resisting the temptation and using a bit of simple regex instead...
Then just keep track of the cursor position and store the positions set to 1 in a set.
"""
import time
from pathlib import Path
import re


class TuringMachine:
    def __init__(self, rawstr: str) -> None:
        blocks = rawstr.split('\n\n')
        self.__state = re.findall(r"state (\w).", blocks[0])[0]
        self.__diag_steps = int(re.findall(r"\d+", blocks[0])[0])
        self.__process: dict[str, dict[int, tuple[int, int, str]]] = {}  # state: (value: (new_v, direction, new_s))
        for block in blocks[1:]:
            states = re.findall(r"state (\w).", block)
            nbrs = list(map(int, re.findall(r"\d+", block)))
            directions = [1 if c == 'right' else -1 for c in re.findall(r"slot to the (\w+).", block)]
            self.__process[states[0]] = {nbrs[0]: (nbrs[1], directions[0], states[1]),
                                         nbrs[2]: (nbrs[3], directions[1], states[2])}

    def get_checksum(self) -> int:
        ones: set[int] = set()
        cursor_pos = 0
        for _ in range(self.__diag_steps):
            value = 1 if cursor_pos in ones else 0
            new_val, cursor_dir, new_state = self.__process[self.__state][value]
            if new_val == 1:
                ones.add(cursor_pos)
            elif cursor_pos in ones:
                ones.remove(cursor_pos)
            cursor_pos += cursor_dir
            self.__state = new_state
        return len(ones)


def main(aoc_input: str) -> None:
    machine = TuringMachine(aoc_input)
    print(f"Part 1: {machine.get_checksum()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2017/day25.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
