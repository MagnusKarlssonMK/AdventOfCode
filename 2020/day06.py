"""
Collect the data per group in sets. For Part 1, just combine the sets for each person in the group to get the answer.
For Part 2 instead get the shared values in the sets for all persons in the group. This can be done with the same
function just passing the comparison function as an input.
"""
import time
from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Group:
    answers: list[str]

    def get_yes_count(self, everyone: bool) -> int:
        yes = set(self.answers[0])
        for i in range(1, len(self.answers)):
            yes = yes | set(self.answers[i]) if not everyone else yes & set(self.answers[i])
        return len(yes)


class Forms:
    def __init__(self, rawstr: str) -> None:
        self.__groups = [Group(g.splitlines()) for g in rawstr.split('\n\n')]

    def get_yes_count(self, everyone: bool = False) -> int:
        return sum([group.get_yes_count(everyone) for group in self.__groups])


def main(aoc_input: str) -> None:
    forms = Forms(aoc_input)
    print(f"Part 1: {forms.get_yes_count()}")
    print(f"Part 2: {forms.get_yes_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day06.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
