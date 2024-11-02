"""
Store the input in a from->[to] dict for part 1, and in reverse form to->from for part 2.
For part 1, go through all the possible replacements and drop the result in a set, and at the end the length of the set
will give the answer.
For part 2, work backwards from the target molecule towards the origin 'e'. Go through the possible retrofits ignoring
the ones coming from 'e' until there are no more replacements, then do the replacements to 'e' and summarize the number
of replacements performed.
"""
import time
from pathlib import Path


class NuclearPlant:
    def __init__(self, rawstr: str) -> None:
        replacements, self.__molecule = rawstr.split('\n\n')
        self.__replacements: dict[str: list[str]] = {}
        self.__retrofits: dict[str: str] = {}
        for line in replacements.splitlines():
            left, right = line.split(' => ')
            if left not in self.__replacements:
                self.__replacements[left] = [right]
            else:
                self.__replacements[left].append(right)
            self.__retrofits[right] = left

    def get_molecule_count(self) -> int:
        altered_molecules = set()
        for replaced in self.__replacements:
            for replacement in self.__replacements[replaced]:
                for i, _ in enumerate(self.__molecule):
                    if self.__molecule[i: i + len(replaced)] == replaced:
                        altered_molecules.add(self.__molecule[: i] + replacement + self.__molecule[i + len(replaced):])
        return len(altered_molecules)

    def get_min_generation_time(self) -> int:
        steps = 0
        modified = True
        current: str = self.__molecule
        while modified:
            modified = False
            for target, source in self.__retrofits.items():
                if source == 'e':
                    continue
                if (count := current.count(target)) > 0:
                    current = current.replace(target, source)
                    modified = True
                    steps += count
        for target, source in self.__retrofits.items():
            if source != 'e':
                continue
            if (count := current.count(target)) > 0:
                current = current.replace(target, source)
                steps += count
        return steps


def main(aoc_input: str) -> None:
    plant = NuclearPlant(aoc_input)
    print(f"Part 1: {plant.get_molecule_count()}")
    print(f"Part 2: {plant.get_min_generation_time()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day19.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
