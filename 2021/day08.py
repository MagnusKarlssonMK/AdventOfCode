"""
Part 1 - straightforward; simply parse the input data, then count number of elements on the right side of the divider
with lenght of 2, 3, 4 or 7 and add up.
Part 2 - a bit more complicated. Start with the left side, identify 1, 4, 7 and 8 by their unique lengths. The segment
mapping to 'a' can then be determined from the difference between 1 and 7. Then 3 can be identified by looking at
the signals with length 5, where 3 will be the only one containing the entire 7. With this, by looking at 4 now we
can determine the segment mapping to 'b' and 'd'. From here on we should have enough information to identify the
rest of the numbers and mappings.
Store the signals in sets to be able to use the '-' operator to find the difference between numbers.
"""
import time
from pathlib import Path


class Display:
    NumSegMap: dict[int: str] = {0: set('abcefg'), 1: set('cf'), 2: set('acdeg'), 3: set('acdfg'), 4: set('bcdf'),
                                 5: set('abdfg'), 6: set('abdefg'), 7: set('acf'), 8: set('abcdefg'), 9: set('abcdfg')}

    def __init__(self, rawstr: str) -> None:
        self.__lines = [(row[0].split(), row[1].split()) for row in
                        [line.split(' | ') for line in rawstr.splitlines()]]

    def get_1478_count(self) -> int:
        p1_result = 0
        for _, right in self.__lines:
            p1_result += sum([1 for word in right if len(word) in (2, 3, 4, 7)])
        return p1_result

    def get_output_sum(self) -> int:
        return sum([self.__set_wires(i) for i, _ in enumerate(self.__lines)])

    def __set_wires(self, line_idx: int) -> int:
        pattern, output = self.__lines[line_idx]
        """Takes the corrupted input pattern and output and returns the actual correct output"""
        numbers: dict[int: list[set[str]]] = {nbr: [] for nbr in range(10)}
        mapping: dict[str: str] = {}
        for p in pattern:  # Store candidate signals for each number based on length
            for key in Display.NumSegMap:
                if len(p) == len(Display.NumSegMap[key]):
                    numbers[key].append(set(p))
        mapping['a'] = numbers[7][0] - numbers[1][0]  # Determine 'a' from 7 and 1
        [numbers[3].pop(n) for n in reversed(range(len(numbers[3]))) if len(numbers[7][0] - numbers[3][n]) > 0]  # Id 3
        mapping['b'] = numbers[4][0] - numbers[3][0]  # Determine 'b' from 4 and 3
        mapping['d'] = numbers[4][0] - numbers[1][0] - mapping['b']
        [numbers[2].pop(n) for n in reversed(range(len(numbers[2])))
            if len(mapping['b'] - numbers[2][n]) == 0 or numbers[2][n] == numbers[3][0]]  # Id 2
        [numbers[5].pop(n) for n in reversed(range(len(numbers[5])))
            if len(mapping['b'] - numbers[5][n]) > 0 or numbers[5][n] == numbers[3][0]]  # Id 5
        mapping['c'] = numbers[7][0] - numbers[5][0]  # Determine 'c' from 7 and 5
        mapping['f'] = numbers[7][0] - numbers[2][0]  # Determine 'c' from 7 and 2
        mapping['e'] = numbers[2][0] - numbers[3][0]  # Determine 'c' from 2 and 3
        mapping['g'] = numbers[3][0] - numbers[7][0] - mapping['d']  # Determine 'c' from 2 and 3

        # Invert the map and translate the output
        imapping = {''.join(v): k for k, v in mapping.items()}
        retstr = ''
        for signal in output:
            sigset = {imapping[c] for c in signal}
            for nbr in Display.NumSegMap:
                if sigset == Display.NumSegMap[nbr]:
                    retstr += str(nbr)
                    break
        return int(retstr)


def main(aoc_input: str) -> None:
    display = Display(aoc_input)
    print(f"Part 1: {display.get_1478_count()}")
    print(f"Part 2: {display.get_output_sum()}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2021/day08.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
