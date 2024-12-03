import time
from pathlib import Path


def calculate(block: str) -> int:
    total = 0
    for part in block.split("mul("):
        mul = part.split(")")
        if len(mul) > 1:  # contained at least one closing parenthesis
            nbrs = mul[0].split(",")
            if len(nbrs) == 2 and nbrs[0].isdigit() and nbrs[1].isdigit():
                total += int(nbrs[0]) * int(nbrs[1])
    return total


class Program:
    def __init__(self, rawstr: str) -> None:
        self.__program = rawstr

    def get_basic_calculation(self) -> int:
        return calculate(self.__program)

    def get_accurrate_calculation(self) -> int:
        return sum([calculate(block.split("don't()")[0]) for block in self.__program.split("do()")])


def main(aoc_input: str) -> None:
    program = Program(aoc_input)
    print(f"Part 1: {program.get_basic_calculation()}")
    print(f"Part 2: {program.get_accurrate_calculation()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2024/day03.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
