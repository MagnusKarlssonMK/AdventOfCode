"""
Build a computer class to hold the data and run the program, taking the first two values as input.
"""
import time
from pathlib import Path
from intcode import Intcode, IntResult


class Computer:
    __CORRECT_OUTPUT = 19690720

    def __init__(self, rawstr: str) -> None:
        self.__cpu = Intcode(list(map(int, rawstr.split(','))))

    def get_alarmstate(self) -> int:
        self.__cpu.override_program(1, 12)
        self.__cpu.override_program(2, 2)
        while True:
            _, res = self.__cpu.run_program()
            if res == IntResult.HALTED:
                break
        return self.__cpu.read_memory(0)

    def find_correct_inputs(self) -> int:
        for noun in range(100):
            for verb in range(100):
                self.__cpu.reboot()
                self.__cpu.override_program(1, noun)
                self.__cpu.override_program(2, verb)
                while True:
                    _, res = self.__cpu.run_program()
                    if res == IntResult.HALTED:
                        if self.__cpu.read_memory(0) == Computer.__CORRECT_OUTPUT:
                            return noun * 100 + verb
                        break
        return -1


def main(aoc_input: str) -> None:
    computer = Computer(aoc_input)
    print(f"Part 1: {computer.get_alarmstate()}")
    print(f"Part 2: {computer.find_correct_inputs()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day02.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
