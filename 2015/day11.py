"""
Some regex juggling and a recursive function to step the password.
"""
import sys
from pathlib import Path
import re

ROOT_DIR = Path(Path(__file__).parents[2], 'AdventOfCode-Input')
INPUT_FILE = Path(ROOT_DIR, '2015/day11.txt')


class Password:
    RULE_ONE = re.compile(r"abc|bcd|cde|def|efg|fgh|pqr|rst|stu|tuv|uvw|vwx|wxy|xyz")
    RULE_TWO = re.compile(r"[^iol]")
    RULE_THREE = re.compile(r"(.)\1.*(.)\2")

    def __init__(self, rawstr: str) -> None:
        self.__pwd = rawstr

    def __get_next_pwd(self, old_pwd: str) -> str:
        old_pwd_list = list(old_pwd)
        if old_pwd_list[-1] == 'z':
            return self.__get_next_pwd(''.join(old_pwd_list[0:-1])) + 'a'
        old_pwd_list[-1] = chr(ord(old_pwd_list[-1]) + 1)
        return ''.join(old_pwd_list)

    def get_new_password(self) -> "Password":
        new_pwd = self.__pwd
        while True:
            new_pwd = self.__get_next_pwd(new_pwd)
            if Password.RULE_ONE.search(new_pwd) and Password.RULE_TWO.search(new_pwd):
                pairs = Password.RULE_THREE.search(new_pwd)
                if pairs:
                    p1, p2 = pairs.groups()
                    if p1 != p2:
                        break
        return Password(new_pwd)

    def __repr__(self):
        return f"{self.__pwd}"


def main() -> int:
    with open(INPUT_FILE, 'r') as file:
        pwd = Password(file.read().strip('\n'))
    pwd = pwd.get_new_password()
    print(f"Part 1: {pwd}")
    pwd = pwd.get_new_password()
    print(f"Part 2: {pwd}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
