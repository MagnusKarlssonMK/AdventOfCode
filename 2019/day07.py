"""
"""
import time
from pathlib import Path
from itertools import permutations
from intcode import Intcode, IntResult


class AmplifierArray:
    def __init__(self, rawstr: str) -> None:
        self.__amps = [Intcode(list(map(int, rawstr.split(',')))) for _ in range(5)]

    def get_max_thruster_signal(self) -> int:
        result = 0
        for phase_inputs in permutations(range(0, 5)):
            out = 0
            for i, p_i in enumerate(phase_inputs):
                self.__amps[i].add_input(p_i)
                self.__amps[i].add_input(out)
                out, _ = self.__amps[i].run_program()
                self.__amps[i].reboot()
            result = max(result, out)
        return result

    def get_max_feedback_loop_signal(self) -> int:
        result = 0
        for phase_inputs in permutations(range(5, 10)):
            for i, amp in enumerate(self.__amps):
                amp.reboot()
                amp.add_input(phase_inputs[i])
            out = 0
            amp = 0
            while True:
                self.__amps[amp].add_input(out)
                val, res = self.__amps[amp].run_program()
                if res == IntResult.OUTPUT:
                    out = val
                else:
                    break
                amp = (amp + 1) % len(self.__amps)
            result = max(result, out)
        return result


def main(aoc_input: str) -> None:
    amps = AmplifierArray(aoc_input)
    print(f"Part 1: {amps.get_max_thruster_signal()}")
    print(f"Part 2: {amps.get_max_feedback_loop_signal()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2019/day07.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
