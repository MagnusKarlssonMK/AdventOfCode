"""

"""
import sys
from collections import Counter


class Polymer:
    def __init__(self, template: str, rules: list[tuple[str, str]]):
        self.chain = template
        self.rules: dict[str: str] = {}
        for left, right in rules:
            self.rules[left] = right

    def takestep(self):
        result = ""
        for i in range(len(self.chain) - 1):
            result += self.chain[i] + self.rules[self.chain[i:i+2]]
        self.chain = result + self.chain[-1]


def main() -> int:
    with open('../Inputfiles/aoc14.txt', 'r') as file:
        template, r = file.read().strip('\n').split('\n\n')
    rules = [(left, right) for left, right in [line.split(' -> ') for line in r.splitlines()]]
    poly = Polymer(template, rules)
    for i in range(10):
        poly.takestep()
    result = sorted(Counter(poly.chain).values())
    print("Part 1:", result[-1] - result[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
