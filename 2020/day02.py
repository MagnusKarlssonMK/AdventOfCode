"""
Mostly an exercise in string parsing, checking the content after that is pretty straightforward.
"""
import sys
from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2020/day02.txt')


@dataclass(frozen=True)
class Password:
    nbr_range: list[int]
    letter: str
    password: str

    def is_valid(self, new_policy: bool) -> bool:
        if not new_policy:
            return self.nbr_range[0] <= self.password.count(self.letter) <= self.nbr_range[1]
        else:
            count = 0
            if len(self.password) >= self.nbr_range[0]:
                if self.password[self.nbr_range[0] - 1] == self.letter:
                    count += 1
                if len(self.password) >= self.nbr_range[1] and self.password[self.nbr_range[1] - 1] == self.letter:
                    count += 1
            return count == 1


class Database:
    def __init__(self, rawstr: str) -> None:
        self.__passwords = [Password(list(map(int, w[0].split('-'))), w[1].strip(':'), w[2])
                            for w in [line.split() for line in rawstr.splitlines()]]

    def get_valid_passwords_count(self, newpolicy: bool = False) -> int:
        return sum([1 for p in self.__passwords if p.is_valid(newpolicy)])


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        pwdb = Database(file.read().strip('\n'))
    print(f"Part 1: {pwdb.get_valid_passwords_count()}")
    print(f"Part 2: {pwdb.get_valid_passwords_count(True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
