"""
Some regex juggling and a recursive function to step the password.
"""
import time
from pathlib import Path
import re


class Password:
    RULE_ONE = re.compile(r"abc|bcd|cde|def|efg|fgh|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz")
    RULE_THREE = re.compile(r"(.)\1.*(.)\2")

    def __init__(self, rawstr: str) -> None:
        self.__pwd = rawstr

    def __get_next_pwd(self, old_pwd: str) -> str:
        old_pwd_list = list(old_pwd)
        last_char = old_pwd_list[-1]
        if last_char == 'z':
            return self.__get_next_pwd(''.join(old_pwd_list[0:-1])) + 'a'
        if last_char in ('h', 'k', 'n'):
            old_pwd_list[-1] = chr(ord(last_char) + 2)
        else:
            old_pwd_list[-1] = chr(ord(last_char) + 1)
        return ''.join(old_pwd_list)

    def get_new_password(self) -> "Password":
        new_pwd = self.__pwd
        while True:
            new_pwd = self.__get_next_pwd(new_pwd)
            if Password.RULE_ONE.search(new_pwd):
                pairs = Password.RULE_THREE.search(new_pwd)
                if pairs:
                    p1, p2 = pairs.groups()
                    if p1 != p2:
                        break
        return Password(new_pwd)

    def __repr__(self):
        return f"{self.__pwd}"


def main(aoc_input: str) -> None:
    pwd = Password(aoc_input)
    pwd = pwd.get_new_password()
    print(f"Part 1: {pwd}")
    pwd = pwd.get_new_password()
    print(f"Part 2: {pwd}")


if __name__ == "__main__":
    ROOT_DIR = Path(Path(__file__).parents[1], 'AdventOfCode-Input')
    INPUT_FILE = Path(ROOT_DIR, '2015/day11.txt')

    start_time = time.perf_counter()
    with open(INPUT_FILE, 'r') as file:
        main(file.read().strip('\n'))
    end_time = time.perf_counter()
    print(f"Total time (ms): {1000 * (end_time - start_time)}")
