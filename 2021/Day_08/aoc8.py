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
import sys

NumSegMap: dict[int: str] = {0: set('abcefg'), 1: set('cf'), 2: set('acdeg'), 3: set('acdfg'), 4: set('bcdf'),
                             5: set('abdfg'), 6: set('abdefg'), 7: set('acf'), 8: set('abcdefg'), 9: set('abcdfg')}


def setwires(pattern: list[str], output: list[str]) -> int:
    """Takes the corrupted input pattern and output and returns the actual correct output"""
    numbers: dict[int: list[set[str]]] = {nbr: [] for nbr in range(10)}
    mapping: dict[str: str] = {}
    for p in pattern:  # Store candidate signals for each number based on length
        for key in list(NumSegMap.keys()):
            if len(p) == len(NumSegMap[key]):
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
        sigset = set()
        [sigset.add(imapping[c]) for c in signal]
        for nbr in list(NumSegMap.keys()):
            if sigset == NumSegMap[nbr]:
                retstr += str(nbr)
                break
    return int(retstr)


def main() -> int:
    with open('../Inputfiles/aoc8.txt', 'r') as file:
        lines = [(row[0].split(), row[1].split()) for row in [line.split(' | ')
                                                              for line in file.read().strip('\n').splitlines()]]
        p1_result = 0
        for line in lines:
            p1_result += sum([1 for word in line[1] if len(word) in (2, 3, 4, 7)])
        print("Part 1: ", p1_result)
        print("Part 2: ", sum([setwires(row[0], row[1]) for row in lines]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
