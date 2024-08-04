"""
A bit of regex generation and recursion.
"""
import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day19.txt')


class SatelliteData:
    def __init__(self, rawstr: str) -> None:
        rules, messages = rawstr.split('\n\n')
        self.__messages = messages.splitlines()
        self.__rules = {}
        for rule in rules.splitlines():
            left, right = rule.split(': ')
            self.__rules[int(left)] = [[c.strip("\"") for c in s.split()] for s in right.split(" | ")]

    def __gen_regex(self, rule: int = 0, depth: int = 20) -> str:
        if depth == 0:
            return ''
        if self.__rules[rule][0][0].isdigit():
            return '(' + '|'.join([''.join([self.__gen_regex(int(s), depth - 1) for s in sub])
                                   for sub in self.__rules[rule]]) + ')'
        return self.__rules[rule][0][0]

    def get_matching_0(self) -> int:
        r = re.compile(self.__gen_regex())
        result = [r.fullmatch(msg) for msg in self.__messages]
        return len([valid for valid in result if valid])

    def update_and_get_matching_0(self) -> int:
        self.__rules[8] = [['42'], ['42', '8']]
        self.__rules[11] = [['42', '31'], ['42', '11', '31']]
        return self.get_matching_0()


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        data = SatelliteData(file.read().strip('\n'))
    print(f"Part 1: {data.get_matching_0()}")
    print(f"Part 2: {data.update_and_get_matching_0()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
