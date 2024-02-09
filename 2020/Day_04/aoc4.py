"""
Yet another string parsing problem. Extract the data and store in a dictionary, which can then be used to crosscheck
the validity conditions.
"""
import sys
from collections import defaultdict


class Passport:
    def __init__(self, rawdata: str):
        self.data = defaultdict(lambda: "")
        for data in [item.split(':') for item in rawdata.split()]:
            self.data[data[0]] = data[1]

    def isvalid(self, extraconditions: bool = False) -> bool:
        present = (self.data['pid'] != "" and self.data['byr'] != "" and self.data['iyr'] != "" and
                   self.data['eyr'] != "" and self.data['hgt'] != "" and self.data['ecl'] != "" and
                   self.data['hcl'] != "")
        if not extraconditions or not present:
            return present
        if (int(self.data['byr']) not in range(1920, 2003) or
                int(self.data['iyr']) not in range(2010, 2021) or
                int(self.data['eyr']) not in range(2020, 2031)):
            return False
        if self.data['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False
        if len(self.data['pid']) != 9 or not self.data['pid'].isdigit():
            return False
        if len(self.data['hcl']) != 7 or self.data['hcl'][0] != '#':
            return False
        for c in self.data['hcl'][1:]:
            if not c.isdigit() and c not in {'a', 'b', 'c', 'd', 'e', 'f'}:
                return False
        if self.data['hgt'].find('cm') == -1 and self.data['hgt'].find('in') == -1:
            return False
        cm = self.data['hgt'].strip('cm')
        inch = self.data['hgt'].strip('in')
        if ((cm.isdigit() and int(cm) not in range(150, 194)) or
                (inch.isdigit() and int(inch) not in range(59, 77))):
            return False
        return True


def main() -> int:
    with open('../Inputfiles/aoc4.txt', 'r') as file:
        passports = [Passport(pp) for pp in file.read().strip('\n').split('\n\n')]
    print("Part 1:", sum([1 for pp in passports if pp.isvalid()]))
    print("Part 2:", sum([1 for pp in passports if pp.isvalid(True)]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
