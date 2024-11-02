"""
Yet another string parsing problem. Extract the data and store in a dictionary, which can then be used to crosscheck
the validity conditions.
"""
import time
from pathlib import Path
from collections import defaultdict


class Passport:
    def __init__(self, rawdata: str) -> None:
        self.__data = defaultdict(lambda: "")
        for data in [item.split(':') for item in rawdata.split()]:
            self.__data[data[0]] = data[1]

    def isvalid(self, extraconditions: bool = False) -> bool:
        present = (self.__data['pid'] != "" and self.__data['byr'] != "" and self.__data['iyr'] != "" and
                   self.__data['eyr'] != "" and self.__data['hgt'] != "" and self.__data['ecl'] != "" and
                   self.__data['hcl'] != "")
        if not extraconditions or not present:
            return present
        if (int(self.__data['byr']) not in range(1920, 2003) or
                int(self.__data['iyr']) not in range(2010, 2021) or
                int(self.__data['eyr']) not in range(2020, 2031)):
            return False
        if self.__data['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False
        if len(self.__data['pid']) != 9 or not self.__data['pid'].isdigit():
            return False
        if len(self.__data['hcl']) != 7 or self.__data['hcl'][0] != '#':
            return False
        for c in self.__data['hcl'][1:]:
            if not c.isdigit() and c not in {'a', 'b', 'c', 'd', 'e', 'f'}:
                return False
        if self.__data['hgt'].find('cm') == -1 and self.__data['hgt'].find('in') == -1:
            return False
        cm = self.__data['hgt'].strip('cm')
        inch = self.__data['hgt'].strip('in')
        if ((cm.isdigit() and int(cm) not in range(150, 194)) or
                (inch.isdigit() and int(inch) not in range(59, 77))):
            return False
        return True


class PassportBatch:
    def __init__(self, rawstr: str) -> None:
        self.__passports = [Passport(p) for p in rawstr.split('\n\n')]

    def get_valid_passports_count(self, extraconditions: bool = False) -> int:
        return sum([1 for p in self.__passports if p.isvalid(extraconditions)])


def main(aoc_input: str) -> None:
    batch = PassportBatch(aoc_input)
    print(f"Part 1: {batch.get_valid_passports_count()}")
    print(f"Part 2: {batch.get_valid_passports_count(True)}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2020/day04.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
