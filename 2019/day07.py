"""
"""
import sys
from pathlib import Path
from itertools import permutations
from intcode import Intcode, IntResult

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2019/day07.txt')


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


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        amps = AmplifierArray(file.read().strip('\n'))
    print(f"Part 1: {amps.get_max_thruster_signal()}")
    print(f"Part 2: {amps.get_max_feedback_loop_signal()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
